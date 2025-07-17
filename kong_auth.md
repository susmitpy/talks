---
theme: seriph
class: text-center

title: Auth with Gateway
info: |
  ## Live Demo
drawings:
  persist: false
transition: slide-left
mdc: true
background: /bg_image.png
---

# Auth with Kong API Gateway

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

# Dissecting Kong API Gateway

```mermaid
graph LR

C[Client]
B[Backend]

subgraph Kong API Gateway
    R[Route]
    S[Service]
    U[Upstream]

    R --> S --> U
end

C -->|Request| R
U -->|Request| B
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 7em;
        scale: 1.3;
    }
</style>


---

# Dissecting Kong API Gateway

## Routes

<br/>

```mermaid
graph LR

U[User] -->|PUT| UPR(/api<u>/users</u>/profile) --> |Mapped to| UR[User Route]

U --> |GET| UOR(/api<u>/orders</u>) --> |Mapped to| OR[Order Route]
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 4em;
        scale: 1.6;
    }
</style>

---

# Dissecting Kong API Gateway

## Services

<br/>

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
        margin-top: 4em;
        scale: 1.6;
    }
</style>

---

# Dissecting Kong API Gateway

## Upstreams

<br/>

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
        margin-top: 4em;
        scale: 1.6;
    }
</style>

---

# Dissecting Kong API Gateway

## Upstream Targets

<br/>

```mermaid
graph LR

U[User] -->|Request| UU[User Upstream]

U --> |Request| OU[Order Upstream]

UU --> |Forward| UT1[User Target 1]

OU --> |Forward| OT1[Order Target 1]
OU --> |Forward| OT2[Order Target 2]
```

<style>
    .mermaid {
        display: flex;
        justify-content: center;
        margin-top: 4em;
        scale: 1.6;
    }
</style>


---

# Dissecting Kong API Gateway

## Plugins

<br/>

```mermaid
graph LR

C[Client]
B[Backend]

subgraph Kong API Gateway
    subgraph Route
      RPL1[Plugin 1]
      RPL2[Plugin 2..n]

      RPL1 --> RPL2
    end
    subgraph Service
      SPL1[Plugin 1]
      SPL2[Plugin 2..n]

      SPL1 --> SPL2
    end
    U[Upstream]

    Route --> |Mapped to| Service --> |Mapped to| U
end

C --> Route
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

# Let's Explore someone's Side Project

<h2>Kong API Gateway with Fast API, Open Telemetry and OpenObserve in Docker </h2>


<div class="flex justify-between mt-6">
  <div class="text-2xl break-words w-1/2 pl-1 flex items-center">
    <a href="https://github.com/susmitpy/docker-kong-fastapi-otel-openobserve">https://github.com/susmitpy/docker-kong-fastapi-otel-openobserve</a>
  </div>
  <div class="w-1/2 flex ml-5 items-center">
    <img src="/kong_auth/kong_auth.png" alt="QR Code">
  </div>
</div>

---
src: ./pages/connect.md
---

---

# Common between me and previous speaker (Amandeep)

* Talked about Kong

* Both of us are from India

* Both of us are not engineers (by degree)

<v-click>

## There is one more thing in common, raise your hand if you know what it is

</v-click>

<style>
  li {
    font-size: 1.8rem;
  }
</style>

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
