---
theme: seriph
title: "Don't Call the Model Twice — Replay-Safe AI Pipelines with Lambda Durable Functions"
info: |
  ## AWS Community Day Mumbai 2026
  A 30-minute session by Susmit Vengurlekar
class: text-center
transition: slide-left
mdc: true
fonts:
  sans: Manrope
  mono: JetBrains Mono
---

<style>
:root { --ink:#0b1220; --panel:#14213d; --line:#29405f; --aws:#ff9900; --sky:#38bdf8; --mint:#31d0aa; --danger:#ff5a5f; --paper:#f7fbff; --muted:#b8c5d6; }
.slidev-layout { background:var(--ink); color:var(--paper); font-family:Manrope,ui-sans-serif,system-ui,sans-serif; }
h1,h2,h3 { color:var(--paper); font-weight:800; letter-spacing:-.025em; text-wrap:balance; } h1 { font-size:2.65rem; line-height:1.07; } h2 { font-size:1.35rem; } p,li { font-size:1.08rem; line-height:1.45; } li::marker { color:var(--aws); }
code,pre { font-family:"JetBrains Mono",ui-monospace,monospace; } pre { background:#070c16!important; border:1px solid var(--line); border-radius:12px; font-size:.9rem!important; line-height:1.35!important; }
.accent{color:var(--aws)} .mint{color:var(--mint)} .danger{color:var(--danger)} .sky{color:var(--sky)} .muted{color:var(--muted)}
.eyebrow { color:var(--aws); font-size:.77rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; } .big { font-size:3.55rem; line-height:1.04; font-weight:850; letter-spacing:-.035em; max-width:1050px; margin:0 auto; }
.frame,.callout { border:1px solid var(--line); border-radius:12px; background:#101b30; } .callout { background:#182945; padding:.85rem 1rem; } .compact { font-size:.9rem; } .tiny { font-size:.9rem; }
.batch-strip { display:grid; grid-template-columns:repeat(6,1fr); gap:.55rem; max-width:900px; margin:1rem auto; } .batch { min-height:64px; border:1px solid #53647d; border-radius:8px; display:flex; flex-direction:column; align-items:center; justify-content:center; font-weight:800; background:#26364f; } .batch small { font-weight:600; color:inherit; } .batch.done { background:var(--mint); border-color:var(--mint); color:#062a22; } .batch.failed { background:var(--danger); border-color:var(--danger); color:#320b10; } .batch.repair { background:var(--aws); border-color:var(--aws); color:#392000; } .batch.pending { background:#1b2a43; border-color:#64748b; color:#e2eaf5; }
.matrix { display:grid; grid-template-columns:1.35fr repeat(6,1fr); max-width:950px; margin:1rem auto; border:1px solid var(--line); border-radius:10px; overflow:hidden; } .matrix > div { padding:.42rem .3rem; border-right:1px solid var(--line); border-bottom:1px solid var(--line); font-weight:700; font-size:.87rem; } .matrix .head { background:#1a2b49; color:var(--aws); } .matrix .row { text-align:left; color:var(--muted); background:#101b30; } .matrix .yes { background:#123d35; color:var(--mint); } .matrix .no { background:#47202a; color:var(--danger); } .matrix .dup { background:#553717; color:#ffd38a; }
.flow { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:.55rem; margin-top:1.1rem; } .node { min-width:130px; padding:.8rem .65rem; border:1px solid var(--line); border-radius:10px; background:#101b30; font-weight:800; } .node small { display:block; margin-top:.25rem; color:var(--muted); font-size:.68rem; font-weight:600; } .node.expensive { border-color:var(--aws); } .arrow { color:var(--sky); font-size:1.5rem; } .loop { max-width:720px; margin:.75rem auto 0; padding:.55rem; border:2px solid var(--aws); border-radius:10px; color:#ffd38a; font-size:.9rem; }
.timeline { max-width:950px; margin:1.15rem auto; text-align:left; } .timeline div { padding:.75rem 1rem; border-bottom:1px solid var(--line); } .timeline div:first-child { border-top:1px solid var(--line); } .compare { width:100%; border-collapse:collapse; font-size:.82rem; text-align:left; } .compare th { color:var(--aws); border-bottom:2px solid var(--aws); padding:.42rem; } .compare td { padding:.44rem; border-bottom:1px solid var(--line); vertical-align:top; } .compare td:first-child { color:var(--sky); font-weight:800; }
.record { max-width:850px; margin:1rem auto; text-align:left; background:#070c16; border:1px solid var(--line); border-radius:12px; padding:.85rem 1.15rem; font-family:"JetBrains Mono",monospace; font-size:.92rem; line-height:1.45; white-space:pre; } .pinned { color:var(--aws); font-weight:800; } .deploy { position:relative; max-width:900px; margin:1.25rem auto; } .deploy:after { content:"deploy v8"; position:absolute; top:-.55rem; left:50%; color:var(--aws); font-size:.8rem; font-weight:800; } .deploy:before { content:""; position:absolute; top:0; bottom:0; left:51%; border-left:2px dashed var(--aws); } .track { display:flex; gap:1rem; align-items:center; min-height:58px; border-bottom:1px solid var(--line); text-align:left; } .track .end { margin-left:auto; }
</style>

<div class="h-full flex flex-col justify-center items-center text-left">
  <div class="eyebrow">AWS Community Day Mumbai 2026</div>
  <h1 style="font-size:4rem;max-width:1050px;">Don’t Call the<br><span class="accent">Model Twice</span></h1>
  <p class="text-2xl mt-5">Replay-safe AI pipelines with Lambda Durable Functions</p>
  <p class="muted mt-9">Susmit Vengurlekar · Data Systems Architect · SkillRev</p>
</div>

<!-- Don't call the model twice — not after a crash, and not after a repair. Let's earn both halves of that sentence. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">Roadmap</div><h1>One loop, four questions</h1><div class="grid grid-cols-2 gap-5 mt-7 text-left"><div class="frame p-5"><h2 class="danger">1 · Why retries fail AI</h2><p class="compact">A globally invalid quiz can be made of locally valid batches.</p></div><div class="frame p-5"><h2 class="sky">2 · Checkpoint &amp; replay</h2><p class="compact">Generate once, verify globally, repair only the failed work.</p></div><div class="frame p-5"><h2 class="mint">3 · Safe code</h2><p class="compact">Deterministic orchestration and repair-aware idempotency.</p></div><div class="frame p-5"><h2 class="accent">4 · Production choices</h2><p class="compact">Versioning, limits, and when to choose Step Functions instead.</p></div></div></div>

<!-- We will follow one concrete quiz workflow from failure to a production decision. -->

---

<div class="h-full flex flex-col justify-center">
  <div class="eyebrow">1 · Failure</div><h1>Every batch succeeded. The quiz is still wrong.</h1>
  <p class="compact muted">60 quiz questions · 6 planned batches · generated in parallel · all 6 returned valid JSON</p>
  <div class="matrix"><div class="head"></div><div class="head">B1</div><div class="head">B2</div><div class="head">B3</div><div class="head">B4</div><div class="head">B5</div><div class="head">B6</div><div class="row">Topic A</div><div class="yes">✓</div><div class="yes">✓</div><div></div><div></div><div></div><div></div><div class="row">Topic B</div><div></div><div class="dup">✓!</div><div class="yes">✓</div><div></div><div class="dup">✓!</div><div></div><div class="row">Topic C</div><div></div><div></div><div></div><div class="yes">✓</div><div></div><div class="yes">✓</div><div class="row">Policy 3</div><div></div><div></div><div class="yes">✓</div><div></div><div></div><div></div><div class="row">Policy 4</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div></div>
  <div class="flex justify-center gap-8 compact"><span class="danger">✕ Policy 4: zero questions</span><span class="accent">✓! Batches 2 &amp; 5: same question, twice</span></div><p class="text-xl mt-6">Cross-batch validation only runs after the join. By then, the money is spent.</p>
</div>

<!-- This is a compliance-manual quiz. Nothing errored, but the output is wrong in a way no single batch could detect. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">1 · Failure</div><h1>Now what?</h1><div class="grid grid-cols-2 gap-7 mt-5 text-left"><div class="frame p-6"><h2 class="danger">“Fix” #1: regenerate everything</h2><p><b>6 → 12 model calls</b> to repair one gap.</p><p class="muted">Five good batches return different. Approvals, published IDs, and exports are suddenly inconsistent.</p><p>You paid twice and silently replaced reviewed content.</p></div><div class="frame p-6"><h2 class="sky">“Fix” #2: build a resume handler</h2><p>A state table, resume entry point, poller, retry bookkeeping.</p><p class="muted">Every new failure mode grows the handler.</p><p>Congratulations — you now maintain a workflow engine.</p></div></div><div class="callout mt-6 text-xl">What you actually want: regenerate <b class="accent">only failing batches</b>, append the validator’s findings, and loop until coverage holds.</div></div>

<!-- Temperature zero reduces variance; it does not make an output identical. I have built the hand-rolled engine; that is why this feature got my attention. -->

---

<div class="h-full flex flex-col justify-center items-center"><div class="eyebrow">1 · Failure</div><h1 class="big">A repair is not a redo.</h1><p class="text-2xl mt-8">The failing batch runs again. The finished batches must not.</p></div>

<!-- Hold that sentence. Everything that follows is machinery to make it true. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">2 · Checkpoint &amp; Replay</div><h1>Plan → generate → verify → repair</h1><div class="flow"><div class="node">Plan batches<small>1 cheap call · specs + avoid-list</small></div><div class="arrow">→</div><div class="node expensive">Generate B1–B6<small>parallel · expensive · nondeterministic</small></div><div class="arrow">→</div><div class="node">Verify globally<small>coverage · dedupe · policy</small></div><div class="arrow">→</div><div class="node">Approval<small>human</small></div><div class="arrow">→</div><div class="node">Publish</div></div><div class="loop">↩ <b>Verify finds failures → repair only those batch IDs → generate them → verify globally again.</b><br>Findings are appended to each repair prompt; finished batches never enter the back-edge.</div><p class="text-xl mt-7">The targeted verify→repair back-edge is the hard part. Its length is unknown at runtime — and it must never touch a finished batch.</p></div>

<!-- Only Generate is dangerous: remote, expensive, nondeterministic. Verify is plain deterministic code. Keep your eye on the repair loop. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">2 · Checkpoint &amp; Replay</div><h1>Three primitives, one contract</h1><div class="batch-strip"><div class="batch done">✓<small>Batch 1 · done</small></div><div class="batch done">✓<small>Batch 2 · done</small></div><div class="batch failed">✕<small>Batch 3 · failed</small></div><div class="batch pending">·<small>Batch 4 · pending</small></div><div class="batch pending">·<small>Batch 5 · pending</small></div><div class="batch pending">·<small>Batch 6 · pending</small></div></div><div class="grid grid-cols-3 gap-5 mt-7 text-left"><div class="frame p-5"><h2 class="mint">STEP</h2><p class="compact">An operation whose result is checkpointed.</p></div><div class="frame p-5"><h2 class="sky">REPLAY</h2><p class="compact">Handler reruns from the top; completed steps can return checkpointed results.</p></div><div class="frame p-5"><h2 class="accent">WAIT</h2><p class="compact">Execution can suspend until resumed; confirm pricing and limits for your runtime.</p></div></div><p class="text-xl mt-6">The intended contract: runtime-managed history instead of a hand-built resume engine.</p></div>

<!-- Replay is not resume at line 214. The handler starts at the top and completed steps are substituted. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">2 · Checkpoint &amp; Replay</div><h1>The whole pipeline, with the repair loop</h1>
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
<div class="flex justify-between tiny muted"><span>parallel: branches checkpoint independently</span><span>results: keyed by immutable batch ID</span><span>sorted(): stable replay order</span></div><p class="tiny mt-3 muted">Illustrative pseudocode and API names: verify current durable-execution semantics, limits, and SDK before the conference build.</p></div>

<!-- Eighteen lines. The data-dependent loop is ugly in a workflow DSL and just a for-loop in code. Recipe is an input, not hidden environment state. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">2 · Checkpoint &amp; Replay</div><h1>Failure mode 1: a batch crashes mid-run</h1><div class="timeline"><div><b class="mint">Run 1</b><span class="muted ml-5">Batches 1–2 complete → checkpointed · batch 3 fails</span></div><div><b class="sky">Replay</b><span class="muted ml-5">Handler starts at line one → plan, B1, and B2 restored</span></div><div><b class="accent">Continue</b><span class="muted ml-5">Batch 3 runs · batches 4–6 proceed normally</span></div></div><div class="batch-strip"><div class="batch done">✓<small>B1 restored</small></div><div class="batch done">✓<small>B2 restored</small></div><div class="batch repair">↻<small>B3 retrying</small></div><div class="batch pending">·<small>B4 pending</small></div><div class="batch pending">·<small>B5 pending</small></div><div class="batch pending">·<small>B6 pending</small></div></div><p class="text-xl"><b class="mint">2 restored</b> · <b class="accent">1 retried</b> · <b>no re-invocation of completed calls</b></p><p class="tiny muted mt-2">At-least-once delivery still applies at an interrupted-call boundary; model and write paths need their own idempotency controls.</p></div>

<!-- The boring failure is handled by the same mechanism. The interesting one is next. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">2 · Checkpoint &amp; Replay</div><h1>Failure mode 2: verify finds the gap</h1><div class="timeline"><div>All 6 batches complete → verify finds <b class="danger">Policy 4 uncovered</b> and <b class="accent">Batches 2 &amp; 5 duplicated</b>.</div><div><b class="accent">Repair iteration 1</b> → B2 and B5 regenerate with findings in the prompt; B1, B3, B4, B6 stay untouched.</div><div><b class="mint">Verify again</b> → coverage holds → loop exits.</div></div><div class="matrix"><div class="head"></div><div class="head">B1</div><div class="head">B2</div><div class="head">B3</div><div class="head">B4</div><div class="head">B5</div><div class="head">B6</div><div class="row">Topic A</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="row">Topic B</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="row">Topic C</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="row">Policy 3</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="row">Policy 4</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div></div><p class="text-xl"><b>Model calls: </b><span class="mint">7 → 9</span><span class="muted">, not </span><span class="danger">7 → 13</span></p></div>

<!-- This is the slide the talk exists for: one plan, six generates, exactly two repairs. Finished work is never re-bought. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">2 · Checkpoint &amp; Replay</div><h1>The demo <span class="muted">(2 minutes, recorded)</span></h1><div class="grid grid-cols-3 gap-5 mt-8 text-left"><div class="frame p-5"><h2 class="danger">1 · Crash</h2><p class="compact">Chaos flag kills Batch 2. History shows failed step and retry; completed batches stay green.</p></div><div class="frame p-5"><h2 class="accent">2 · Repair</h2><p class="compact">Verify prints “Policy 4: 0 questions.” One batch regenerates with its feedback; peers restore.</p></div><div class="frame p-5"><h2 class="mint">3 · Counter</h2><p class="compact">DynamoDB invocation counter stays visible and finishes at plan + generates + repairs. Final matrix is all ✓.</p></div></div><p class="text-2xl mt-9">Watch the <span class="accent">counter</span>, not the green ticks.</p></div>

<!-- For reviewers: this is a recorded two-minute clip against a public repo. The three panels are the shot list, not a live-demo promise. -->

<!-- Scope: the deck uses a 6-batch production narrative; the demo PoC is a deliberately scaled-down 3-batch proof. -->

---

<div class="h-full flex flex-col justify-center items-center text-center"><div class="eyebrow">Scope note</div><h1>Six batches explain the production pattern.</h1><p class="text-2xl mt-7 max-w-4xl">The accepted-talk demo PoC is deliberately smaller: <b class="accent">3 batches</b> as a scaled-down proof. The 6-batch narrative is not a promise about the initial demo build.</p></div>

<!-- Keep the distinction explicit: the talk teaches the production shape; the PoC proves the mechanism at smaller scale. -->

---

<div class="h-full flex flex-col justify-center items-center text-center"><div class="eyebrow">Implementation note</div><h1>Use these runtime behaviors as a design hypothesis.</h1><p class="text-2xl mt-7 max-w-4xl">Before building, verify the current SDK’s checkpoint and replay semantics, callback pricing and maximum wait, concurrency limits, and version/alias behavior. The workflow pattern is the point; product guarantees must be checked against the release you deploy.</p></div>

<!-- This keeps the session useful without overstating a pre-build API contract. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">3 · Replay-Safe Code</div><h1>Replay requires deterministic orchestration</h1><div class="grid grid-cols-2 gap-7 mt-7 text-left"><div class="frame p-6"><h2 class="mint">Safe in orchestration</h2><ul><li>Stable input and ordering: <code>sorted(findings.failing)</code></li><li>Branching on step results</li><li>Small, serializable values</li><li>Explicit caller-provided run ID</li></ul></div><div class="frame p-6"><h2 class="danger">Move into a step</h2><ul><li>Current time, random IDs, <code>uuid4()</code></li><li>External config reads: env vars, flags</li><li>Network calls and side effects</li><li>Anything that can differ on replay</li></ul></div></div><p class="callout mt-6">Same inputs must produce the same sequence of durable operations. Loop <i>length</i> may depend on step results; iteration <i>order</i> may not.</p></div>

<!-- The repair loop is legal because it branches on checkpointed step output. Iterating a set is the subtle trap. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">3 · Replay-Safe Code</div><h1>Pin the recipe, not just the prompt</h1><div class="record">{
  "pk": "RUN#a41f…",
  "sk": "Q#B2#1#A2",
  "question": "…",
  <span class="pinned">"model_id": "amazon.nova-2-lite-v1:0",</span>
  <span class="pinned">"prompt_version": "v3",</span>
  <span class="pinned">"settings": {"temperature": 0.7},</span>
  <span class="pinned">"attempt": 2,</span>
  <span class="pinned">"source_rev": "sha256:8c1e…"</span>
}</div><p class="text-2xl mt-5">“Latest” is a deployment strategy — <span class="danger">not a replay strategy.</span></p><p class="muted">Attempt matters: a repair can legitimately produce the same batch twice.</p></div>

<!-- This record answers: which exact recipe made the question, and was it original output or a repair? -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">3 · Replay-Safe Code</div><h1>Checkpointing protects the execution.<br><span class="mint">Idempotency protects the world outside it.</span></h1><div class="grid grid-cols-2 gap-7 mt-8 text-left"><div class="frame p-6"><h2 class="sky">Checkpointed step</h2><p>A <b>completed</b> step is restored during replay.</p><p class="muted">Protects against redoing finished work.</p></div><div class="frame p-6"><h2 class="mint">Idempotent side effect</h2><p>An <b>interrupted or failed</b> step can run more than once.</p><p class="muted">Protects against duplicate writes, emails, and payments.</p></div></div><p class="callout mt-6">A repair adds a third case: <b>same batch, intentionally, attempt 2.</b> Your write path must tell it apart from an accidental replay.</p></div>

<!-- Durable steps are at-least-once around failures. The title promises not to re-buy completed work; the write path provides the asterisk. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">3 · Replay-Safe Code</div><h1>The key must encode the attempt</h1>
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
<div class="grid grid-cols-2 gap-5 mt-3 compact text-left"><div class="callout">Replay of completed publish → same key → conditional failure is caught as an expected no-op <span class="mint">✓</span></div><div class="callout">Repair attempt 2 → <b>new key</b> → write succeeds; reader takes <code>max(attempt)</code> <span class="mint">✓</span></div></div><p class="tiny mt-3 muted">Without <code>attempt</code>, a repair is silently swallowed — and the bad questions survive.</p></div>

<!-- The conditional write that makes replays safe can make a repair invisible. The attempt suffix separates the two cases. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">3 · Replay-Safe Code</div><h1>The loop’s exit gate costs nothing while it waits</h1><div class="grid grid-cols-3 gap-5 mt-8 text-left"><div class="frame p-6"><h2 class="accent">Checkpoint work</h2><p class="compact">Generate, verify, and repair until coverage holds — all recorded.</p></div><div class="callout p-6"><h2 class="sky">Wait for callback</h2><p class="compact">Send approval request; suspend execution. Confirm current pricing and maximum wait in the runtime docs.</p></div><div class="frame p-6"><h2 class="mint">Resume once</h2><p class="compact">Reviewer approves or rejects; recorded work restores before publish.</p></div></div><p class="text-xl mt-7">The approval arrives as an event. Nothing is running while you wait.</p></div>

<!-- Step Functions can also wait free while idle. The repair loop, not this callback, is the decision point. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">4 · Production</div><h1>In-flight executions keep their version</h1><div class="deploy"><div class="track"><span class="accent">Execution A</span><span>starts on v7</span><span class="end mint">completes on v7</span></div><div class="track"><span class="sky">New execution</span><span class="end">starts on v8</span></div></div><p class="text-xl mt-9">A running execution keeps the version that started it. New executions take the updated alias.</p><p class="muted">$LATEST is a development convenience, not an in-flight reliability plan.</p></div>

<!-- A repair loop can live for hours, or an approval wait for weeks. Check exact alias mechanics before the conference build; this is the operational contract. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">4 · Production</div><h1>Why not Step Functions?</h1><table class="compare mt-5"><thead><tr><th>Question</th><th>Durable Functions</th><th>Step Functions</th></tr></thead><tbody><tr><td>Primary shape</td><td>Lambda-centric application logic</td><td>Cross-service workflow orchestration</td></tr><tr><td>Authoring</td><td>Python / Node / Java, in code</td><td>ASL graph, visual designer, CDK</td></tr><tr><td>Data-dependent loops</td><td>A for-loop with state</td><td>Expressible, painful to read and evolve</td></tr><tr><td>Fan-out width</td><td>Bounded per-execution budget — good for 6 batches</td><td>Distributed Map for massive fan-out</td></tr><tr><td>Visibility</td><td>Code + execution history, for engineers</td><td>Graph readable by auditors and non-engineers</td></tr><tr><td>Integrations</td><td>Lambda programming model + SDKs</td><td>200+ native AWS integrations</td></tr></tbody></table><p class="compact mt-5">6 batches with a feedback loop → durable functions. Tens of thousands of documents, or five services and a non-technical reader → Step Functions. Hybrid is normal.</p></div>

<!-- This is not a product fight. The loop selects Durable Functions here; scale and non-technical visibility select Step Functions elsewhere. -->

---

<div class="h-full flex flex-col justify-center"><div class="eyebrow">4 · Production</div><h1>When durable functions are the wrong answer</h1><div class="callout mt-6 text-left"><h2 class="danger">Your team can’t hold the determinism line.</h2><p>Every engineer touching the handler must understand the rules. If they cannot, don’t hide that risk behind a framework.</p></div><div class="grid grid-cols-3 gap-5 mt-6 text-left"><div class="frame p-5"><h2>Latency</h2><p class="compact muted">Checkpointing has overhead; this is the wrong tool for sub-second paths.</p></div><div class="frame p-5"><h2>Budgets</h2><p class="compact muted">Operation count, checkpoint payloads, and history retention are bounded.</p></div><div class="frame p-5"><h2>Consistency debt</h2><p class="compact muted">The expensive thing is regenerating content a human already reviewed.</p></div></div><p class="text-xl mt-7">With a cheap model, the argument was never the API bill. It is reviewed-content consistency, wall-clock, and rate-limit headroom.</p></div>

<!-- I am deliberately not showing a rupee figure. The thing you cannot afford twice is the reviewer’s afternoon. -->

---

<div class="h-full flex flex-col justify-center"><h1>Replay-safe AI workflow checklist</h1><div class="grid grid-cols-2 gap-x-12 gap-y-3 max-w-5xl mx-auto text-left text-lg mt-5"><div>✓ Plan batches before generating</div><div>✓ <b class="mint">Step</b> every model call and external operation</div><div>✓ Keep orchestration <b class="sky">deterministic</b></div><div>✓ <b class="accent">Verify globally, repair locally</b></div><div>✓ Persist the full generation <b>recipe</b>, including attempt</div><div>✓ Make every side effect idempotent — and repair-aware</div><div>✓ Bound fan-out; deploy safely with executions in flight</div></div><div class="matrix mt-4"><div class="head"></div><div class="head">B1</div><div class="head">B2</div><div class="head">B3</div><div class="head">B4</div><div class="head">B5</div><div class="head">B6</div><div class="row">Topic A</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="row">Topic B</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="row">Topic C</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="row">Policy 3</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="row">Policy 4</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div><div class="yes">✓</div></div><div class="flex items-center justify-center gap-5 mt-3"><QRCode value="https://github.com/susmitpy/durable-quiz" :size="84"/><p>github.com/susmitpy/durable-quiz<br>susmitpy.github.io/talks</p></div><p class="text-xl"><b class="mint">Every batch is still the batch a human approved.</b> Nothing was bought twice.</p></div>

<!-- Questions welcome. Start with where the verify-then-repair boundary sits in your workflow. -->
