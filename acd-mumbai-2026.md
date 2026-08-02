---
theme: seriph
title: "Don't Call the Model Twice — Verify Globally, Repair Locally"
info: |
  ## AWS Community Day Mumbai 2026
  A 15-minute lightning talk by Susmit Vengurlekar
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
  <div class="eyebrow">AWS Community Day Mumbai 2026</div>
  <h1 class="plain" style="font-size:4.2rem">
    Don't Call the<br><span class="orange">Model Twice</span>
  </h1>
  <p class="text-2xl mt-4">Verify globally, repair locally</p>
  <p class="muted mt-10">Susmit Vengurlekar · Data Systems Architect · SkillRev</p>
</div>

<!-- 20s. Fifteen minutes, one claim: retry is the wrong primitive for AI output. Straight into the failure. -->

---

<div class="eyebrow">60 questions · one compliance manual</div>

# Six batches. All green. The quiz is wrong.

<p class="compact muted">Six model calls in parallel · every batch returned valid JSON · every batch passed its grounding check</p>

<div class="matrix mt-4">
  <div class="head"></div><div class="head">B1</div><div class="head">B2</div><div class="head">B3</div><div class="head">B4</div><div class="head">B5</div><div class="head">B6</div>
  <div class="row">Topic A</div><div class="yes">✓</div><div class="yes">✓</div><div></div><div></div><div></div><div></div>
  <div class="row">Topic B</div><div></div><div class="dup">✓!</div><div class="yes">✓</div><div></div><div class="dup">✓!</div><div></div>
  <div class="row">Topic C</div><div></div><div></div><div></div><div class="yes">✓</div><div></div><div class="yes">✓</div>
  <div class="row">Policy 3</div><div></div><div></div><div class="yes">✓</div><div></div><div></div><div></div>
  <div class="row">Policy 4</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div><div class="no">✕</div>
</div>

<div class="flex gap-10 mt-4 compact">
  <span class="red">✕ Policy 4 — zero questions anywhere</span>
  <span class="orange">✓! Batches 2 &amp; 5 — the same question, twice</span>
</div>

<v-click><div class="question mt-5">Nothing errored. Every batch passed. <b>So what do you retry?</b></div></v-click>

<!-- 75s. Read the two red rows out loud — do not assume they scan it. Policy 4 is empty in all six columns; B2 and B5 wrote the same question. Then the click, then a real pause. This question is the whole talk. -->

---

<div class="eyebrow">Twenty seconds about me</div>

# Susmit Vengurlekar

<p class="muted">Data Systems Architect at SkillRev · 8+ years shipping software</p>

<p class="mt-6 text-xl">I work on <b class="orange">ForQuiz</b> — training manuals, decks, and SOPs become knowledge checks a human reviews before anyone sees them.</p>

<p class="muted mt-4 compact"><a href="https://forquiz.fusebytes.in">forquiz.fusebytes.in</a> · almost everywhere as <b class="orange">susmitpy</b></p>

<!-- 20s. Do not linger. Say the callout as one sentence and move — volunteering it early buys you credibility for the next twelve minutes. -->

---

<div class="eyebrow">What "correct" actually means</div>

# Four properties. Two of them no single call can see.

<div class="grid grid-cols-2 gap-5 mt-6">
  <div class="frame t-teal">
    <div class="tagline">Checkable per call</div>
    <h2 class="teal">Valid structure</h2>
    <p class="compact">Schema, option count, exactly one correct answer.</p>
  </div>
  <div class="frame t-teal">
    <div class="tagline">Checkable per call</div>
    <h2 class="teal">Grounded in the source</h2>
    <p class="compact">Every question traceable to the uploaded manual.</p>
  </div>
  <div class="frame t-red">
    <div class="tagline">Only after the join</div>
    <h2 class="red">Blueprint coverage</h2>
    <p class="compact">Every required topic and policy has questions.</p>
  </div>
  <div class="frame t-red">
    <div class="tagline">Only after the join</div>
    <h2 class="red">No duplicates</h2>
    <p class="compact">Not within a batch — <b>across</b> all six.</p>
  </div>
</div>

<p class="text-xl mt-6">A batch can satisfy everything it is able to check <b class="orange">and still be part of a wrong quiz.</b></p>

<!-- 55s. Left column is what a single call can certify about itself. Right column is a property of the set — and nothing inside one call can evaluate it. That asymmetry is the entire talk. -->

---

<div class="eyebrow">The shape of it</div>

# One handler, four steps, one back-edge

<div class="arch mt-5">

  <div class="arch-sources">
    <span>reference sites</span><span>PDFs &amp; decks</span><span>"what to cover" instruction</span>
    <span class="muted" style="border:none;background:none">→ ingest is out of scope today</span>
  </div>

  <div class="arch-box mt-4">
    <div class="tag">AWS Lambda durable function</div>
    <div class="flow">
      <div class="node">Plan<small>1 cheap call · batch specs</small></div>
      <div class="arrow">→</div>
      <div class="node hot">Generate ×6<small>Nova 2 Lite + Guardrails · parallel</small></div>
      <div class="arrow">→</div>
      <div class="node">Verify<small>deterministic · no model</small></div>
      <div class="arrow">→</div>
      <div class="node">Publish<small>after human approval</small></div>
    </div>
    <p class="tiny orange mt-3">↩ Verify → repair only the failing batch IDs → Verify again</p>
  </div>

  <div class="arch-band"><b class="teal">Your table · DynamoDB</b><span>questions, generation recipe, attempt number</span></div>
  <div class="arch-band managed"><b>Runtime-managed</b><span>checkpoint history — you do not build or operate this</span></div>

</div>

<!-- 65s. Guardrails runs on the model call itself, not as a later pass — an ungrounded response you have to notice separately is a response you already paid for. Verify is plain Python, no model. And the bottom band is the point: the state store is not yours. -->

---

<div class="eyebrow">Before you blame the validation</div>

# Green is a stricter check than you'd guess.

<div class="record mt-5">
  <div>BATCH 2 — validation result</div>
  <div> </div>
  <div>  schema            <span class="teal">pass</span>    10 questions · 4 options · exactly 1 correct</div>
  <div>  grounding         <span class="pin">0.91</span>    threshold 0.75 · Bedrock Guardrails</div>
  <div>  in-batch dupes    <span class="teal">pass</span>    no repeats inside this batch</div>
  <div> </div>
  <div>  → <span class="teal">GREEN</span></div>
</div>

<p class="mt-5">Contextual grounding runs <b>on the model call itself</b> — not as a later pass.</p>

<p class="text-xl mt-4">Six batches cleared that bar. <b class="orange">Policy 4 is still empty.</b></p>

<!-- 55s. Grounding says every question traces back to the manual — a real hallucination check, scored, not a vibe. Attach it to the call so a bad response never becomes a checkpoint. And say the last line slowly: a strict per-batch check, six times over, and the quiz is still wrong. -->

---
layout: center
---

<div class="text-center">
  <div class="eyebrow">The thesis</div>
  <h1 class="big plain" style="margin-bottom:2rem">Local validity is not global validity.</h1>
  <p class="lede muted narrow">Coverage and cross-batch duplication are properties of the <b>set</b>. Nothing inside a single call can evaluate them — no matter how strict that call's checks are.</p>
</div>

<!-- 40s. Say the headline, stop, let it sit. Then the second sentence once. Do not elaborate — slide 8 is the elaboration. -->

---

<div class="eyebrow">The obvious moves</div>

# Three answers, all bad.

<div class="grid grid-cols-3 gap-5 mt-6">
  <div class="frame t-red">
    <h2 class="red">Regenerate all six</h2>
    <p class="compact"><b>6 → 12 calls</b> to fix one gap.</p>
    <p class="compact muted">Five good batches come back <i>different</i>. Content a human already approved is silently replaced.</p>
  </div>
  <div class="frame t-red">
    <h2 class="red">One giant call</h2>
    <p class="compact">Context isn't the problem — <b>Nova 2 Lite holds a million tokens.</b></p>
    <p class="compact muted">But 60 questions strain a 64K output cap, one bad question fails the whole call, and you've lost per-topic control entirely.</p>
  </div>
  <div class="frame t-red">
    <h2 class="red">Hand-roll a resume handler</h2>
    <p class="compact">State table, resume entry point, poller, retry bookkeeping.</p>
    <p class="compact muted">Every new failure mode grows it. You now maintain a workflow engine.</p>
  </div>
</div>

<div class="callout mt-6">
What you actually want: regenerate <b class="orange">only the failing batches</b>, hand them the verifier's findings, and loop until coverage holds.
</div>

<!-- 70s — roughly 20s each, so one sentence per frame out loud. On the middle one: temperature zero narrows variance, it does not make output identical, so "regenerate all" really does churn approved content. Land on the callout; it's the spec for everything after this. -->

---

<div class="eyebrow">The mechanism</div>

# Replay isn't resume.

<p class="compact muted">The handler starts again <b>from line one</b>. Operations that already completed return their recorded result instead of running a second time.</p>

<div class="strip mt-5">
  <div class="chip done"><div class="mark">✓</div><small>B1 · recorded</small></div>
  <div class="chip done"><div class="mark">✓</div><small>B2 · recorded</small></div>
  <div class="chip failed"><div class="mark">✕</div><small>B3 · failed</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B4 · pending</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B5 · pending</small></div>
  <div class="chip pending"><div class="mark">·</div><small>B6 · pending</small></div>
</div>

<div class="grid grid-cols-3 gap-5 mt-6">
  <div class="frame t-teal"><h2 class="teal">STEP</h2><p class="compact">Run business logic. Result is checkpointed.</p></div>
  <div class="frame t-sky"><h2 class="sky">REPLAY</h2><p class="compact">Rerun from the top; completed steps hand back what they returned.</p></div>
  <div class="frame t-orange"><h2 class="orange">WAIT</h2><p class="compact">Suspend for an event — up to a year — without paying for idle compute.</p></div>
</div>

<p class="mt-5">You get a <b>runtime-managed history</b> instead of the resume handler from three slides ago.</p>

<!-- 55s. Emphasise "from line one" — people hear "resume" and picture a goto. Your code runs top to bottom every time; the SDK substitutes results for work already done. That's why determinism matters later. -->

---

<div class="eyebrow">The loop</div>

# Verify globally. Repair locally. Repeat.

<div class="flow mt-6">
  <div class="node">Plan<small>batch specs + avoid-list</small></div>
  <div class="arrow">→</div>
  <div class="node hot">Generate ×6<small>parallel · each one a step</small></div>
  <div class="arrow">→</div>
  <div class="node">Verify<small>coverage · dupes · policy</small></div>
  <div class="arrow">→</div>
  <div class="node">Review<small>human · suspended, free</small></div>
  <div class="arrow">→</div>
  <div class="node">Publish<small>DynamoDB</small></div>
</div>

<div class="loopback">
  <span class="curve">↩</span>
  <span>Verify fails → regenerate <b class="orange">only the failing batch IDs</b>, with the findings in the prompt → verify the whole set again.</span>
</div>

<div class="grid grid-cols-2 gap-5 mt-5">
  <div class="frame t-orange"><h2 class="orange">Length is unknown at runtime</h2><p class="compact">How many repair rounds you need depends on what verify finds. That's a data-dependent loop.</p></div>
  <div class="frame t-teal"><h2 class="teal">Finished batches never enter it</h2><p class="compact">A batch that passed is not regenerated, not re-priced, not re-reviewed.</p></div>
</div>

<!-- 70s. Only Generate is dangerous — remote, costly, nondeterministic. Verify is plain Python with no model in it. The back-edge is the whole design: unknown length, and it must never touch finished work. The two frames are why this is awkward in a workflow DSL. -->

---

<div class="eyebrow">The code</div>

# A data-dependent loop is just a for-loop.

```python
@durable_step
def generate(ctx, spec, recipe, feedback=None, attempt=1) -> str: ...   # → a DynamoDB key

@durable_execution
def handler(event, context: DurableContext):
    recipe = event["recipe"]                            # model + prompt + thresholds
    plan = context.step(plan_batches(event["doc"], recipe), name="plan")
    specs = {s.id: s for s in plan.specs}
    branches = [lambda ctx, s=s: ctx.step(generate(s, recipe), name=f"gen-{s.id}")
                for s in specs.values()]                # parallel() wants ctx-takers
    refs = dict(zip(specs, context.parallel(branches).get_results()))

    for attempt in range(2, MAX_ATTEMPTS + 1):
        findings = context.step(verify(plan, refs), name=f"verify-a{attempt}")
        if findings.ok: break
        for bid in sorted(findings.failing):            # stable order on replay
            refs[bid] = context.step(generate(specs[bid], recipe,
                findings.for_batch(bid), attempt), name=f"repair-{bid}-a{attempt}")

    gate = context.create_callback(name="review")       # suspends free · 72h timeout
    send_for_review(gate.callback_id, refs)
    if gate.result(): return context.step(publish(refs), name="publish")
```

<!-- 85s, the longest slide. Three things only. One: generate is decorated, so you invoke it and pass the result to context.step — that's the idiom. Two: refs holds DynamoDB keys; checkpoints cap at 256 KB and you do not want sixty questions of JSON replayed every time. Three: the repair loop is an ordinary for-loop over sorted IDs. Do not read the callback lines aloud — point and move. -->

---

<div class="eyebrow">What it cost</div>

# Nine calls, not thirteen.

<div class="strip mt-6">
  <div class="chip done"><div class="mark">✓</div><small>B1 · untouched</small></div>
  <div class="chip repair"><div class="mark">↻</div><small>B2 · repaired</small></div>
  <div class="chip done"><div class="mark">✓</div><small>B3 · untouched</small></div>
  <div class="chip done"><div class="mark">✓</div><small>B4 · untouched</small></div>
  <div class="chip repair"><div class="mark">↻</div><small>B5 · repaired</small></div>
  <div class="chip done"><div class="mark">✓</div><small>B6 · untouched</small></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-7">
  <div class="frame t-teal">
    <h2 class="teal">Repair locally</h2>
    <p class="compact">1 plan + 6 generate + <b>2 repairs</b></p>
    <p class="text-2xl mt-2"><b class="teal">9 model calls</b></p>
  </div>
  <div class="frame t-red">
    <h2 class="red">Regenerate everything</h2>
    <p class="compact">1 plan + 6 generate + <b>6 more</b></p>
    <p class="text-2xl mt-2"><b class="red">13 model calls</b></p>
  </div>
</div>

<p class="text-xl mt-7">With a cheap model, four saved calls is not the point. <b class="orange">Four batches a human already approved were never touched.</b></p>

<!-- 45s. The numbers are the setup; the last line is the payload. Say it and stop. The thing you cannot afford twice is the reviewer's afternoon, not the API bill. -->

---

<div class="eyebrow">Before you build this</div>

# Two things that will bite you.

<div class="grid grid-cols-2 gap-6 mt-5">
  <div class="frame t-red">
    <h2 class="red">1 · Replay runs your code again</h2>
    <p class="compact">Anything outside a step re-executes on every replay and must come out the same.</p>
    <p class="compact muted"><b>Into a step:</b> <code>uuid4()</code>, <code>now()</code>, env reads, every network call.</p>
    <p class="compact muted"><b>Fine in orchestration:</b> branching on step results, <code>sorted()</code> ordering.</p>
    <p class="compact mt-2">Loop <i>length</i> may depend on step output. Iteration <i>order</i> may not.</p>
  </div>
  <div class="frame t-red">
    <h2 class="red">2 · Your idempotency eats the repair</h2>
    <p class="compact">A conditional write keyed on <code>run + batch + index</code> is exactly right for replay safety.</p>
    <p class="compact muted">Then a repair regenerates batch 2 — same run, same batch, same index. Same key.</p>
    <p class="compact mt-2">The write is rejected as a duplicate. <b class="red">The bad questions survive.</b></p>
  </div>
</div>

```python
sk = f"Q#{batch_id}#{q_idx}#A{attempt}"          # ← the attempt belongs in the key
table.put_item(Item={"pk": f"RUN#{run_id}", "sk": sk, "question": q},
               ConditionExpression="attribute_not_exists(sk)")
# replay of a finished write → same key → ConditionalCheckFailed → expected no-op ✓
# genuine repair, attempt 2   → new key  → writes; reader takes max(attempt)      ✓
```

<!-- 85s, split ~30/55 — trap 2 is the one nobody sees coming. Frame it as the cruel part: the write path is *correctly* idempotent, and that correctness is what discards the fix. One character of key design separates "this is a replay, ignore it" from "this is a repair, take it." -->

---

<div class="eyebrow">The obvious question</div>

# Why not Step Functions?

<div class="grid grid-cols-2 gap-6 mt-8">
  <div class="frame t-orange">
    <h2 class="orange">Durable functions</h2>
    <p>A loop whose shape depends on its own results, living inside application code.</p>
    <p class="compact muted">Six batches, a verifier, and a feedback edge.</p>
  </div>
  <div class="frame t-sky">
    <h2 class="sky">Step Functions</h2>
    <p>Massive fan-out, or a graph someone non-technical has to read.</p>
    <p class="compact muted">Distributed Map, five services, an auditor.</p>
  </div>
</div>

<p class="text-xl mt-8">The loop picked this one. <b>Scale or a non-engineer audience picks the other.</b> Running both is normal.</p>

<!-- 30s. Not a product fight — say the last line and mean it. If someone's state machine already works, nothing here says rip it out. -->

---

<div class="eyebrow">If you remember three things</div>

# Verify globally. Repair locally.

<div class="grid grid-cols-3 gap-5 mt-7">
  <div class="frame t-red"><h2 class="red">01</h2><p class="compact">A batch cannot certify a property that spans batches. Coverage and duplication live after the join.</p></div>
  <div class="frame t-orange"><h2 class="orange">02</h2><p class="compact">Checkpoint and replay turn the repair loop into a for-loop. Length can depend on results; order cannot.</p></div>
  <div class="frame t-teal"><h2 class="teal">03</h2><p class="compact">Put the attempt in your idempotency key, or a correct write path will silently discard the fix.</p></div>
</div>

<div class="flex items-center gap-8 mt-8">
  <img src="/portfolio.png" alt="Portfolio QR" class="w-32 h-32 rounded-lg" />
  <div>
    <p class="text-2xl"><b class="teal">Every batch is still the batch a human approved.</b></p>
    <p class="text-xl mt-2">Nothing was bought twice.</p>
    <p class="muted mt-4">Susmit Vengurlekar · almost everywhere as <b class="orange">susmitpy</b> · <a href="https://forquiz.fusebytes.in">forquiz.fusebytes.in</a></p>
  </div>
</div>

<!-- 35s. No Q&A, so do not ask for questions — say "I'll be in the hallway, come argue with me about where your verify boundary sits." Then stop talking and leave the slide up. -->
