---
theme: seriph
title: "Don't Call the Model Twice — Replay-Safe AI Pipelines with Lambda Durable Functions"
info: |
  ## AWS Community Day Mumbai 2026
  A 30-minute session by Susmit Vengurlekar
class: acd
defaults:
  class: acd
transition: slide-left
mdc: true
fonts:
  sans: Manrope
  mono: JetBrains Mono
---

<AcdTheme />

<div class="h-full flex flex-col justify-center">
  <div class="eyebrow">AWS Community Day Mumbai 2026 · 17 October</div>
  <h1 class="plain" style="font-size:4.2rem">
    Don't Call the<br><span class="orange">Model Twice</span>
  </h1>
  <p class="text-2xl mt-4">Replay-safe AI pipelines with Lambda Durable Functions</p>
  <p class="muted mt-10">Susmit Vengurlekar · Data Systems Architect · SkillRev</p>
</div>

<!-- Don't call the model twice — not after a crash, and not after a repair. Let's earn both halves of that sentence. -->

---

<div class="eyebrow">Picture this…</div>

# One training manual must become one trustworthy quiz.

<p class="lede" style="margin-top:0.75rem"><b>ForQuiz</b> turns a deck, SOP, or chapter into an editable knowledge check.</p>
<p class="muted compact"><a href="https://forquiz.fusebytes.in">forquiz.fusebytes.in</a></p>

<div class="scenario mt-5">
  <v-click><div class="scenario-step"><b class="orange">01</b><span>Upload a training or compliance manual.</span></div></v-click>
  <v-click><div class="scenario-step"><b class="sky">02</b><span>Plan 60 questions across six batches.</span></div></v-click>
  <v-click><div class="scenario-step"><b class="teal">03</b><span>Generate those batches in parallel. One crashes; retry that batch independently.</span></div></v-click>
  <v-click><div class="scenario-step success"><b class="teal">04</b><span>Eventually, every batch returns valid JSON and passes its local checks.</span><strong>6 / 6 green</strong></div></v-click>
  <v-click><div class="scenario-step danger"><b class="red">05</b><span>The combined quiz has zero Policy 4 questions and a cross-batch duplicate.</span></div></v-click>
</div>

<v-click><div class="question mt-5">Nothing crashed. Every batch is green. <b>What do you retry now?</b></div></v-click>

<!-- This single workflow is the thread for the whole talk. We will first see why ordinary retries fail it, then build the repair loop that retries only the work that is actually wrong. -->

---

<div class="eyebrow">Roadmap</div>

# One loop, four questions

<div class="grid grid-cols-2 gap-5 mt-6">
  <div class="frame t-red"><h2 class="red">1 · Why retries fail AI</h2><p class="compact">A globally invalid quiz can be made of locally valid batches.</p></div>
  <div class="frame t-sky"><h2 class="sky">2 · Checkpoint &amp; replay</h2><p class="compact">Generate once, verify globally, repair only the failed work.</p></div>
  <div class="frame t-teal"><h2 class="teal">3 · Safe code</h2><p class="compact">Deterministic orchestration and repair-aware idempotency.</p></div>
  <div class="frame t-orange"><h2 class="orange">4 · Production choices</h2><p class="compact">Versioning, limits, and when to choose Step Functions instead.</p></div>
</div>

<!-- We will follow one concrete quiz workflow from failure to a production decision. -->

---

<div class="eyebrow">1 · Failure</div>

# Every batch succeeded. The quiz is wrong.

<p class="compact muted">60 questions · 6 planned batches · generated in parallel · all 6 returned valid JSON</p>

<div class="matrix mt-4">
  <div class="head"></div><div class="head">B1</div><div class="head">B2</div><div class="head">B3</div><div class="head">B4</div><div class="head">B5</div><div class="head">B6</div>
  <div class="row">Topic A</div><div class="yes">✓</div><div class="yes">✓</div><div></div><div></div><div></div><div></div>
  <div class="row">Topic B</div><div></div><div class="dup">✓!</div><div class="yes">✓</div><div></div><div class="dup">✓!</div><div></div>
  <div class="row">Topic C</div><div></div><div></div><div></div><div class="yes">✓</div><div></div><div class="yes">✓</div>
  <div class="row">Policy 3</div><div></div><div></div><div class="yes">✓</div><div></div><div></div><div></div>
  <div class="row">Policy 4</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div>
</div>

<div class="flex gap-10 mt-4 compact">
  <span class="red">✕ Policy 4 — zero questions</span>
  <span class="orange">✓! Batches 2 &amp; 5 — same question, twice</span>
</div>

<p class="mt-4">Cross-batch validation only runs <b>after the join</b>. By then, the money is spent.</p>

<!-- This is a compliance-manual quiz. Nothing errored, but the output is wrong in a way no single batch could detect. -->

---

<div class="eyebrow">Who is talking</div>

# I build the workflow this talk is about.

<div class="grid grid-cols-2 gap-8 mt-6 items-stretch">
  <div>
    <p class="text-2xl"><b>Susmit Vengurlekar</b></p>
    <p class="muted">Data Systems Architect at SkillRev · 8+ years shipping software</p>
    <p class="mt-6">At <b class="orange">ForQuiz</b>, a deck, SOP, or chapter becomes an editable knowledge check — then a human can review what it produced.</p>
    <p class="mt-4"><a href="https://forquiz.fusebytes.in">forquiz.fusebytes.in</a></p>
  </div>
  <div class="frame t-orange">
    <h2 class="orange">The engineering constraint</h2>
    <p>Generated content is not disposable.</p>
    <p class="compact muted">It can be reviewed, approved, exported, and relied on for compliance training.</p>
    <p class="mt-5"><b class="teal">The goal:</b> repair the wrong batch without silently replacing the good work around it.</p>
  </div>
</div>

<!-- This is not a résumé slide. I build the workflow we are tracing, where generated material becomes content people review and rely on. That is why a broad retry is a product problem, not merely a cost problem. -->

---

<div class="eyebrow">1 · Failure</div>

# Now what?

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="frame t-red">
    <h2 class="red">"Fix" #1 · Regenerate everything</h2>
    <p><b>6 → 12 model calls</b> to repair one gap.</p>
    <p class="muted">Five good batches come back different. Approvals, published IDs, and exports go inconsistent.</p>
    <p>You paid twice and silently replaced reviewed content.</p>
  </div>
  <div class="frame t-sky">
    <h2 class="sky">"Fix" #2 · Build a resume handler</h2>
    <p>A state table, resume entry point, poller, retry bookkeeping.</p>
    <p class="muted">Every new failure mode grows the handler.</p>
    <p>Congratulations — you now maintain a workflow engine.</p>
  </div>
</div>

<div class="callout mt-6">
What you actually want: regenerate <b class="orange">only failing batches</b>, append the validator's findings, and loop until coverage holds.
</div>

<!-- Temperature zero reduces variance; it does not make an output identical. I have built the hand-rolled engine; that is why this feature got my attention. -->

---
layout: center
---

<div class="text-center">
  <div class="eyebrow">1 · Failure</div>
  <h1 class="big plain" style="margin-bottom:2rem">A repair is not a redo.</h1>
  <p class="lede muted">The failing batch runs again. The finished batches must not.</p>
</div>

<!-- Hold that sentence. Everything that follows is machinery to make it true. -->

---

<div class="eyebrow">2 · Checkpoint &amp; Replay</div>

# Plan → generate → verify → repair

<div class="flow mt-6">
  <div class="node">Plan batches<small>1 cheap call · specs + avoid-list</small></div>
  <div class="arrow">→</div>
  <div class="node hot">Generate B1–B6<small>parallel · expensive · nondeterministic</small></div>
  <div class="arrow">→</div>
  <div class="node">Verify globally<small>coverage · dedupe · policy</small></div>
  <div class="arrow">→</div>
  <div class="node">Approval<small>human</small></div>
  <div class="arrow">→</div>
  <div class="node">Publish<small>DynamoDB</small></div>
</div>

<div class="callout mt-6">
↩ <b>Verify finds failures → repair only those batch IDs → generate them → verify globally again.</b><br>
Findings are appended to each repair prompt; finished batches never enter the back-edge.
</div>

<p class="mt-5">The targeted verify→repair back-edge is the hard part. Its length is unknown at runtime — and it must never touch a finished batch.</p>

<!-- Only Generate is dangerous: remote, expensive, nondeterministic. Verify is plain deterministic code. Keep your eye on the repair loop. -->

---

<div class="eyebrow">2 · Checkpoint &amp; Replay</div>

# Three primitives, one contract

<p class="compact muted">Checkpoint-and-replay means the handler may start again, while completed durable operations return their recorded result instead of running again.</p>

<div class="strip mt-5">
  <div class="chip done"><div class="mark">✓</div><small>B1 · done</small></div>
  <div class="chip done"><div class="mark">✓</div><small>B2 · done</small></div>
  <div class="chip failed"><div class="mark">✕</div><small>B3 · failed</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B4 · pending</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B5 · pending</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B6 · pending</small></div>
</div>

<div class="grid grid-cols-3 gap-5 mt-6">
  <div class="frame t-teal"><h2 class="teal">STEP</h2><p class="compact">An operation whose result is checkpointed.</p></div>
  <div class="frame t-sky"><h2 class="sky">REPLAY</h2><p class="compact">Handler reruns from the top; completed steps return checkpointed results.</p></div>
  <div class="frame t-orange"><h2 class="orange">WAIT</h2><p class="compact">Execution can suspend until resumed; confirm pricing and limits for your runtime.</p></div>
</div>

<p class="mt-6">The contract: <b>runtime-managed history</b> instead of a hand-built resume engine.</p>

<!-- Replay is not resume at line 214. The handler starts at the top and completed steps are substituted. -->

---

<div class="eyebrow">2 · Checkpoint &amp; Replay</div>

# The whole pipeline, with the repair loop

```python
@durable_execution
def handler(event, context: DurableContext):
    recipe = event["generation_recipe"]
    plan = context.step(plan_batches, event["document"], recipe)
    batch_map = {batch.id: batch for batch in plan.batches}
    initial = context.parallel([make_generate(batch, recipe, attempt=1)
                                for batch in batch_map.values()])
    results = dict(zip(batch_map, initial))  # immutable batch-ID -> result
    for attempt in range(2, MAX_ATTEMPTS + 1):
        findings = context.step(verify, plan, results)
        if findings.ok: break
        for batch_id in sorted(findings.failing):
            results[batch_id] = context.step(generate_batch, batch_map[batch_id],
                recipe, feedback=findings.for_batch(batch_id), attempt=attempt)
    context.wait_for_callback(approval_request(results))
    return context.step(publish, results)
```

<div class="flex justify-between tiny muted mt-2">
  <span><code>parallel</code> — branches checkpoint independently</span>
  <span><code>results</code> — keyed by immutable batch ID</span>
  <span><code>sorted()</code> — stable replay order</span>
</div>


<!-- Eighteen lines. The data-dependent loop is ugly in a workflow DSL and just a for-loop in code. Recipe is an input, not hidden environment state. -->

---

<div class="eyebrow">2 · Checkpoint &amp; Replay</div>

# Failure mode 1 — a batch crashes mid-run

<div class="steps mt-5">
  <div><b class="teal">Run 1</b><span class="muted ml-4">Batches 1–2 complete → checkpointed · batch 3 fails</span></div>
  <div><b class="sky">Replay</b><span class="muted ml-4">Handler starts at line one → plan, B1, and B2 restored</span></div>
  <div><b class="orange">Continue</b><span class="muted ml-4">Batch 3 runs · batches 4–6 proceed normally</span></div>
</div>

<div class="strip mt-6">
  <div class="chip done"><div class="mark">✓</div><small>B1 restored</small></div>
  <div class="chip done"><div class="mark">✓</div><small>B2 restored</small></div>
  <div class="chip repair"><div class="mark">↻</div><small>B3 retrying</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B4 pending</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B5 pending</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B6 pending</small></div>
</div>

<p class="text-xl mt-6"><b class="teal">2 restored</b> · <b class="orange">1 retried</b> · <b>no re-invocation of completed calls</b></p>

<p class="tiny muted mt-2">At-least-once delivery still applies at an interrupted-call boundary; model and write paths need their own idempotency controls.</p>

<!-- The boring failure is handled by the same mechanism. The interesting one is next. -->

---

<div class="eyebrow">2 · Checkpoint &amp; Replay</div>

# Failure mode 2 — verify finds the gap

<div class="steps mt-4">
  <div>All 6 batches complete → verify finds <b class="red">Policy 4 uncovered</b> and <b class="orange">B2 &amp; B5 duplicated</b>.</div>
  <div><b class="orange">Repair iteration 1</b> → B2 and B5 regenerate with the findings in the prompt; B1, B3, B4, B6 stay untouched.</div>
  <div><b class="teal">Verify again</b> → coverage holds → loop exits.</div>
</div>

<div class="matrix mt-4">
  <div class="head"></div><div class="head">B1</div><div class="head">B2</div><div class="head">B3</div><div class="head">B4</div><div class="head">B5</div><div class="head">B6</div>
  <div class="row">Topic A</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div>
  <div class="row">Topic B</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div>
  <div class="row">Topic C</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div>
  <div class="row">Policy 3</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div>
  <div class="row">Policy 4</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div>
</div>

<p class="text-xl mt-4">Model calls: <b class="teal">7 → 9</b><span class="muted">, not </span><b class="red">7 → 13</b></p>

<!-- This is the slide the talk exists for: one plan, six generates, exactly two repairs. Finished work is never re-bought. -->

---

<div class="eyebrow">2 · Checkpoint &amp; Replay</div>

# The demo <span class="muted text-2xl">(2 minutes, recorded)</span>

<div class="grid grid-cols-3 gap-5 mt-8">
  <div class="frame t-red"><h2 class="red">1 · Crash</h2><p class="compact">Chaos flag kills Batch 2. History shows the failed step and retry; completed batches stay green.</p></div>
  <div class="frame t-orange"><h2 class="orange">2 · Repair</h2><p class="compact">Verify prints "Policy 4: 0 questions." One batch regenerates with its feedback; peers restore.</p></div>
  <div class="frame t-teal"><h2 class="teal">3 · Counter</h2><p class="compact">DynamoDB invocation counter stays on screen and lands at plan + generates + repairs. Final matrix is all ✓.</p></div>
</div>

<p class="text-2xl mt-10">Watch the <b class="orange">counter</b>, not the green ticks.</p>

<!-- For reviewers: a recorded two-minute clip against a public repo. The three panels are the shot list, not a live-demo promise. -->

---
layout: center
---

<div class="text-center">
  <div class="eyebrow">Scope note</div>
  <h1 class="plain">Six batches explain the production pattern.</h1>
  <p class="lede narrow">The demo PoC is deliberately smaller: <b class="orange">3 batches</b> as a scaled-down proof. The 6-batch narrative is not a promise about the initial demo build.</p>
</div>

<!-- The talk teaches the production shape; the PoC proves the mechanism at smaller scale. -->

---
layout: center
---

<div class="text-center">
  <div class="eyebrow">Implementation note</div>
  <h1 class="plain">Treat the runtime behaviour as a design hypothesis.</h1>
  <p class="lede narrow">Before building, verify the current SDK's checkpoint and replay semantics, callback pricing and maximum wait, concurrency limits, and version/alias behaviour. The workflow pattern is the point; product guarantees must be checked against the release you deploy.</p>
</div>

<!-- This keeps the session useful without overstating a pre-build API contract. -->

---

<div class="eyebrow">3 · Replay-Safe Code</div>

# Replay requires deterministic orchestration

<div class="grid grid-cols-2 gap-6 mt-6">

<div class="frame t-teal">

<h2 class="teal">Safe in orchestration</h2>

- Stable input and ordering: `sorted(findings.failing)`
- Branching on step results
- Small, serializable values
- Explicit caller-provided run ID

</div>

<div class="frame t-red">

<h2 class="red">Move into a step</h2>

- Current time, random IDs, `uuid4()`
- External config reads: env vars, flags
- Network calls and side effects
- Anything that can differ on replay

</div>

</div>

<div class="callout mt-6">
Same inputs must produce the same sequence of durable operations. Loop <i>length</i> may depend on step results; iteration <i>order</i> may not.
</div>

<!-- The repair loop is legal because it branches on checkpointed step output. Iterating a set is the subtle trap. -->

---

<div class="eyebrow">3 · Replay-Safe Code</div>

# Pin the recipe, not just the prompt

<div class="record mt-5">
  <div>{</div>
  <div>  "pk": "RUN#a41f…",</div>
  <div>  "sk": "Q#B2#1#A2",</div>
  <div>  "question": "…",</div>
  <div class="pin">  "model_id": "amazon.nova-2-lite-v1:0",</div>
  <div class="pin">  "prompt_version": "v3",</div>
  <div class="pin">  "settings": {"temperature": 0.7},</div>
  <div class="pin">  "attempt": 2,</div>
  <div class="pin">  "source_rev": "sha256:8c1e…"</div>
  <div>}</div>
</div>

<p class="text-2xl mt-5">"Latest" is a deployment strategy — <b class="red">not a replay strategy.</b></p>
<p class="muted">Attempt matters: a repair can legitimately produce the same batch twice.</p>

<!-- This record answers: which exact recipe made the question, and was it original output or a repair? -->

---

<div class="eyebrow">3 · Replay-Safe Code</div>

# Checkpointing protects the execution.<br><span class="teal">Idempotency protects the world outside it.</span>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="frame t-sky">
    <h2 class="sky">Checkpointed step</h2>
    <p>A <b>completed</b> step is restored during replay.</p>
    <p class="muted">Protects against redoing finished work.</p>
  </div>
  <div class="frame t-teal">
    <h2 class="teal">Idempotent side effect</h2>
    <p>An <b>interrupted or failed</b> step can run more than once.</p>
    <p class="muted">Protects against duplicate writes, emails, and payments.</p>
  </div>
</div>

<div class="callout mt-6">
A repair adds a third case: <b>same batch, intentionally, attempt 2.</b> Your write path must tell it apart from an accidental replay.
</div>

<!-- Durable steps are at-least-once around failures. The title promises not to re-buy completed work; the write path provides the asterisk. -->

---

<div class="eyebrow">3 · Replay-Safe Code</div>

# The key must encode the attempt

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

<div class="grid grid-cols-2 gap-5 mt-4">
  <div class="callout compact">Replay of a completed publish → same key → conditional failure caught as an expected no-op <b class="teal">✓</b></div>
  <div class="callout compact">Repair attempt 2 → <b>new key</b> → write succeeds; reader takes <code>max(attempt)</code> <b class="teal">✓</b></div>
</div>

<p class="tiny muted mt-3">Without <code>attempt</code>, a repair is silently swallowed — and the bad questions survive.</p>

<!-- The conditional write that makes replays safe can make a repair invisible. The attempt suffix separates the two cases. -->

---

<div class="eyebrow">3 · Replay-Safe Code</div>

# The loop's exit gate costs nothing while it waits

<div class="grid grid-cols-3 gap-5 mt-8">
  <div class="frame t-orange"><h2 class="orange">Checkpoint work</h2><p class="compact">Generate, verify, and repair until coverage holds — all recorded.</p></div>
  <div class="frame t-sky"><h2 class="sky">Wait for callback</h2><p class="compact">Send the approval request; suspend execution. Confirm current pricing and maximum wait in the runtime docs.</p></div>
  <div class="frame t-teal"><h2 class="teal">Resume once</h2><p class="compact">Reviewer approves or rejects; recorded work restores before publish.</p></div>
</div>

<p class="text-xl mt-8">The approval arrives as an event. <b>Nothing is running while you wait.</b></p>

<!-- Step Functions can also wait free while idle. The repair loop, not this callback, is the decision point. -->

---

<div class="eyebrow">4 · Production</div>

# In-flight executions keep their version

<div class="mt-8">
  <div class="track"><b class="orange">Execution A</b><span class="muted">starts on v7</span><span class="flex-line"></span><b class="teal">completes on v7</b></div>
  <div class="track"><b class="sky">New execution</b><span class="muted">alias updated</span><span class="flex-line"></span><b>starts on v8</b></div>
</div>

<p class="text-xl mt-8">A running execution keeps the version that started it. New executions take the updated alias.</p>
<div class="callout compact mt-4"><b class="orange">The bridge:</b> a repair loop already in progress — or an approval wait already suspended — can complete on <b>v7</b> after <b>v8</b> ships.</div>
<p class="muted mt-3">$LATEST is a development convenience, not an in-flight reliability plan.</p>

<!-- A repair loop can live for hours, or an approval wait for weeks. Check exact alias mechanics before you build; this is the operational contract. -->

---

<div class="eyebrow">4 · Production</div>

# Why not Step Functions?

| Question | Durable Functions | Step Functions |
|---|---|---|
| Primary shape | Lambda-centric application logic | Cross-service workflow orchestration |
| Authoring | Python / Node / Java, in code | ASL graph, visual designer, CDK |
| Data-dependent loops | A for-loop with state | Expressible, painful to read and evolve |
| Fan-out width | Bounded per-execution budget — good for 6 batches | Distributed Map for massive fan-out |
| Visibility | Code + execution history, for engineers | Graph readable by auditors and non-engineers |
| Integrations | Lambda programming model + SDKs | 200+ native AWS integrations |

<p class="compact mt-4">6 batches with a feedback loop → <b class="orange">durable functions</b>. Tens of thousands of documents, or five services and a non-technical reader → <b class="sky">Step Functions</b>. Hybrid is normal.</p>

<!-- This is not a product fight. The loop selects Durable Functions here; scale and non-technical visibility select Step Functions elsewhere. -->

---

<div class="eyebrow">4 · Production</div>

# When durable functions are the wrong answer

<div class="callout mt-3">
  <h2 class="red">Your team can't hold the determinism line.</h2>
  <p class="compact">Every engineer touching the handler must understand the rules. If they cannot, don't hide that risk behind a framework.</p>
</div>

<div class="grid grid-cols-3 gap-5 mt-4">
  <div class="frame"><h2>Latency</h2><p class="compact muted">Checkpointing has overhead; wrong tool for sub-second paths.</p></div>
  <div class="frame"><h2>Budgets</h2><p class="compact muted">Operation count, checkpoint payloads, and history retention are bounded.</p></div>
  <div class="frame"><h2>Consistency debt</h2><p class="compact muted">The expensive thing is regenerating content a human already reviewed.</p></div>
</div>

<p class="mt-4">With a cheap model the argument was never the API bill. It is reviewed-content consistency, wall-clock, and rate-limit headroom.</p>

<!-- I am deliberately not showing a rupee figure. The thing you cannot afford twice is the reviewer's afternoon. -->

---

# Replay-safe AI workflow checklist

<div class="grid grid-cols-2 gap-x-10 gap-y-2 mt-6">
  <div>✓ Plan batches before generating</div>
  <div>✓ <b class="teal">Step</b> every model call and external operation</div>
  <div>✓ Keep orchestration <b class="sky">deterministic</b></div>
  <div>✓ <b class="orange">Verify globally, repair locally</b></div>
  <div>✓ Persist the full generation <b>recipe</b>, including attempt</div>
  <div>✓ Make every side effect idempotent — and repair-aware</div>
  <div>✓ Bound fan-out; deploy safely with executions in flight</div>
  <div>✓ Pick Step Functions when scale or auditors demand it</div>
</div>

<div class="flex items-center gap-5 mt-8">
</div>

<p class="text-xl mt-6"><b class="teal">Every batch is still the batch a human approved.</b> Nothing was bought twice.</p>

<!-- Questions welcome. Start with where the verify-then-repair boundary sits in your workflow. -->

---
layout: center
---

<div class="text-center">
  <h1 class="big plain">Thank you</h1>
  <p class="lede">Almost everywhere as <b class="orange">susmitpy</b></p>
  <div class="flex justify-center items-start gap-12 mt-8">
    <div>
      <img src="/portfolio.png" alt="Portfolio QR" class="w-40 h-40 rounded-lg" />
      <p class="muted mt-2">Portfolio</p>
    </div>
  </div>
</div>

<!-- Open for questions: start with where the verify-then-repair boundary sits in your workflow. -->
