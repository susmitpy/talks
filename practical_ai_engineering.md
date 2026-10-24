---
theme: seriph
title: "Practical AI Engineering: From Architecture to Working Systems"
info: |
  ## Intelligence बैठक
  A 90-minute talk + hands-on workshop by Susmit Vengurlekar
class: pae
defaults:
  class: pae
transition: slide-left
colorSchema: dark
mdc: true
fonts:
  sans: Manrope
  mono: JetBrains Mono
---

<PaeTheme />

<div class="h-full flex flex-col justify-center">
  <div class="eyebrow">Intelligence बैठक</div>
  <h1 class="plain" style="font-size:3.4rem; line-height:1.1">
    Practical <span class="tool">AI Engineering</span>
  </h1>
  <p class="text-2xl">From architecture to working systems</p>


  <p class="muted mt-10">Susmit Vengurlekar</p>
</div>

---

<div class="h-full flex flex-col justify-center">
 
  <div class="flow mt-10 h-40" >
    <div class="node n-llm">LLMs<small>interpret · generate</small></div>
    <div class="arrow">+</div>
    <div class="node n-code">Deterministic code<small>rules · validation · state</small></div>
    <div class="arrow">+</div>
    <div class="node n-tool">Tools &amp; automation<small>APIs · browsers · MCP</small></div>
    <div class="arrow">=</div>
    <div class="node">A working system</div>
  </div>

</div>


---
src: ./pages/disclaimer.md
---

---
src: ./pages/about.md
---


---

<div class="eyebrow">Refresher</div>

# The model is one component, not the whole application


<style>
.mermaid {
  transform: scale(1);
  transform-origin: top center;
  display: flex;
  justify-content: center;
}
</style>

```mermaid
flowchart LR
  U([User request]) --> A[Application / orchestrator]
  A --> L[LLM]
  A --> C[Deterministic code]
  A --> T[Tools via MCP]
  L --> A
  C --> A
  T --> A
  S --> R([Result])
  S[System]
  L --> S
  C --> S
  T --> S

  classDef llm fill:#2a2340,stroke:#a78bfa,stroke-width:2px,color:#fff;
  classDef code fill:#12302c,stroke:#2dd4bf,stroke-width:2px,color:#fff;
  classDef tool fill:#3a2f12,stroke:#fbbf24,stroke-width:2px,color:#fff;
  classDef io fill:#1b2028,stroke:#8d97a6,stroke-width:2px,color:#fff;
  class S io;
  class L llm;
  class A,C code;
  class T tool;
  class U,R io;
```



---

<div class="eyebrow">Choose the right kind of work</div>

# Don't give everything to the LLM

<div class="grid grid-cols-2 gap-5 mt-4">
  <div class="card t-llm">
    <h3 class="llm">LLM</h3>
    <ul>
      <li>Messy text</li>
      <li>Drafting, rewriting, classifying, summarising</li>
      <li>Requests phrased a hundred different ways</li>
    </ul>
  </div>
  <div class="card t-code" v-click>
    <h3 class="code">Deterministic code</h3>
    <ul>
      <li>Exact calculations and business rules</li>
      <li>Validation and schemas</li>
      <li>Auth, permissions, critical state changes</li>
      <li>Retries and data integrity</li>
    </ul>
  </div>
</div>

<v-click>
<div class="question"><b>Audience question:</b> Would you let an LLM calculate GST on an invoice? Why not?</div>
</v-click>
---

<div class="eyebrow">Scale</div>

# A demo that works once is not yet a reliable system

<div class="grid grid-cols-3 gap-4 mt-6 items-center text-3xl">
  <div class="card t-tool"><span>Latency</span></div>
  <div class="card t-tool"><span>Reliability</span></div>
  <div class="card t-tool"><span>Cost</span></div>
  <div class="card t-tool"><span>Concurrency</span></div>
  <div class="card t-tool"><span>Observability</span></div>
  <div class="card t-tool"><span>Integrity &amp; safety</span></div>
</div>


---
layout: center
---

<div class="eyebrow">Case study</div>

<h1 class="plain" style="font-size:3.6rem">SHAW</h1>
---

# SHAW · Architecture

<style>
.mermaid {
  transform: scale(1.05);
  transform-origin: top center;
  display: flex;
  justify-content: center;
}
</style>

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'fontSize':'15px'}}}%%
flowchart LR
  subgraph ORCH [Pipeline]
    direction TB
    F[Filter + sort<br/>due date · priority]
    SEL[LLM picks tickets<br/>fallback: most urgent]
    W[Worktree + ports<br/>per ticket]
    F --> SEL --> W
  end

  subgraph AG [Shaw agent · Claude Code / Codex CLI]
    direction TB
    SH[Shaw orchestrator]
    SUB[Sub-agents<br/>planner · implement · reviewer<br/>browser-tester · pre-pr-runner …]
    SH --> SUB
  end

  subgraph TOOLS [MCP servers]
    direction TB
    M1[ticket-portal]
    M2[playwright]
    M3[(llm-memory · Qdrant)]
    M4[doc-extract]
  end

  D[Delivery<br/>Azure DevOps PR · Slack · ticket update]
  MON[Monitor · hooks · dashboard<br/>stall heal · retries · logs]

  ORCH --> AG
  AG <--> TOOLS
  MON -.-> AG

  classDef llm fill:#2a2340,stroke:#a78bfa,stroke-width:2px,color:#fff;
  classDef code fill:#12302c,stroke:#2dd4bf,stroke-width:2px,color:#fff;
  classDef tool fill:#3a2f12,stroke:#fbbf24,stroke-width:2px,color:#fff;
  classDef data fill:#132638,stroke:#60a5fa,stroke-width:2px,color:#fff;
  classDef human fill:#3a1a2c,stroke:#f472b6,stroke-width:2px,color:#fff;
  class SEL,SH,SUB llm;
  class F,W,D,MON,S code;
  class M1,M2,M4 tool;
  class P,M3 data;
  class H human;
```

---

<div class="eyebrow">Case study</div>

# Marto · Agentic Outbound System

<div class="flow mt-10">
  <div class="node n-llm">Research each domain<small>saved as MD · e.g. Finance</small></div>
  <div class="arrow">→</div>
  <div class="node n-tool">Apollo company search<small>keywords + filters</small></div>
  <div class="arrow">→</div>
  <div class="node n-llm">Pick one person<small>research them</small></div>
  <div class="arrow">→</div>
  <div class="node n-tool">Personalized email + follow-up<small>Apollo Sequence</small></div>
  <div class="arrow">→</div>
  <div class="node n-human">Detect "yes" reply<small>draft try-out link reply</small></div>
</div>

<!--
1. Research each domain, store findings as MD file (e.g. Finance).
2. Apollo keyword search with filters to fetch companies.
3. Find one person per company, research them.
4. Draft personalized email + follow-up, create Apollo Sequence.
5. If they reply yes, detect it and draft reply with try-out link.
-->

---

<div class="eyebrow">Integration lesson</div>

# The best integration isn't always the most elaborate one


<img src="/practical_ai/wireframe-dashboard.png" class="shot" style="max-width:100%; max-height:95%" />


---

# This slide deck was also made with AI

<div class="flow mt-4">
  <div class="node n-human">Voice brainstorm<small>ChatGPT Voice Mode, walking around the house</small></div>
  <div class="arrow">→</div>
  <div class="node n-llm">Structured outline<small>ChatGPT organises the raw ideas</small></div>
  <div class="arrow">→</div>
  <div class="node n-code">Markdown brief<small>slide-by-slide spec</small></div>
  <div class="arrow">→</div>
  <div class="node n-llm">Slide agent<small>reads my repos, writes Slidev</small></div>
  <div class="arrow">→</div>
  <div class="node n-human">Deck<small>I review and edit. And delete half the slides</small></div>
</div>


---


# Three practical workflows

<div class="grid grid-cols-2 gap-6 mt-2">
  <div class="card t-tool">
    <h3>CREATE · ForQuiz social content</h3>
    <ul class="small">
      <li><span class="human">Pitch</span> picked from our sales notes</li>
      <li><span class="llm">Agent</span> plans slides, spoken lines, caption, hashtags</li>
      <li><span class="code">Code</span> builds the deck and renders PNGs</li>
      <li><span class="code">Local TTS</span> (Kokoro) voices the mascot · ffmpeg makes the reel</li>
    </ul>
  </div>
  <div class="card t-tool" v-click>
    <h3>TEST · Browser tester</h3>
    <ul class="small">
      <li><span class="human">Requirement</span> + URL</li>
      <li><span class="llm">Agent</span> builds a checklist, drives the browser via <b>Playwright MCP</b></li>
      <li><span class="code">Code</span> records, trims still frames, merges clips</li>
      <li><span class="llm">LLM</span> writes narration · <span class="code">Piper TTS</span> speaks it</li>
    </ul>
  </div>
  <div class="card t-tool col-span-2" v-click>
    <h3>BUILD · How not to build with AI vs how to</h3>
    <div class="grid grid-cols-2 gap-6">
      <ul class="small">
        <li>❌ "Build me X" → agent guesses → rewrite loop</li>
      </ul>
      <ul class="small">
        <li>✅ <span class="llm">grill-me</span>: agent grills <span class="human">you</span>, one question at a time → plan very clear</li>
        <li>✅ <span class="code">domain-modeling</span>: glossary in CONTEXT.md → every term defined</li>
      </ul>
    </div>
  </div>
</div>

--- 

# Build systems, not just prompts

<div class="grid grid-cols-2 gap-16 mt-12 items-center">
  <div class="text-4xl space-y-6 dim ml-12">
    <div>Slides</div>
    <div>QA Agent Repo</div>
    <div>Hands On Repo</div>
    <div>Portfolio</div>
    <div>LinkedIn</div>
  </div>

  <div class="flex justify-center">
    <img src="/agentcore_policy/qr.png" class="w-96 rounded-xl" />
  </div>
</div>


---

<div class="eyebrow">Hands-on · 30–40 min</div>

# Your turn: a mini support agent + one MCP tool

## Best way to understand the system is to build it

<div class="flow mt-12">
  <div class="node n-human">Customer question<small>"where is ORD-101?"</small></div>
  <div class="arrow">→</div>
  <div class="node n-llm">Pydantic AI agent<small>mock LLM → Gemini Flash</small></div>
  <div class="arrow">→</div>
  <div class="node n-code">lookup_order()<small>mock data · single source of truth</small></div>
  <div class="arrow">←</div>
  <div class="node n-tool">MCP server<small>get_order</small></div>
</div>