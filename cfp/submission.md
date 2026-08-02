# CFP Submission — AWS Community Day Mumbai 2026

**Session Title**
> Don't Call the Model Twice: Replay-Safe AI Pipelines with Lambda Durable Functions

**Description**
> You did the right things. You planned your quiz generation upfront — 60 questions in 6 batches, each batch scoped by topic, difficulty, and policy coverage before a single model call. You fanned the batches out in parallel. Every batch succeeded. Then the cross-batch validation ran: policy 4 has zero questions, and batches 2 and 5 test the same thing twice.
>
> Now what?
>
> The naive answer regenerates everything — paying again for four perfectly good batches and, because LLMs are nondeterministic, silently replacing content that may already be reviewed, referenced, or published. The hand-rolled answer persists partial results and writes a resume handler — congratulations, you now maintain a workflow engine. The correct answer regenerates *only* the failing batches, feeds the validator's findings back into their prompts, and loops until coverage holds — without ever re-calling the model for work that is already done. That repair loop is stateful, data-dependent, and unknown-length at plan time: exactly the shape that is awkward in a workflow DSL and natural in ordinary code.
>
> AWS Lambda durable functions (GA since re:Invent 2025, available in Asia Pacific (Mumbai)) run this loop inside the Lambda programming model you already use. Parallel branches checkpoint independently. On replay, the handler runs from the top but completed operations are restored from checkpoints instead of re-executed. Executions suspend free of charge — for a reviewer, for hours or months — and resume where they left off.
>
> I'll walk a plan → parallel generate → global verify → targeted repair pipeline on Amazon Nova 2 Lite through both failure modes: a mid-run crash and a post-join coverage gap. The execution history will show finished batches restored rather than re-run, while a live Bedrock invocation counter proves the model was never called twice for the same work. Then the parts the docs skim past: determinism rules for code that will be replayed, pinning the full generation recipe (model, prompt version, settings, attempt) into your records, idempotent writes that survive repair attempts, and what happens when you deploy while executions are in flight — plus an honest decision list for durable functions vs Step Functions, including the fan-out width at which Step Functions simply wins.
>
> **You'll leave able to:**
> 1. Structure an LLM generation job as plan → parallel generate → global verify → targeted repair, and identify which boundaries must be checkpointed.
> 2. Write handler code that is safe to replay — determinism constraints, recipe pinning, idempotency across repair attempts.
> 3. Choose between durable functions and Step Functions from a concrete decision list rather than vibes.
>
> **For:** serverless and AI engineers who have already shipped a Bedrock or LLM workload on Lambda. Python and Lambda assumed; no prior durable functions knowledge needed.

**Session Format:** 30 Minutes Session

**Talk Level:** 300/400

**Notes**
> **Agenda (30 min, Q&A included)**
> - 0:00–2:00 — The failure planning can't prevent: every batch green, quiz still wrong
> - 2:00–4:30 — The two wrong fixes: regenerate-all (cost + silent replacement), resume-by-hand (you built a workflow engine)
> - 4:30–7:00 — The pipeline in ~60 lines of Python: plan, parallel steps, the repair loop
> - 7:00–10:00 — Checkpoint and replay: what re-executes, what is restored, per-branch independence
> - 10:00–12:00 — **Recorded demo (2 min):** crash one batch, repair another; the counter never double-counts
> - 12:00–15:00 — Determinism: what you may not do inside replayed code
> - 15:00–18:00 — Recipe pinning and idempotency when the same batch gets attempt #2
> - 18:00–20:00 — Deploying while executions are in flight
> - 20:00–24:00 — Durable functions vs Step Functions — including where fan-out width means Step Functions wins
> - 24:00–26:00 — Limits and when *not* to use this
> - 26:00–30:00 — Replay-safe checklist + Q&A

**Speaker Name:** Susmit Vengurlekar

**Speaker Tagline:** Data Systems Architect — pipelines that survive failure

**Organization:** SkillRev

**LinkedIn:** https://www.linkedin.com/in/susmit-vengurlekar/

**Past Session Recordings:**
> - AWS Lambda in Action: Use Cases & AWS CDK — AWS User Group Mumbai — https://youtu.be/3rr95M8gyl8
> - Real Time CTR Analysis using Apache Flink and Kafka — Kafka Meetup — https://youtu.be/FsCWEC8Ir8I
> - Auth with Kong API Gateway — Kong Mumbai — https://youtu.be/5Il3ddDElRM
> - Full list: https://susmitpy.github.io/talks/

**Spoken at ACD Mumbai / AWS UG Mumbai before:** Yes — AWS User Group Mumbai, "AWS Lambda in Action: Use Cases & AWS CDK": https://youtu.be/3rr95M8gyl8

**Speaker Biography**
> Susmit Vengurlekar is a Data Scientist and Solution Architect at SkillRev in Mumbai, where he builds LLM-backed products on AWS. Over the last five years he has shipped real-time streaming pipelines on Kafka and Flink, knowledge-graph RAG systems on Neo4j, and a multi-warehouse data profiler with a checkpoint-and-resume engine he had to build by hand — which is roughly why Lambda durable functions got his attention. He has spoken at AWS User Group Mumbai, DevFest Mumbai, Global Azure Bootcamp, and the Kafka, MongoDB and Neo4j meetups, and writes at susmitpy.medium.com.