---
theme: seriph
class: text-center

title: Tracking Changes with MongoDB Change Stream
info: |
    ## With Live Demo
drawings:
    persist: false
transition: slide-left
mdc: true
background: /bg_image.png
---

# Tracking Changes with MongoDB Change Stream

### By Susmit Vengurlekar (@susmitpy)

---
src: ./pages/bug.md
---

---
src: ./pages/disclaimer.md
---

---
src: ./pages/about.md
---

---

# Agenda

1. What is a Stream 
2. Change Data Capture
3. Intro to MongoDB
4. Intro to MongoDB Change Stream
5. Intro to Kafka
6. Intro to Neo4j
7. ⁠Intro to Kafka Connect
8. One Use Case
9. Live Demo
10. Q&A 

<style>
    li {
        font-size: 1.3em;
    }
</style>

---

# What is a Stream

- A sequence of data elements made available over time
- Flow of data from one point to another

<br/>

```mermaid
graph LR
    A[Source] --> B[Stream]
    B --> C[Sink]
```

<style>
    li {
        font-size: 1.5em;
    }
</style>

---

# Change Data Capture (CDC)

- Capturing changes in data as they occur
- Capturing inserts, updates, and deletes

<br/>

```mermaid
graph LR

    A[Client] --Create Order--> B[(DB)]
    B --Change Stream--> C[Listener]
    C --> D(Do Something)
```

<style>
    li {
        font-size: 1.5em;
    }
</style>



---

# Intro to MongoDB

- Does not need introduction 

<v-click>

- Document-oriented NoSQL database
- Schema On Read
</v-click>

<style>
    li {
        font-size: 1.5em;
    }
</style>

---

# Intro to MongoDB Change Stream

- Real-time data changes
- Can be consumed by applications
- Capture inserts, updates, and deletes

<style>
    li {
        font-size: 1.5em;
    }
</style>

---

# Intro to Kafka

- open-source distributed event streaming platform which is Fault Tolerant & Scalable
- Can act like a Pub-Sub system as well as a message queue

<div class="flex items-center justify-center">
  <img src="/kafka/fit_in.svg" class="w-2.5/5"/>
</div>

<style>
    li {
        font-size: 1.2em;
    }
</style>

---

# Intro to Neo4j

- Graph database
- Labels, Nodes, Relationships, and Properties
- Native Graph Storage: Store data using pointers on disk
- Cypher Query Language

<img src="/mongo/neo_intro.png" class="w-3/4" style="background:white"/>

<style>
    li {
        font-size: 1.2em;
    }
</style>

---

# Intro to Kafka Connect

- Tool for scalably and reliably streaming data between Apache Kafka and other data systems
- Connectors for various data sources and sinks
- Kafka Connect workers are JVM processes

<br/>

```mermaid
graph LR

 A[Source] -- Data --> B[Kafka Connect - Source Connector]
 B -- Act as a Producer --> C[Kafka]
 D[Kafka Connect - Sink Connector] -- Data --> E[Sink]
 D -- Act as a Consumer --> C
```
<style>
    li {
        font-size: 1.2em;
    }
</style>

---

# E-commerce Use Case

- Primary Data Store: MongoDB
- Data Store for Recommendations: Neo4j
- But then, we can listen for changes and directly write to Neo4j, why Kafka?

<v-click>

- Decouple MongoDB and Neo4j
    - Data Buffer in case of spikes
    - Allows for downtime of Neo4j
    - Replayability
    - Can configure Dead Letter Queue for failed messages
    - One more thing
</v-click>

<v-click>

### Gave me a chance to setup slighly more complex demo and have more content in the talk

</v-click>

<style>
    li {
        font-size: 1.1em;
    }
</style>

---

# MongoDB to Kafka to Neo4j

```mermaid
graph LR

A[MongoDB] -- Change Stream --> B[Kafka Connect Worker - MongoDB Source Connector] --> C[Kafka] --> D[Kafka Connect Worker - Neo4j Sink Connector] --> E[Neo4j]
```

<br/> 
<v-click>

## Enough of Slides, Let's see some code, some configuration and get things working.
<br/>

<div class="flex flex-row gap-4">
<img src="/mongo/mongo_kafka_neo4j.png" width="250" height="250" />
<div class="flex flex-col">
<p> Scan the QR Code for the demo github repo</p>
<p>Github Repo: susmitpy/mongodb-kafka-neo4j</p>
</div>
</div>

</v-click>

---
src: ./pages/connect.md
---

---
src: ./pages/qa.md
---
