---
theme: default
class: text-center
duration: 30
title: "Gateways, Guardrails & the Reality of GenAI Systems"
info: |
  ## Concepts
drawings:
  persist: false
transition: fade-out
mdc: true
fonts:
  sans: "Inter"
  serif: "Space Grotesk"
  mono: "Fira Code"
---

<style>
:root {
  /* Vibrant Cyber/GenAI Theme Colors */
  --slidev-theme-primary: #FFFFFF;
  --slidev-theme-secondary: #00e5ff; /* Neon Cyan */
  --slidev-theme-accent: #ff007f;   /* Neon Pink */
  --slidev-theme-background: #0f0a17; /* Solid Dark Theme Background */
  --slidev-theme-foreground: #E0E0E0;
  --slidev-code-background: rgba(10, 10, 15, 0.95);
}

.slidev-layout {
  background: var(--slidev-theme-background) !important;
  color: var(--slidev-theme-foreground) !important;
}

h1 {
  color: var(--slidev-theme-secondary);
  font-weight: 800 !important;
  letter-spacing: -0.02em;
}

h2 {
  color: var(--slidev-theme-secondary) !important;
  font-weight: 600 !important;
}

a {
  color: var(--slidev-theme-secondary);
  text-decoration-color: var(--slidev-theme-accent);
}

.glow-box {
  background: rgba(20, 20, 30, 0.6);
  border: 1px solid rgba(0, 229, 255, 0.2);
  box-shadow: 0 0 30px rgba(0, 229, 255, 0.15);
  border-radius: 16px;
  padding: 3rem;
  backdrop-filter: blur(10px);
}
</style>

<div class="h-full flex flex-col justify-center items-center">
  <div class="glow-box text-center transform hover:scale-105 transition-transform duration-500">
    <h1 style="font-size: 3.8rem; line-height: 1.2; margin-bottom: 0.5em;">Gateways, Guardrails & the Reality of GenAI Systems</h1>
    <div class="mt-8 text-xl font-mono text-gray-400">
      By Susmit Vengurlekar (@susmitpy)
    </div>
  </div>
</div>

---
src: ./pages/disclaimer.md
---

---
src: ./pages/about.md
---

---
src: ./pages/ice_breaker.md
---

---

# 🗺️ Agenda

<div class="text-2xl mt-8 mb-6 font-light text-gray-300">
Here is our roadmap for the next ~ 33 minutes:
</div>

<v-clicks>

* 🚀 **[25 min] Core Concepts & GenAI:** API / AI Gateways, AuthN/Z, and LLM Observability
* ❓ **[1 min] Promotion:** Mandatory ForQuiz plug 
* 🔑 **[2 min] Key Takeaways:** Spoiler, Nothing related to the talk
* 🎤 **[5 min] Q & A:** You ask, someone from audience answers

</v-clicks>

<style>
  li {
    font-size: 1.6rem;
    line-height: 2;
    margin-bottom: 0.8em;
    text-align: left;
    padding-left: 1rem;
    border-left: 3px solid transparent;
    transition: all 0.3s ease;
  }
  li:hover {
    border-left: 3px solid var(--slidev-theme-secondary);
    background: rgba(0, 229, 255, 0.05);
  }
</style>

---

# 💥 The Problem: Microservice & GenAI Sprawl

<div class="text-xl mt-2 mb-6 text-gray-300">
Building a single-tenant GenAI app is easy. Scaling it to production is hard.
</div>

<v-clicks>

* 💸 **The Single-Tenant Trap:** GenAI without AuthN/Z leads to untracked costs and "bill shock". You cannot rate-limit what you cannot attribute!
* 🕵️ **The Black Box:** Without observability, an LLM agent stuck in a loop or hallucinating is impossible to debug.
* 🔁 **Duplication of Effort:** Implementing Auth, JWT validation, and Token Tracking in *every single service*.
* 🔗 **Tight Coupling:** Hardcoding LLM providers (OpenAI, Anthropic) directly into business logic.

</v-clicks>

<style>
  li {
    font-size: 1.5rem;
    line-height: 1.6;
    margin-bottom: 0.8em;
    text-align: left;
  }
  .text-2xl {
    margin-bottom: 1.5em;
  }
</style>

---

<div class="mt-6" style="background: rgba(128, 114, 191, 0.15); padding: 1.2rem; border-left: 4px solid #ff007f; border-radius: 6px;">
  <b class="text-xl text-pink-400">🙋‍♂️ Audience Question:</b> How many of you have deployed an LLM app and accidentally left it open to unlimited API calls? Be honest! 😅
</div>



---

# 🌉 Anatomy of a Gateway (API & AI)

<div class="text-2xl mt-4 mb-6 text-center text-cyan-300">
A single entry point, abstracting backend architecture and AI models.
</div>

```mermaid
graph LR

C[Client]
B[Standard Backend]
LLM[LLM / GPU Inference]

subgraph The Gateway
    R[Ingress Routes]
    S[Logical Services]
    U[Upstream Load Balancing]

    R --> S --> U
end

C -->|Request| R
U -->|API Request| B
U -->|Prompt Ingress| LLM
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 5em;
        scale: 1.1;
    }
</style>

---

# 🌉 Anatomy of a Gateway

## 1. Ingress Routes

<div class="text-2xl mt-2 mb-8 text-center text-cyan-300">
Mapping external requests to internal boundaries (Traditional & AI).
</div>

```mermaid
graph LR

U[User] -->|PUT| UPR(/api<u>/users</u>/profile) --> |Mapped to| UR[User Route]

U --> |POST| UOR(/api<u>/v1/chat</u>) --> |Mapped to| CR[Chat/LLM Route]
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 5em;
        scale: 1.8;
    }
</style>

---

# 🌉 Anatomy of a Gateway

## 2. Logical Services

<div class="text-2xl mt-2 mb-8 text-center text-cyan-300">
Abstracting the compute. Is it a database CRUD app, or an AI Model?
</div>

```mermaid
graph LR

U[User] -->|Request| UR[User Route]

U --> |Prompt| CR[Chat/LLM Route]

UR --> |Mapped to| US[User Service]
CR --> |Mapped to| IS[Inference Service]
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 5em;
        scale: 1.7;
    }
</style>

---

# 🌉 Anatomy of a Gateway

## 3. Upstream Load Balancing

<div class="text-2xl mt-2 mb-6 text-center text-cyan-300">
Separating CPU workloads from GPU workloads and external providers.
</div>

```mermaid
graph LR

U[User] -->|Request| US[User Service]
U --> |Prompt| IS[Inference Service]

US --> |Mapped to| UU[Standard Upstream]
IS --> |Mapped to| IU[LLM Upstream]

UU --> |Forward| UT1[CPU Instance]

IU --> |Forward| EXT[External: OpenAI/Anthropic API]
IU --> |Fallback| SLF[Self-Hosted: Local GPU/vLLM]
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 2em;
        scale: 1.1;
    }
</style>

---

# 🔐 Authentication vs Authorization in GenAI

<div class="text-2xl mt-4 mb-6 text-pink-400">
Identity, Access, and Cost Allocation.
</div>

<v-clicks>

* 🛡️ **Authentication (AuthN):** Verifying identity.
    * *Example:* Checking a password, validating a JWT signature.
    * *Gateway Role:* Ideal. Validate tokens centrally.

* 🔑 **Authorization (AuthZ):** Determining permissions.
    * *Example:* Can user X view record Y? Can POST to `/payments` to create payment ?
    * *Gateway Role:* Basic RBAC (Role-Based Access Control) is possible. Fine-grained, business-logic-heavy AuthZ usually stays in the backend.

</v-clicks>

<style>
  li {
    font-size: 1.7rem;
    line-height: 1.4;
    margin-bottom: 0.6em;
    text-align: left;
  }
  ul ul li {
      font-size: 1.4rem;
      color: var(--slidev-theme-foreground);
      opacity: 0.9;
  }
</style>

---

# 🎟️ The JWT Lifecycle

<div class="text-xl mt-4 mb-6 p-4 border-l-4 border-cyan-400 rounded bg-cyan-900 bg-opacity-20 text-cyan-200">
<b>Gateway Role:</b> Validate JWT centrally. If token is invalid, drop the request before hitting expensive GPU instances.
</div>

<v-clicks>

* 🧠 **Authorization (AuthZ) & Multi-Tenancy in GenAI:**
    * *Standard:* Can user X view record Y?
    * *GenAI:* Is this tenant allowed to use the `GPT-4` route, or only `Llama-3-8B`? Are they within their **token rate-limit** quota? 
    * *Security:* AuthZ prevents one compromised tenant from exhausting your entire organization's LLM API budget.

</v-clicks>

<style>
  li {
    font-size: 1.8rem;
    line-height: 1.4;
    margin-bottom: 0.6em;
    text-align: left;
  }
  ul ul li {
      font-size: 1.80rem;
      color: var(--slidev-theme-foreground);
      opacity: 0.9;
  }
</style>

---

# 🔌 The Middleware/Plugin Pattern for Microservices

<br/>

```mermaid
graph LR

C[Client]
B[Backend / LLM]

subgraph Gateway
    subgraph Route Scope
      RPL1[Auth Validation]
      RPL2[Token Rate Limiting]

      RPL1 --> RPL2
    end
    subgraph Service Scope
      SPL1[Claim-to-Header]
      SPL2[Telemetry / Token Counting]

      SPL1 --> SPL2
    end
    U[Upstream]

    RPL2 --> |Mapped to| SPL1 --> |Mapped to| U
end

C --> RPL1
U --> B
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 4em;
        scale: 1.1;
    }
</style>

---

# 💉 Claim-to-Header Injection (Tenant Allocation)

```mermaid
sequenceDiagram
    participant C as Client
    participant G as API Gateway
    participant B as Inference Backend

    C->>G: Request with JWT
    Note over G: Validates JWT signature<br/>Extracts 'sub' and 'tier'
    G->>B: Forward Request<br/>Headers: auth-user=123, auth-tier=premium
    Note over B: Trusts header<br/>Allocates priority GPU Queue
    B-->>C: Streaming Output
```

<style>
  .mermaid {
    display: flex;
    justify-content: center;
    margin-top: -1em;
    scale: 1;
  }
</style>

---

# 📊 Observability (LLMOps)

<div class="text-3xl mt-4 mb-6 text-cyan-300">
Gaining visibility into the GenAI black box.
</div>

<v-clicks>

* 📝 **Logs:** Not just errors. Tracking prompts, responses, and tool outputs (with PII masking at the gateway).
* 📈 **Metrics (The GenAI Additions):** 
    * *Latency:* **TTFT** (Time to First Token) vs Total Generation Time.
    * *Usage:* Input Tokens, Output Tokens, Cost per Tenant.
* 🕸️ **Traces:** Journey of a request across distributed systems. Crucial for debugging slow RAG pipelines or erratic Agents.
* 🛡️ **Gateway Advantage:** The Gateway initiates the distributed trace (OpenTelemetry) and standardizes token metrics regardless of whether the backend is OpenAI or a self-hosted GPU.

</v-clicks>

<style>
  li {
    font-size: 1.45rem;
    line-height: 1.2;
    margin-bottom: 0.8em;
    text-align: left;
  }
</style>

---

# 🕵️‍♂️ Tracing Agents & Sandboxes

<div class="text-xl mt-2 mb-4 text-center text-cyan-300">
Distributed tracing (OpenTelemetry) makes complex Agent loops observable.
</div>

```mermaid
gantt
    dateFormat  s
    axisFormat  %S
    title OpenTelemetry Trace: Agent execution
    
    section Orchestrator
    Agent Planning               :a1, 1, 2s

    section LLM / GPU Node
    Reason & Select Tools    :a2, 2, 3s
    Agentic RAG Loop           :a3, 5, 5s
    Write Code in Sandbox           :a4, 10, 4s
    Synthesize Output       :a5, 17, 3s
    
    section Code Sandbox
    Spin up Container            :a6, 3, 10s
    Execute Python Tool          :a7, 14, 3s
```

<div class="mt-8 p-4 bg-gray-800 bg-opacity-60 rounded-lg text-xl text-center shadow-[0_0_20px_rgba(255,0,127,0.15)] border border-gray-700">
<span class="text-pink-400 font-bold">Span Attributes attached:</span> Agent ID, Tool Name, Container ID, Container Resources, Host Instance, Token Count, Latency.
</div>

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 1em;
        scale: 1.1;
    }
</style>

---

# 📦 Containerization & Isolation

* 🐳 **Docker Containers:** Package the application code, ensuring consistent execution.

<v-clicks>

* 🏖️ **GenAI Sandboxing:** 
    * Agents that write and execute code *must* do so in isolated, ephemeral sandbox containers (without network access to your DB!).
* 🚦 **Gateway Networking Strategy:**
    * Gateway sits on the "external" edge.
    * CPU Orchestration / Backends sit on internal networks.
    * Self-hosted GPU instances and Agent Sandboxes are highly restricted, isolated nodes. The Gateway ensures strict AuthZ before any traffic reaches them.

</v-clicks>

<style>
  li {
    font-size: 1.6rem;
    line-height: 1.5;
    margin-bottom: 0.8em;
    text-align: left;
  }
  ul ul li {
      font-size: 1.4rem;
      color: var(--slidev-theme-foreground);
      opacity: 0.9;
  }
</style>

---

# 🌍 The Open-Source Landscape

<div class="text-2xl mt-2 mb-2 text-center font-light text-gray-300">
Abstracting these concerns is a community-wide effort.
</div>

<div class="grid grid-cols-2 gap-8 mt-1">
  <div class="bg-gray-800 bg-opacity-50 p-6 rounded-xl border border-cyan-500 hover:border-pink-500 transition-colors shadow-[0_0_20px_rgba(0,229,255,0.1)]">
    <h2 class="text-cyan-400 mb-4 border-b border-gray-700 pb-2">🚦 Gateways & Orchestration</h2>
    <ul>
      <li><b>Kong API Gateway / LiteLLM</b></li>
      <li><b>Envoy Proxy</b> (Istio, Gloo)</li>
      <li><b>vLLM / Ollama</b> (Self-hosted Inference)</li>
    </ul>
  </div>
  <div class="bg-gray-800 bg-opacity-50 p-6 rounded-xl border border-pink-500 hover:border-cyan-500 transition-colors shadow-[0_0_20px_rgba(255,0,127,0.1)]">
    <h2 class="text-pink-400 mb-4 border-b border-gray-700 pb-2">📊 Observability (LLMOps)</h2>
    <ul>
      <li><b>OpenTelemetry</b> (Traces & Tokens)</li>
      <li><b>OpenObserve</b> (Logs/Traces/Metrics)</li>
      <li><b>Langfuse / Arize</b> (GenAI specific)</li>
      <li><b>Prometheus & Grafana</b></li>
    </ul>
  </div>
</div>

<style>
  li {
    font-size: 1.45rem;
    line-height: 1.2;
    margin-bottom: 0.8em;
    text-align: left;
  }
  </style>

---
layout: center
class: text-center
---

# 💻 Output

<div class="text-2xl mt-4 text-gray-300">Let's see the end result</div>
<div class="text-xl mt-2 mb-4 text-center text-cyan-300">
And not 'Kyu, kaha, kaise'
</div>


<div class="mt-8 p-6 bg-gray-900 rounded-2xl border border-cyan-500 inline-block shadow-[0_0_30px_rgba(0,229,255,0.2)] transform hover:scale-105 transition-transform duration-300">
  <img src="/kong_auth/kong_auth.png" alt="QR Code" class="w-48 h-48 mx-auto rounded-lg">
  <div class="mt-6">
    <a href="https://github.com/susmitpy/docker-kong-fastapi-otel-openobserve" class="text-xl font-mono text-cyan-400 hover:text-pink-400 transition-colors">
      Scan for GitHub Repo
    </a>
  </div>
</div>

---
src: ./pages/forquiz.md
---

---

# 🔑 Key Takeaway #1


<v-click>

<div class="mt-12 flex flex-col gap-10 px-8">

<div class="bg-gray-800 bg-opacity-40 p-8 rounded-xl border-l-4 border-cyan-500 shadow-[0_0_20px_rgba(0,229,255,0.1)]">
  <div class="text-4xl mb-4 font-bold">
    <span class="text-cyan-400">Fundamentals</span> <span class="text-white">&gt;</span> <span class="text-pink-400">Syntax</span>
  </div>
  <div class="text-2xl mt-4 text-gray-400 font-mono">
    for vs while ≠ fundamental
  </div>
  <div class="text-3xl mt-4">
    <span class="text-white">Understanding</span> <span class="text-cyan-400">iteration</span> <span class="text-white">+</span> <span class="text-pink-400">mutation</span> <span class="text-white">=</span> <span class="text-cyan-400 font-bold">fundamental</span>
  </div>
</div>

</div>

</v-click>



---

# 🔑 Key Takeaway #2

<div class="mt-12 flex flex-col gap-10 px-8">

<v-click>


<div class="bg-gray-800 bg-opacity-40 p-8 rounded-xl border-l-4 border-pink-500 shadow-[0_0_20px_rgba(255,0,127,0.1)]">
  <div class="text-4xl mb-4 font-bold">
    <span class="text-pink-400">HI</span> <span class="text-white">&gt;&gt;</span> <span class="text-cyan-400">AI</span>
  </div>
  <div class="text-2xl mt-4 text-gray-400 font-mono">
    "Is my architecture solid?" ≠ valid prompt
  </div>
  <div class="text-3xl mt-4">
    <span class="text-white">There is no "solid". Architecture is about</span> <span class="text-pink-400 font-bold">trade-offs</span> <span class="text-white">requiring</span> <span class="text-cyan-400 font-bold">conceptual knowledge</span> <span class="text-white">&</span> <span class="text-yellow-400 font-bold">practicality</span><span class="text-white">.</span>
  </div>
</div>

</v-click>

</div>

---

# 🔑 Key Takeaway #3

<v-click>

<div class="grid grid-cols-2 gap-8 px-4 items-center">

  <div class="relative transform hover:scale-105 transition-transform duration-500">
    <div class="absolute inset-0 bg-gradient-to-tr from-cyan-500 to-pink-500 rounded-xl blur opacity-30"></div>
    <img src="/steve_components.jpeg" alt="Steve Jobs Component Art" class="relative rounded-xl border border-gray-600 shadow-[0_0_20px_rgba(0,229,255,0.2)] object-cover h-[400px] w-full" />
  </div>

  <div class="bg-gray-800 bg-opacity-40 p-8 rounded-xl border-r-4 border-cyan-500 shadow-[0_0_20px_rgba(0,229,255,0.1)] flex flex-col justify-center">
    <div class="text-3xl mt-2 text-gray-300 font-serif italic mb-6">
      "AI connects existing dots. Humans create new ones."
    </div>
    <div class="text-2xl mb--10 leading-snug">
      <span class="text-white">An LLM sees hardware as compute power. It takes </span> <span class="text-cyan-400 font-bold">human curiosity</span> <span class="text-white"> and out-of-the-box </span> <span class="text-yellow-400 font-bold">Jugaad</span> <span class="text-white"> to look at e-waste and create a </span> <span class="text-pink-400 font-bold italic">Jakaas</span> <span class="text-white"> masterpiece.</span>
    </div>

  </div>

</div>

</v-click>

---

# 🔑 Key Takeaway #4

<div class="mt-12 flex flex-col gap-10 px-8">

<v-click>

<div class="text-center text-5xl font-extrabold mt-8 p-8">
  <span class="text-pink-400">AI is learning,</span><br/>
  <span class="text-cyan-400 mt-4 inline-block">Are you ?</span>
</div>

</v-click>

</div>

---
src: ./pages/connect.md
---


---
src: ./pages/qa.md
---