---
theme: seriph
class: text-center
duration: 30

title: "Abstracting Cross-Cutting Concerns: AuthN/Z and Observability at the Edge"
info: |
  ## Concepts and Demo
drawings:
  persist: false
transition: slide-left
mdc: true
background: /bg_image.png
---

# Abstracting Cross-Cutting Concerns 

<hr/>

<br/>

<span class="text-4xl"> AuthN/Z and Observability at the GenAI Edge </span>

<br/>

### By Susmit Vengurlekar (@susmitpy)

---
src: ./pages/disclaimer.md
---

---
src: ./pages/bug.md
---

---
src: ./pages/about.md
---

---
src: ./pages/ice_breaker.md
---

---

# Agenda

<div class="text-3xl mt-12 mb-6">
How we'll spend our ~ 30 minutes together:
</div>

<v-clicks>

* **[20 min] Core Concepts & GenAI:** API / AI Gateways, AuthN/Z, and LLM Observability
* **[5 min] Demo:** Seeing it in action (Kong, FastAPI, OpenObserve)
* **[5 min] Q & A:** Your questions

</v-clicks>

<style>
  li {
    font-size: 2rem;
    line-height: 1.8;
    margin-bottom: 0.8em;
    text-align: left;
  }
</style>

---

# The Problem: Microservice & GenAI Sprawl

<div class="text-xl mt-4">
Building a single-tenant GenAI app is easy. Scaling it to production is hard.
</div>

* **The Single-Tenant Trap:** GenAI without AuthN/Z (multi-tenancy) leads to untracked costs and "bill shock". You cannot rate-limit or bill what you cannot attribute.
* **The Black Box:** Without observability, an LLM agent stuck in a loop or hallucinating is impossible to debug.
* **Duplication of Effort:** Implementing Auth, JWT validation, and Token Tracking in every single service or AI script.
* **Tight Coupling:** Hardcoding LLM providers (OpenAI, Anthropic) vs. self-hosted GPU inferences directly into business logic.

<style>
  li {
    font-size: 1.6rem;
    line-height: 1.5;
    margin-bottom: 0.8em;
    text-align: left;
  }
  .text-2xl {
    margin-bottom: 1.5em;
  }
</style>

---

# Anatomy of a Gateway (API & AI)

<div class="text-3xl mt-4 text-center">
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

# Anatomy of a Gateway

## Ingress Routes

<div class="text-3xl mt-2 mb-8 text-center">
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

# Anatomy of a Gateway

## Logical Services

<div class="text-3xl mt-2 mb-8 text-center">
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
        scale: 1.8;
    }
</style>

---

# Anatomy of a Gateway

## Upstream Load Balancing (The GenAI Split)

<div class="text-3xl mt-2 mb-6 text-center">
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
        scale: 1.3;
    }
</style>

---

# Authentication vs Authorization in GenAI

<div class="text-3xl mt-4 mb-6">
Identity, Access, and Cost Allocation.
</div>

<v-clicks>

* **Authentication (AuthN):** Verifying identity.
    * *Example:* Checking a password, validating a JWT signature.
    * *Gateway Role:* Ideal. Validate tokens centrally.

* **Authorization (AuthZ):** Determining permissions.
    * *Example:* Can user X view record Y? Can POST to /payments to create payment ?
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

# The JWT Lifecycle
Gateway Role:* Validate JWT centrally. If token is invalid, drop the request before hitting expensive GPU instances.

* **Authorization (AuthZ) & Multi-Tenancy:**
    * *Standard:* Can user X view record Y?
    * *GenAI:* Is this tenant allowed to use the `GPT-4` route, or only `Llama-3-8B`? Are they within their **token rate-limit** quota? 
    * *Security:* AuthZ prevents one compromised tenant from exhausting your entire organization's LLM API budget.

</v-clicks>

<style>
  li {
    font-size: 1.6rem;
    line-height: 1.4;
    margin-bottom: 0.6em;
    text-align: left;
  }
  ul ul li {
      font-size: 1.35rem;
      color: var(--slidev-theme-foreground);
      opacity: 0.9;
  }
</style>

---

# The Middleware/Plugin Pattern

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

# Claim-to-Header Injection (Tenant Allocation)

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

# Observability (LLMOps)

<div class="text-3xl mt-4 mb-6">
Gaining visibility into the GenAI black box.
</div>

<v-clicks>

* **Logs:** Not just errors. Tracking prompts, responses, and tool outputs (with PII masking at the gateway).
* **Metrics (The GenAI Additions):** 
    * *Latency:* **TTFT** (Time to First Token) vs Total Generation Time.
    * *Usage:* Input Tokens, Output Tokens, Cost per Tenant.
* **Traces:** Journey of a request across distributed systems. Crucial for debugging slow RAG pipelines or erratic Agents.
* **Gateway Advantage:** The Gateway initiates the distributed trace (OpenTelemetry) and standardizes token metrics regardless of whether the backend is OpenAI or a self-hosted GPU.

</v-clicks>

<style>
  li {
    font-size: 1.55rem;
    line-height: 1.5;
    margin-bottom: 0.8em;
    text-align: left;
  }
</style>

---

# Tracing Agents & Sandboxes

<div class="text-xl mt-2 mb-4 text-center">
Distributed tracing (OpenTelemetry) makes complex Agent loops observable.
</div>

```mermaid
gantt
    dateFormat  s
    axisFormat  %S
    title OpenTelemetry Trace: Agent execution
    
    section Gateway
    Inbound Request (API)        :a1, 0, 10s
    
    section Orchestrator
    Agent Planning               :a2, 1, 2s
    
    section LLM / GPU Node
    LLM: Reason & Select Tool    :a3, 2, 4s
    LLM: Synthesize Output       :a6, 8, 10s
    
    section Code Sandbox
    Spin up Container            :a4, 4, 5s
    Execute Python Tool          :a5, 5, 8s
```

<div class="mt-4 text-sm opacity-80 text-center">
<b>Span Attributes attached:</b> Agent ID, Tool Name, Container ID, Host Instance, Token Count, Latency.
</div>

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 1em;
        scale: 1;
    }
</style>

---

# Containerization & Isolation

* **Docker Containers:** Package the application code, ensuring consistent execution.

<v-clicks>

* **GenAI Sandboxing:** 
    * Agents that write and execute code *must* do so in isolated, ephemeral sandbox containers (without network access to your DB!).
* **Gateway Networking Strategy:**
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

# The Open-Source Landscape

<div class="text-2xl mt-2 mb-4 text-center">
Abstracting these concerns is a community-wide effort.
</div>

<div class="grid grid-cols-2 gap-8 mt-4">
  <div>
    <h2>Gateways & Orchestration</h2>
    <ul>
      <li><b>Kong API Gateway / LiteLLM</b></li>
      <li><b>Envoy Proxy</b> (Istio, Gloo)</li>
      <li><b>vLLM / Ollama</b> (Self-hosted Inference)</li>
    </ul>
  </div>
  <div>
    <h2>Observability (LLMOps)</h2>
    <ul>
      <li><b>OpenTelemetry</b> (Traces & Tokens)</li>
      <li><b>OpenObserve</b> (Logs/Traces/Metrics)</li>
      <li><b>Langfuse / Arize</b> (GenAI specific)</li>
      <li><b>Prometheus & Grafana</b>/docker-kong-fastapi-otel-openobserve">https://github.com/susmitpy/docker-kong-fastapi-otel-openobserve</a>
  </div>
  <div class="w-1/2 flex ml-5 items-center">
    <img src="/kong_auth/kong_auth.png" alt="QR Code">
  </div>
</div>

---

<div class="flex flex-col h-full">
<h1>Demo</h1>
<Youtube id="KHkabnbNmHQ" class="mx-auto my-auto w-full h-full p-4"/>
</div>

---
src: ./pages/connect.md
---


---
src: ./pages/qa.md
---