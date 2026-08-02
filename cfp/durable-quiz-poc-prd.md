# PRD — `durable-quiz` PoC (v2: plan → generate → verify → repair)

**Purpose:** produce a ~2 minute recorded demo for the talk *"Don't Call the Model Twice: Replay-Safe AI Pipelines with Lambda Durable Functions"* (AWS Community Day Mumbai 2026).

**Status:** dormant until the CFP is accepted. Written now so the deck's claims stay buildable. Re-verify everything in §12 the week the build starts, not the week this was written — the SDK surface moves.

**Target effort:** 1.5 focused days. The plan step and verify logic are new code relative to v1. If it's taking three days, something in Non-Goals crept back in.

---

## 1. The one sentence this build must earn

> "Global verification found that policy 4 had zero questions. The repair regenerated only batch 2, with the validator's findings appended to its prompt — the counter went 7 → 9, not 7 → 13, and the other batches came back from checkpoints untouched."

Secondary sentence (crash flavour, cheaper to show, still lands):

> "We crashed batch 2 mid-run. On replay, finished batches were restored from checkpoints and the counter proved Bedrock was never called twice for the same work."

Every line of code serves one of those two sentences or gets cut.

Demoted to P2 (see §6.8): the approval-callback sentence. With the Step Functions comparison now in the deck, free-while-idle waits are parity, not differentiation. The repair loop is the differentiator; spend the build budget there.

---

## 2. Non-goals — explicitly not building

- ForQuiz product integration of any kind
- Any frontend, web UI, or reviewer dashboard
- Authentication / authorization
- S3 input, PDF parsing, document ingestion
- Embeddings, vector store, RAG
- Multi-agent anything
- A model-based verifier — verify is deterministic code only (coverage vs plan, substring dedupe, policy keyword check)
- Sophisticated repair prompting — findings are appended to the prompt as plain text, nothing cleverer
- Multi-model comparison, prompt library, evaluation harness
- Retries tuned for production, DLQs, alarms, dashboards
- Tests beyond one smoke test

If reviewers ask "did you productionise it," the honest answer — "no, this is a teaching artifact, here's the repo" — is the right one.

---

## 3. Definition of done

Ship when all of these are true:

1. `python run.py --gap-in 2` produces a run where all batches generate cleanly, verify reports a coverage gap traceable to batch 2, and the repair loop fixes it in one iteration — regenerating only batch 2.
2. `python run.py --crash-at 2` produces a run that fails mid-generation and self-recovers, with finished batches restored from checkpoints.
3. The Lambda console execution history visibly distinguishes restored steps from re-executed steps in both runs.
4. A printed counter shows exact expected totals: plan(1) + generate(3) + repair(1) = **5** for the gap run; no double-counting in the crash run.
5. `python compare.py` prints two visibly different question sets from one identical prompt.
6. The repair prompt visibly contains the verifier's findings (print it during the demo run).
7. Records carry the full recipe: model_id, prompt_version, settings, source_rev, **attempt** — and a repair writes attempt=2 records without colliding with attempt=1.
8. Final quiz JSON prints to terminal, read path takes max(attempt) per question slot.
9. Repo is public, README has a 5-line quickstart, account ID and ARNs redacted from the recording.

---

## 4. Architecture

```
sample_doc.md  (bundled, 3 topics + 2 policy requirements)
        │
        ▼
Lambda durable function  (Python, durable execution enabled)
   ├── step: plan_batches          → 1 cheap Nova call → 3 batch specs
   │                                 (topic, difficulty, avoid-list, coverage targets)
   ├── parallel: generate(batch)   → 3 branches, Nova 2 Lite, 2 MCQs each
   │                                 max_concurrency=3, each branch checkpoints
   ├── repair loop (max 2 iterations):
   │     ├── step: verify          → deterministic: coverage vs plan,
   │     │                            cross-batch dedupe, policy keywords
   │     └── step: generate(batch, feedback, attempt)   ← failing batches only,
   │                                                       stable (sorted) order
   ├── [P2] wait_for_callback      → human approval, suspends
   └── step: assemble              → final quiz JSON (max attempt per slot)
        │
        ▼
DynamoDB (single table): questions · invocation counter · chaos/gap flags
```

3 batches × 2 questions — small enough for a terminal recording, big enough to show branch independence. No S3, no queues, no second Lambda.

---

## 5. Data model — one DynamoDB table

Table `durable-quiz`, PK `pk` (S), SK `sk` (S), on-demand billing.

| Item | pk | sk | attrs |
|---|---|---|---|
| Question | `RUN#{run_id}` | `Q#{batch_id}#{q_idx}#A{attempt}` | question, options, answer, batch_id, attempt, prompt_version, model_id, settings, source_rev |
| Invocation counter | `RUN#{run_id}` | `COUNTER` | `bedrock_calls` (atomic ADD) |
| Chaos flag | `CONFIG` | `CHAOS` | `crash_at_batch` (int or null) |
| Gap flag | `CONFIG` | `GAP` | `suppress_policy_in_batch` (int or null) — see §6.5 |
| Callback token (P2) | `RUN#{run_id}` | `CALLBACK` | token, status |

Question writes use `ConditionExpression: attribute_not_exists(pk) AND attribute_not_exists(sk)`.

**The attempt suffix is load-bearing.** Without it, a repair's write hits attempt-1's key, the condition fails silently, and the old questions survive — the exact bug slide 14 teaches. The conditional failure on a *replayed* publish is a talking point; a conditional failure on a *repair* would be a defect. The key design is what separates them.

---

## 6. Build spec

### P0 — must exist for the demo to work

**6.1 Source document.** `sample_doc.md`: 3 short topic sections (~120 words each) plus a stated requirements block ("the quiz must cover policies P1 and P2"). Topic the audience knows cold — VPC networking basics or SQL joins. Bundled in the package; no S3.

**6.2 `plan_batches` step.** One Bedrock call (Nova 2 Lite, thinking off) that returns 3 batch specs as JSON: topic, difficulty, avoid-list, and which coverage targets each batch owns. Increment the counter in the same step. Pin `PROMPT_VERSION` and model ID as constants; persist both (plus settings and source_rev) onto every record. If the plan JSON is malformed, the step's own retry handles it — that's the point.

**6.3 `generate` step.** Bedrock Converse API, Nova 2 Lite, thinking off. Exactly 2 MCQs as JSON per batch. Signature carries `(batch_spec, recipe, feedback=None, attempt=1)`. When `feedback` is present, append it verbatim to the prompt under a "REVIEWER FINDINGS — address these" header, and *print the final prompt* to the execution log (demo asset: the audience sees the findings land in the prompt). Counter increment via `UpdateItem ... ADD bedrock_calls 1` immediately after the Bedrock response, same step — keep the step small so the call-to-increment window is negligible, and mention that granularity trade-off in the talk.

**6.4 Parallel fan-out.** Use the SDK's parallel/map compound operation with `max_concurrency=3`, branch-level checkpointing, and error isolation so one failing branch doesn't fail the siblings. **This is now the headline claim of the talk — the deck's slide 7 is built on it.** If the primitive's semantics on partial failure differ from the deck's story (see §12, unknown #1), the deck changes, not the truth. Fallback if the primitive is missing or unusable: sequential per-section steps, and the talk's concurrency framing gets rewritten before the conference. Do not describe concurrency that wasn't built.

**6.5 `verify` step + gap injection.** Deterministic Python, no model call:
- Coverage: every target in the plan appears in at least one question (keyword match)
- Dedupe: normalized-substring overlap across batches
- Policy: P1/P2 keywords present somewhere

Gap injection: when `suppress_policy_in_batch == N`, the `generate` step for batch N gets "do NOT mention {policy}" quietly appended (a hidden instruction, mimicking a real drift bug). Verify then finds the gap organically — nothing is faked at the verify layer, which matters for honesty: the *check* is real, only the *defect* is planted. `--gap-in 2` sets the flag; repair regenerates batch 2 with findings and without the suppression (repair prompts never include the suppression line).

**6.6 Repair loop.** Max 2 iterations. `for batch_id in sorted(findings.failing)` — stable order, and the `sorted` is deliberate teaching content (deck slide 11). Each repair call passes `attempt=iteration+1`. Loop exits on `findings.ok` or max iterations; on max-out, fail loudly with the findings printed.

**6.7 Crash injection.** Before `generate` for batch N, a read of `CONFIG#CHAos` inside a step that *raises* when `crash_at_batch == N`. The read must live inside the failing step — failed steps write no checkpoint, so the flag is re-read on retry. If it were read once in a completed step, clearing the flag couldn't unstick the run.

Recovery path A (preferred): flip the flag to null via CLI while step retries back off; the retry passes on camera. Path B (backup): let it fail terminally, clear, re-invoke, show replay restoring checkpoints — contingent on §12 unknown #4.

**6.8 `compare.py`.** Standalone, ~15 lines, no Lambda. Same prompt, two Nova calls, outputs side by side. Still the cheapest strongest ten seconds in the demo, and it validates Bedrock access on day one.

**6.9 `run.py`.** Thin CLI: `--gap-in N`, `--crash-at N`, invoke, poll, pretty-print step progress + live counter + final quiz JSON. Large monospace output, no spinners.

### P2 — only if P0 is recorded and there's slack

**6.10 Human-review callback.** One approval gate for the whole run. Hard time-box: 60 minutes (down from 90 — it's parity content now, worth one slide with a console screenshot either way). Persist the token to DynamoDB so `approve.py` can find it. Cut into a separate 20-second clip droppable without re-editing.

---

## 7. Determinism build rules

Handler code re-executes from the top on every replay. Non-negotiable, and they double as slide 11:

- No `datetime.now()`, `time.time()`, `random`, or `uuid4()` in the workflow body. Such values are produced inside a step and restored from its checkpoint. `run_id` comes from the caller in the event.
- No branching on ambient state — env vars, feature flags, `os.environ` — outside a step. The recipe is an event input.
- No mutating module-level state between steps.
- Step results JSON-serialisable and small: pass batch IDs and indices between steps, not section text blobs. Question text goes to DynamoDB; checkpoints carry keys.
- Stable operation ordering across replays. Specifically: **the repair loop iterates `sorted(findings.failing)`** — loop *length* may depend on step results (fine), iteration *order* may not depend on set/dict ordering (trap).
- Findings objects must serialize stably too (sorted lists, not sets) since they flow through checkpoints into repair prompts.

Write `DETERMINISM.md` in the repo as these are hit; it becomes slide 11 with near-zero extra work.

---

## 8. Configuration

- **Runtime:** Python (confirm currently supported versions at build time; 3.13/3.14 at launch).
- **Region:** `ap-south-1`. Confirm durable functions availability (GA in Mumbai since Dec 2025) and Nova 2 Lite availability; if the model isn't in-region, use the global cross-region inference profile rather than moving the stack — and say so in the talk, because a Mumbai audience hits exactly this.
- **Model ID, prompt version, settings:** constants, persisted onto every record, never read from env inside the workflow body.

---

## 9. Recorded demo — shot list

Target ~2:00 main clip. 1080p, terminal font ≥ 20pt, dark background, zoom cranked, account ID redacted. It's edited video — cut ruthlessly.

| Time | Shot | On-screen |
|---|---|---|
| 0:00–0:08 | `cat sample_doc.md` | 3 topics + policy requirements, scroll fast |
| 0:08–0:18 | `python compare.py` | two different outputs, one prompt — **let it land** |
| 0:18–0:25 | `run.py --gap-in 2` starts | plan step → 3 batch specs print; counter: 1 |
| 0:25–0:40 | Parallel generation | 3 batches complete; counter: 4 |
| 0:40–0:55 | Verify fires | findings print: "policy P2: 0 questions (owner: batch 2)" |
| 0:55–1:10 | Repair | the repair prompt prints **with findings visible in it**; batch 2 regenerates; counter: **4 → 5, hold this frame** |
| 1:10–1:20 | Verify passes | loop exits; coverage table prints all-✓ |
| 1:20–1:35 | Console execution history | restored steps vs re-executed steps, visibly different |
| 1:35–1:50 | Crash run (compressed) | `--crash-at 2` → fail → flag cleared on camera → resume, no double-count |
| 1:50–2:00 | Final quiz JSON | 6 questions; batch 2 records show `attempt: 2` |

Closing frame doubles as deck slide 19's healed coverage matrix — engineer the verify output's final print to *be* that matrix.

---

## 10. Risks and fallbacks

| Risk | Mitigation |
|---|---|
| Parallel primitive's partial-failure semantics differ from the deck's story | §12 unknown #1, verify **first**; deck slide 7/8 language bends to reality, not vice versa |
| No parallel/map primitive in the current Python SDK | Sequential per-batch steps; rewrite the talk's concurrency claim before the conference |
| Nova 2 Lite not in `ap-south-1` | Global inference profile; note it in the talk |
| Repair loop churns (verify never satisfied) | Max 2 iterations + loud failure; tighten the plan prompt's coverage instructions |
| Gap injection too subtle — verify misses it | Keyword suppression is blunt by design; if needed, suppress the exact policy keyword string |
| Retry backoff window too short for the on-camera flag flip | Recovery path B |
| Terminally failed executions can't be resumed | Path A becomes mandatory — §12 unknown #4 |
| Model returns malformed JSON | Feature, not bug — it exercises step retry; tighten the prompt only if it's too frequent to record cleanly |
| Callback plumbing eats the schedule | It's P2 with a 60-minute box; screenshot fallback |

---

## 11. Build order

1. **Verify the load-bearing unknowns (§12) — 45 min.** Especially #1; the deck was submitted on its back.
2. CDK scaffold: durable-enabled Lambda + DynamoDB + Bedrock IAM (30 min).
3. `compare.py` — validates Bedrock access, highest value per line (20 min).
4. Happy path: plan → parallel generate → verify (passing) → assemble (2.5 hrs).
5. Counter + recipe/attempt persistence (30 min).
6. Gap injection + repair loop (2 hrs). **This is the heart; protect this block.**
7. Crash injection + recovery (1 hr).
8. Record P0 demo (1.5 hrs including retakes). **Before** touching P2.
9. P2 callback, 60-minute box (1 hr).
10. README, DETERMINISM.md, redact, publish repo (45 min).

---

## 12. To verify against current AWS docs before building

The SDK surface has moved through 2026; confirm rather than assume:

1. **Parallel/map compound operation in the Python SDK: exact name, signature, and — critically — partial-failure semantics.** What does retrying one failed branch look like in the execution history? Do sibling branches' checkpoints survive a branch failure? Are `max_concurrency` and completion criteria configurable as the deck implies? *This is the assumption the whole talk now leans on.*
2. Exact primitive names/signatures for step, wait, callback (slide 7 ships as "indicative pseudocode" for this reason — true it up for the conference build).
3. Default and configurable step retry policy and backoff (sizes the on-camera flag-flip window).
4. Whether a terminally failed execution can be resumed by re-invocation, and how (decides recovery path A vs B).
5. Checkpoint payload size and per-execution operation-count limits (slide 17's fan-out row and slide 18's budgets bullet cite these — get real numbers).
6. Version/alias behaviour for in-flight executions when code changes (slide 16 states the contract; confirm the mechanics).
7. History retention window defaults and configurability.