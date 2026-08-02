# CFP Submission — AWS Community Day Mumbai 2026

**Session Title**
Don't Call the Model Twice: Verify Globally, Repair Locally

**Description**
Six parallel model calls turn a compliance manual into a 60-question quiz. Every batch returns valid JSON. Every batch clears its grounding check. Six out of six green — and the quiz is still wrong: one policy has zero questions, and two batches wrote the same one.

Nothing errored, so there is nothing to retry. Retry assumes failure is an error. Here the failure is a property that spans batches, and no single call can see it.

This talk builds the alternative: verify globally after the join, then regenerate only the failing batches — a data-dependent repair loop, written as an ordinary for-loop, on AWS Lambda durable functions with Amazon Bedrock and DynamoDB. Fifteen minutes, one code walkthrough, and the two traps: replay determinism, and why a correctly idempotent write silently swallows a repair.

**Session Format:** 15 Minutes Session

**Talk Level:** 300/400


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
Susmit Vengurlekar is a Data Systems Architect at SkillRev with 8+ years building software. He works on ForQuiz, which turns training manuals, decks, and SOPs into reviewable knowledge checks. Almost everywhere as susmitpy.