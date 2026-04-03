---
theme: seriph
class: text-center
duration: 30

title: "Abstracting Cross-Cutting Concerns: AuthN/Z and Observability at the Edge"
info: |
  ## Live Demo
drawings:
  persist: false
transition: slide-left
mdc: true
background: /bg_image.png
---

# Abstracting Cross-Cutting Concerns 

<hr/>

<br/>

<span class="text-4xl"> AuthN/Z and Observability </span>

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

* **[20 min] Core Concepts:** API Gateways, AuthN/Z, and Observability
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

# The Problem: Microservice Sprawl

<div class="text-xl mt-4">
Managing complexity of cross-cutting concerns.
</div>

* **Duplication of Effort:** Implementing Auth logic, JWT validation, and Telemetry in every single service.
* **Language-Agnostic Nightmares:** Maintaining consistent middleware across Python, Go, Node.js, and Java.
* **Security Risks:** Higher chance of misconfiguration and inconsistent security policies.
* **Tight Coupling:** Business logic becomes intertwined with infrastructure concerns.

<style>
  li {
    font-size: 1.8rem;
    line-height: 1.5;
    margin-bottom: 0.8em;
    text-align: left;
  }
  .text-2xl {
    margin-bottom: 1.5em;
  }
</style>

---

# Anatomy of an API Gateway

<div class="text-3xl mt-4 text-center">
An API Gateway acts as a single entry point, abstracting away the backend architecture.
</div>

```mermaid
graph LR

C[Client]
B[Backend]

subgraph API Gateway
    R[Ingress Routes]
    S[Logical Services]
    U[Upstream Load Balancing]

    R --> S --> U
end

C -->|Request| R
U -->|Request| B
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

# Anatomy of an API Gateway

## Ingress Routes

<div class="text-3xl mt-2 mb-8 text-center">
Mapping external requests to internal logical boundaries.
</div>

```mermaid
graph LR

U[User] -->|PUT| UPR(/api<u>/users</u>/profile) --> |Mapped to| UR[User Route]

U --> |GET| UOR(/api<u>/orders</u>) --> |Mapped to| OR[Order Route]
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

# Anatomy of an API Gateway

## Logical Services

<div class="text-3xl mt-2 mb-8 text-center">
Defining abstract backend components independent of physical locations.
</div>

```mermaid
graph LR

U[User] -->|Request| UR[User Route]

U --> |Request| OR[Order Route]

UR --> |Mapped to| US[User Service]
OR --> |Mapped to| OS[Order Service]
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

# Anatomy of an API Gateway

## Upstream Load Balancing

<div class="text-3xl mt-2 mb-8 text-center">
Managing physical targets and health checks for logical services.
</div>

```mermaid
graph LR

U[User] -->|Request| US[User Service]

U --> |Request| OS[Order Service]

US --> |Mapped to| UU[User Upstream]
OS --> |Mapped to| OU[Order Upstream]
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

# Anatomy of an API Gateway

## Upstream Targets

<div class="text-3xl mt-2 mb-8 text-center">
Routing to the actual compute instances running the code.
</div>

```mermaid
graph LR

U[User] -->|Request| UU[User Upstream]

U --> |Request| OU[Order Upstream]

UU --> |Forward| UT1[Target Instance 1]

OU --> |Forward| OT1[Target Instance 1]
OU --> |Forward| OT2[Target Instance 2]
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 4em;
        scale: 1.5;
    }
</style>

---

# Authentication vs Authorization

<div class="text-3xl mt-4 mb-6">
Who are you vs. What can you do?
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

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Auth Service
    participant G as API Gateway

    C->>A: 1. Login (User / Pass)
    A-->>C: 2. Return JWT (Signed)
    C->>G: 3. Request + Header: Bearer <JWT>
    Note over G: 4. Verify Signature & Expiry
    G-->>C: 5. Return Protected Data
```

<style>
  .mermaid {
    display: flex;
    justify-content: center;
    margin-bottom: 1em;
    scale: 1.1;
  }
</style>

---

# Anatomy of an API Gateway

## The Middleware/Plugin Pattern

<br/>

```mermaid
graph LR

C[Client]
B[Backend]

subgraph API Gateway
    subgraph Route Scope
      RPL1[Auth Validation]
      RPL2[Rate Limiting]

      RPL1 --> RPL2
    end
    subgraph Service Scope
      SPL1[Header Injection]
      SPL2[Tracing]

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

# Claim-to-Header Injection

```mermaid
sequenceDiagram
    participant C as Client
    participant G as API Gateway
    participant B as Backend Service

    C->>G: Request with JWT
    Note over G: Validates JWT signature<br/>Extracts 'sub' claim
    G->>B: Forward Request<br/>Header: auth-user-identifier=123
    Note over B: Trusts header<br/>Executes business logic
    B-->>C: Response
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

# Observability

<div class="text-3xl mt-4 mb-6">
Gaining visibility into the black box.
</div>

<v-clicks>

* **Logs:** Discrete events (e.g., "Request failed with 500").
* **Metrics:** Aggregated data (e.g., "Latency is 50ms", "Error rate is 2%").
* **Traces:** Journey of a request across distributed systems.
* **Gateway Advantage:** The Gateway is perfectly positioned to generate baseline metrics and initiate distributed traces (OpenTelemetry) before traffic even hits your services.

</v-clicks>

<style>
  li {
    font-size: 1.7rem;
    line-height: 1.5;
    margin-bottom: 0.8em;
    text-align: left;
  }
</style>

---

# Containerization & Networking

* **Docker Containers:** Package the application code and dependencies, ensuring consistent execution.

<v-clicks>

* **Docker Networks:** Virtual networks that allow containers to communicate securely.
* **Gateway Networking:**
    * Gateway sits on an "external" network.
    * Backends sit on "internal" networks.
    * The Gateway bridges the gap, enforcing that clients *must* pass through it to reach the backends.

</v-clicks>

<style>
  li {
    font-size: 1.7rem;
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

# Kubernetes: Ingress & API Gateway

```mermaid
graph TD
    Client[Client] -->|External IP| LB[Cloud Load Balancer]
    LB --> IGW[Ingress Controller / API Gateway]

    subgraph Kubernetes Cluster
        IGW -->|/users| SvcU[User Service]
        IGW -->|/orders| SvcO[Order Service]

        SvcU --> P_U1[User Pod 1]
        SvcU --> P_U2[User Pod 2]
        SvcO --> P_O1[Order Pod 1]
    end
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: -1.7em;
        scale: 0.95;
    }
</style>

---

# Kubernetes: Service Mesh

```mermaid
graph LR
    subgraph Pod A
        AppA[Service A] <--> ProxyA((Sidecar Proxy))
    end
    
    subgraph Pod B
        ProxyB((Sidecar Proxy)) <--> AppB[Service B]
    end
    
    ProxyA <-->|mTLS, Traffic Mgmt, AuthZ| ProxyB
    
    CP{Control Plane} -.->|Config & Policies| ProxyA
    CP -.->|Config & Policies| ProxyB
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 5em;
        scale: 1.2;
    }
</style>

---

# The Open-Source Landscape

<div class="text-2xl mt-2 mb-4 text-center">
Abstracting these concerns is a community-wide effort.
</div>

<div class="grid grid-cols-2 gap-8 mt-4">
  <div>
    <h2>API Gateways</h2>
    <ul>
      <li><b>Envoy Proxy</b> (Istio, Gloo)</li>
      <li><b>Kong API Gateway</b></li>
      <li><b>Apache APISIX</b></li>
      <li><b>Tyk</b></li>
    </ul>
  </div>
  <div>
    <h2>Observability</h2>
    <ul>
      <li><b>OpenTelemetry</b> (The standard)</li>
      <li><b>Prometheus</b> (Metrics)</li>
      <li><b>Jaeger</b> (Tracing)</li>
      <li><b>OpenObserve</b> (Logs/Traces/Metrics)</li>
      <li><b>Grafana</b> (Visualization)</li>
    </ul>
  </div>
</div>

<style>
  h2 {
    font-size: 2.2rem !important;
    margin-bottom: 1rem !important;
    text-align: left;
  }
  li {
    font-size: 1.6rem;
    text-align: left;
    margin-bottom: 0.6em;
  }
</style>

---

# Let's see these concepts in action via an open-source stack

<h2>API Gateway with FastAPI, OpenTelemetry and OpenObserve in Docker </h2>

<div class="flex justify-between mt-6">
  <div class="text-2xl break-words w-1/2 pl-1 flex items-center">
    <a href="https://github.com/susmitpy/docker-kong-fastapi-otel-openobserve">https://github.com/susmitpy/docker-kong-fastapi-otel-openobserve</a>
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

## We both are from DG Ruparel College, Mumbai
<br/>
<div class="flex">
  <div class="w-7/10 pr-4">
    <SlidevVideo autoplay>
      <source src="/ruparel meme.mp4" type="video/mp4" />
    </SlidevVideo>
  </div>
  <div class="w-3/10">
    <img src="/ruparel_selfie.jpeg"/>
  </div>
</div>

---
src: ./pages/qa.md
---