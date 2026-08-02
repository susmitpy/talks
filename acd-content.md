# Don't Call the Model Twice — Replay-Safe AI Pipelines with Lambda Durable Functions

Content source of truth for the Slidev deck `durable-functions-mumbai-2026.md`.
Event: AWS Community Day Mumbai 2026 · 17 October 2026 · 30-minute session.
Speaker: Susmit Vengurlekar · Data Systems Architect, SkillRev.
Product referenced: ForQuiz (forquiz.fusebytes.in).

---

## Slide 1 — Title

- Eyebrow: AWS Community Day Mumbai 2026
- Title: Don't Call the **Model Twice**
- Subtitle: Replay-safe AI pipelines with Lambda Durable Functions
- Byline: Susmit Vengurlekar · Data Systems Architect · SkillRev
- Notes: Don't call the model twice — not after a crash, and not after a repair. Let's earn both halves of that sentence.

---

## Slide 2 — Roadmap: one loop, four questions

1. **Why retries fail AI** — A globally invalid quiz can be made of locally valid batches.
2. **Checkpoint & replay** — Generate once, verify globally, repair only the failed work.
3. **Safe code** — Deterministic orchestration and repair-aware idempotency.
4. **Production choices** — Versioning, limits, and when to choose Step Functions instead.

Notes: We will follow one concrete quiz workflow from failure to a production decision.

---

## Slide 3 — About the speaker / the product

- Data Scientist & Solution Architect at SkillRev
- Building **ForQuiz** — Engage, Educate, Convert with gamified quizzes → forquiz.fusebytes.in
- The quiz-generation pipeline in this talk is ForQuiz's real workload
- Certified Neo4j Professional · 8+ years programming
- Notes: The pipeline is not a toy. It generates compliance-manual quizzes in production.

---

## Slide 4 — Failure: every batch succeeded, the quiz is still wrong

- Setup: 60 quiz questions · 6 planned batches · generated in parallel · all 6 returned valid JSON
- Coverage matrix (rows = required topics/policies, columns = batches B1–B6):
  - Topic A: covered by B1, B2
  - Topic B: covered by B3; **duplicated across B2 and B5** (same question, twice)
  - Topic C: covered by B4, B6
  - Policy 3: covered by B3
  - Policy 4: **covered by nothing — zero questions**
- Punchline: Cross-batch validation only runs after the join. By then, the money is spent.
- Notes: This is a compliance-manual quiz. Nothing errored, but the output is wrong in a way no single batch could detect.

---

## Slide 5 — Now what? Two bad fixes

**"Fix" #1: regenerate everything**
- 6 → 12 model calls to repair one gap.
- Five good batches return *different* content. Approvals, published IDs, and exports go inconsistent.
- You paid twice and silently replaced reviewed content.

**"Fix" #2: build a resume handler**
- A state table, resume entry point, poller, retry bookkeeping.
- Every new failure mode grows the handler.
- Congratulations — you now maintain a workflow engine.

Callout: What you actually want — regenerate **only failing batches**, append the validator's findings, and loop until coverage holds.

Notes: Temperature zero reduces variance; it does not make an output identical. I have built the hand-rolled engine; that is why this feature got my attention.

---

## Slide 6 — Statement slide

**A repair is not a redo.**

The failing batch runs again. The finished batches must not.

Notes: Hold that sentence. Everything that follows is machinery to make it true.

---

## Slide 7 — The shape: plan → generate → verify → repair

Flow:
1. Plan batches — 1 cheap call · specs + avoid-list
2. Generate B1–B6 — parallel · expensive · nondeterministic
3. Verify globally — coverage · dedupe · policy
4. Approval — human
5. Publish

Back-edge: Verify finds failures → repair only those batch IDs → generate them → verify globally again. Findings are appended to each repair prompt; finished batches never enter the back-edge.

Punchline: The targeted verify→repair back-edge is the hard part. Its length is unknown at runtime — and it must never touch a finished batch.

Notes: Only Generate is dangerous: remote, expensive, nondeterministic. Verify is plain deterministic code. Keep your eye on the repair loop.

---

## Slide 8 — Three primitives, one contract

- **STEP** — An operation whose result is checkpointed.
- **REPLAY** — Handler reruns from the top; completed steps return checkpointed results.
- **WAIT** — Execution can suspend until resumed; confirm pricing and limits for your runtime.

Batch strip visual: B1 done ✓, B2 done ✓, B3 failed ✕, B4–B6 pending.

Punchline: The intended contract — runtime-managed history instead of a hand-built resume engine.

Notes: Replay is not resume at line 214. The handler starts at the top and completed steps are substituted.

---

## Slide 9 — The whole pipeline, with the repair loop

```python
@durable_execution
def handler(event, context: DurableContext):
    recipe = event["generation_recipe"]
    plan = context.step(plan_batches, event["document"], recipe)
    batch_map = {batch.id: batch for batch in plan.batches}
    initial = context.parallel([make_generate(batch, recipe, attempt=1)
                                for batch in batch_map.values()])
    results = dict(zip(batch_map, initial))  # immutable batch-ID → result
    for attempt in range(2, MAX_ATTEMPTS + 1):
        findings = context.step(verify, plan, results)
        if findings.ok: break
        for batch_id in sorted(findings.failing):
            results[batch_id] = context.step(generate_batch, batch_map[batch_id],
                recipe, feedback=findings.for_batch(batch_id), attempt=attempt)
    context.wait_for_callback(approval_request(results))
    return context.step(publish, results)
```

Annotations:
- `parallel`: branches checkpoint independently
- `results`: keyed by immutable batch ID
- `sorted()`: stable replay order

Caveat: Illustrative pseudocode and API names — verify current durable-execution semantics, limits, and SDK before the conference build.

Notes: Eighteen lines. The data-dependent loop is ugly in a workflow DSL and just a for-loop in code. Recipe is an input, not hidden environment state.

---

## Slide 10 — Failure mode 1: a batch crashes mid-run

Timeline:
- **Run 1** — Batches 1–2 complete → checkpointed · batch 3 fails
- **Replay** — Handler starts at line one → plan, B1, and B2 restored
- **Continue** — Batch 3 runs · batches 4–6 proceed normally

Batch strip: B1 restored ✓, B2 restored ✓, B3 retrying ↻, B4–B6 pending.

Score: **2 restored · 1 retried · no re-invocation of completed calls**

Caveat: At-least-once delivery still applies at an interrupted-call boundary; model and write paths need their own idempotency controls.

Notes: The boring failure is handled by the same mechanism. The interesting one is next.

---

## Slide 11 — Failure mode 2: verify finds the gap

Timeline:
- All 6 batches complete → verify finds **Policy 4 uncovered** and **Batches 2 & 5 duplicated**.
- **Repair iteration 1** → B2 and B5 regenerate with findings in the prompt; B1, B3, B4, B6 stay untouched.
- **Verify again** → coverage holds → loop exits.

Matrix: all rows (Topic A, Topic B, Topic C, Policy 3, Policy 4) now fully covered.

Score: Model calls **7 → 9**, not 7 → 13.

Notes: This is the slide the talk exists for: one plan, six generates, exactly two repairs. Finished work is never re-bought.

---

## Slide 12 — The demo (2 minutes, recorded)

1. **Crash** — Chaos flag kills Batch 2. History shows failed step and retry; completed batches stay green.
2. **Repair** — Verify prints "Policy 4: 0 questions." One batch regenerates with its feedback; peers restore.
3. **Counter** — DynamoDB invocation counter stays visible and finishes at plan + generates + repairs. Final matrix is all ✓.

Punchline: Watch the **counter**, not the green ticks.

Notes: For reviewers — a recorded two-minute clip against a public repo. The three panels are the shot list, not a live-demo promise. The deck uses a 6-batch production narrative; the demo PoC is a deliberately scaled-down 3-batch proof.

---

## Slide 13 — Scope note

Six batches explain the production pattern.

The accepted-talk demo PoC is deliberately smaller: **3 batches** as a scaled-down proof. The 6-batch narrative is not a promise about the initial demo build.

Notes: Keep the distinction explicit: the talk teaches the production shape; the PoC proves the mechanism at smaller scale.

---

## Slide 14 — Implementation note

Use these runtime behaviors as a design hypothesis.

Before building, verify the current SDK's checkpoint and replay semantics, callback pricing and maximum wait, concurrency limits, and version/alias behavior. The workflow pattern is the point; product guarantees must be checked against the release you deploy.

Notes: This keeps the session useful without overstating a pre-build API contract.

---

## Slide 15 — Replay requires deterministic orchestration

**Safe in orchestration**
- Stable input and ordering: `sorted(findings.failing)`
- Branching on step results
- Small, serializable values
- Explicit caller-provided run ID

**Move into a step**
- Current time, random IDs, `uuid4()`
- External config reads: env vars, flags
- Network calls and side effects
- Anything that can differ on replay

Callout: Same inputs must produce the same sequence of durable operations. Loop *length* may depend on step results; iteration *order* may not.

Notes: The repair loop is legal because it branches on checkpointed step output. Iterating a set is the subtle trap.

---

## Slide 16 — Pin the recipe, not just the prompt

```json
{
  "pk": "RUN#a41f…",
  "sk": "Q#B2#1#A2",
  "question": "…",
  "model_id": "amazon.nova-2-lite-v1:0",
  "prompt_version": "v3",
  "settings": {"temperature": 0.7},
  "attempt": 2,
  "source_rev": "sha256:8c1e…"
}
```
(highlight the last five fields as "pinned")

Punchline: "Latest" is a deployment strategy — **not a replay strategy.**

Sub-point: Attempt matters — a repair can legitimately produce the same batch twice.

Notes: This record answers: which exact recipe made the question, and was it original output or a repair?

---

## Slide 17 — Checkpointing vs idempotency

Title: Checkpointing protects the execution. **Idempotency protects the world outside it.**

- **Checkpointed step** — A *completed* step is restored during replay. Protects against redoing finished work.
- **Idempotent side effect** — An *interrupted or failed* step can run more than once. Protects against duplicate writes, emails, and payments.

Callout: A repair adds a third case: **same batch, intentionally, attempt 2.** Your write path must tell it apart from an accidental replay.

Notes: Durable steps are at-least-once around failures. The title promises not to re-buy completed work; the write path provides the asterisk.

---

## Slide 18 — The key must encode the attempt

```python
def publish_once(run_id, batch_id, attempt, questions):
    for q_idx, question in enumerate(questions):
        try:
            table.put_item(Item={"pk": f"RUN#{run_id}",
              "sk": f"Q#{batch_id}#{q_idx}#A{attempt}", "question": question},
              ConditionExpression="attribute_not_exists(pk) AND attribute_not_exists(sk)")
        except ClientError as error:
            if error.response["Error"]["Code"] != "ConditionalCheckFailedException":
                raise
            # Same key already exists: expected replay, not a failed write.
```

- Replay of completed publish → same key → conditional failure caught as an expected no-op ✓
- Repair attempt 2 → **new key** → write succeeds; reader takes `max(attempt)` ✓
- Without `attempt`, a repair is silently swallowed — and the bad questions survive.

Notes: The conditional write that makes replays safe can make a repair invisible. The attempt suffix separates the two cases.

---

## Slide 19 — The loop's exit gate costs nothing while it waits

- **Checkpoint work** — Generate, verify, and repair until coverage holds — all recorded.
- **Wait for callback** — Send approval request; suspend execution. Confirm current pricing and maximum wait in the runtime docs.
- **Resume once** — Reviewer approves or rejects; recorded work restores before publish.

Punchline: The approval arrives as an event. Nothing is running while you wait.

Notes: Step Functions can also wait free while idle. The repair loop, not this callback, is the decision point.

---

## Slide 20 — In-flight executions keep their version

- Execution A starts on v7 → completes on v7
- New execution starts on v8

Punchline: A running execution keeps the version that started it. New executions take the updated alias.

Sub-point: $LATEST is a development convenience, not an in-flight reliability plan.

Notes: A repair loop can live for hours, or an approval wait for weeks. Check exact alias mechanics before the conference build; this is the operational contract.

---

## Slide 21 — Why not Step Functions?

| Question | Durable Functions | Step Functions |
|---|---|---|
| Primary shape | Lambda-centric application logic | Cross-service workflow orchestration |
| Authoring | Python / Node / Java, in code | ASL graph, visual designer, CDK |
| Data-dependent loops | A for-loop with state | Expressible, painful to read and evolve |
| Fan-out width | Bounded per-execution budget — good for 6 batches | Distributed Map for massive fan-out |
| Visibility | Code + execution history, for engineers | Graph readable by auditors and non-engineers |
| Integrations | Lambda programming model + SDKs | 200+ native AWS integrations |

Punchline: 6 batches with a feedback loop → durable functions. Tens of thousands of documents, or five services and a non-technical reader → Step Functions. Hybrid is normal.

Notes: This is not a product fight. The loop selects Durable Functions here; scale and non-technical visibility select Step Functions elsewhere.

---

## Slide 22 — When durable functions are the wrong answer

Headline warning: **Your team can't hold the determinism line.** Every engineer touching the handler must understand the rules. If they cannot, don't hide that risk behind a framework.

- **Latency** — Checkpointing has overhead; wrong tool for sub-second paths.
- **Budgets** — Operation count, checkpoint payloads, and history retention are bounded.
- **Consistency debt** — The expensive thing is regenerating content a human already reviewed.

Punchline: With a cheap model, the argument was never the API bill. It is reviewed-content consistency, wall-clock, and rate-limit headroom.

Notes: I am deliberately not showing a rupee figure. The thing you cannot afford twice is the reviewer's afternoon.

---

## Slide 23 — Replay-safe AI workflow checklist

- ✓ Plan batches before generating
- ✓ **Step** every model call and external operation
- ✓ Keep orchestration **deterministic**
- ✓ **Verify globally, repair locally**
- ✓ Persist the full generation **recipe**, including attempt
- ✓ Make every side effect idempotent — and repair-aware
- ✓ Bound fan-out; deploy safely with executions in flight

Closing line: **Every batch is still the batch a human approved.** Nothing was bought twice.

Links: github.com/susmitpy/durable-quiz · susmitpy.github.io/talks (QR code)

Notes: Questions welcome. Start with where the verify-then-repair boundary sits in your workflow.

---

## Slide 24 — ForQuiz

Your Partner in Edutainment — Engage, Educate, and Convert with gamified quizzes.

- 🎯 Engage customers with quizzes that surface what's on their mind
- 📚 Educate at peak attention with "Did You Know" interstitials
- 🔄 Convert with CTAs and in-game surveys
- 📊 Turn participation data into leads and customer studies

forquiz.fusebytes.in · Made in India for the World 🇮🇳

---

## Slide 25 — Connect / Q&A

- Almost everywhere as **susmitpy**
- Portfolio QR
- Thank you — now open for questions.
