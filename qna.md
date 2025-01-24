---
theme: seriph
class: text-center

title: QnA on Private Knowledge Graph using Neo4j
info: |
  ## RAG pipeline
drawings:
  persist: false
transition: slide-left
mdc: true
background: /bg_image.png
---

# QnA on Private Knowledge Graph using Neo4j

### By Susmit Vengurlekar


<div class="text-xs text-gray-400 absolute bottom-10 left-0 right-0 text-center">
Gentle Reminder: Start screen recording
</div>


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

# Agenda

* What is LLM ?
* What is RAG ?
* What is a Knowledge Graph?
* Intro to Neo4j
* Demo Time
  - Asking questions to LLM
  - Setting up RAG based pipeline
  - Asking questions to RAG + LLM

<style>
  li {
    font-size: 1.8rem;
  }
</style>

--- 

# What is LLM ?

- LLM is a Language Model that is trained on a large corpus of text data
- It works by predicting the next token given a sequence of tokens in a recursive manner

### Example

- Input sequence: "The quick brown"
- Predict next token: "fox"
- Updated sequence: "The quick brown fox"
- Predict next token: "jumps"
- Repeat the process

Stop when output length reaches a certain threshold or a special token is predicted

<style>
  li {
    font-size: 1.5rem;
  }
  p {
    font-size: 1.3rem;
  }
</style>

--- 

# What is RAG ?

* RAG stands for Retrieval Augmented Generation
* It is used to get more context to feed into LLM

```mermaid
graph LR

DS[Data Source]
Q[User Query]
RAG[RAG]
LLM[LLM]


Q --> RAG
RAG --> |1. Fetch Information from| DS
RAG --> |2. Enriched User Query| LLM
```

<style>
  li {
    font-size: 2rem;
  }
</style>

---

# What is a Knowledge Graph?

- A Knowledge Graph is a graph database that stores information in the form of nodes and edges
- Nodes represent entities and edges represent relationships between entities
- Properties can be attached to nodes and edges

### Example

```mermaid
graph LR
    P[("Person {Name: 'Susmit'}")]
    PL[("Programming Language {Name: 'Python'}")]
    
    P -->|"Knows {Since: 2016}"| PL
```

<style>
  li {
    font-size: 1.5rem;
  }
</style>

---

# Intro to Neo4j

- Graph database
- Labels, Nodes, Relationships, and Properties
- Native Graph Storage: Store data using pointers on disk
- Cypher Query Language
- Create only directed relationships, but traverse them any way.

<img src="/mongo/neo_intro.png" class="w-3/4" style="background:white"/>

<style>
    li {
        font-size: 1em;
    }
</style>

---

# Demo Time

- Asking questions to LLM
- Setting up RAG based pipeline
- Asking questions to RAG + LLM

---
src: ./pages/connect.md
---

---
src: ./pages/qa.md
---
