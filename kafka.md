---
theme: seriph
class: text-center

title: Kafka 1o1
info: |
  ## Introduction to Apache Kafka
drawings:
  persist: false
transition: slide-left
mdc: true
background: /bg_image.png
---

# Kafka 1o1

### By Susmit Vengurlekar

---

<div class="flex flex-col h-full justify-center items-center gap-15">
  <h1 class="text"> Light attracts Bugs </h1>
  <h1 class="text" v-click> Dark Mode is better </h1>
</div>

<style>
  .text {
    color: #ffffff;
    font-size: 4.5em;

  }
</style>

---
src: ./pages/about.md
---


---

# Agenda

<v-switch>
<template #0>

1. What is Kafka?
2. Use Cases
3. Where does Kafka fit in?
4. Components in Kafka 
5. Kafka <> Confluent
</template> 

<template #1>

1. What is Kafka?
2. Use Cases
3. Where does Kafka fit in?
4. Components in Kafka
    - Publishers 
    - Brokers
        - Topics
        - Partitions
        - Partition Replication
    - Zookeeper / KRaft
    - Consumers
5. Kafka <> Confluent
</template>

<template #2>

1. What is Kafka?
2. Use Cases
3. Where does Kafka fit in?
4. Components in Kafka 
    - Publishers
    - Brokers
        - Topics, Partitions, Partition Replication
    - Zookeeper / KRaft
    - Consumers
        - Queue Behaviour
        - Pub-Sub Behaviour
5. Kafka <> Confluent

</template>
</v-switch>


---

# What is  Kafka ?

<div class="flex flex-row items-center h-3/4 gap-2">
  <img src="/kafka/iot.webp" class="w-1/3 h-3/4"/>
  <img src="/kafka/pipe.png" class="w-1/3 h-3/4" v-click='2'/>
  <img src="/kafka/cassandra.webp" class="w-1/3 h-3/4" v-click/>
</div>

---
layout: image-left

image: /kafka/logo.png

class: content
---

# What is Kafka ?

<v-clicks>

- open-source distributed event streaming platform
- Can act like a Pub-Sub system
- Can also act like a message queue
- Fault Tolerant & Scalable

</v-clicks>

<style>
  .content {
    li {
      font-size: 1.5em;
    }
  }
</style>

---

# (Some) Use Cases

<v-clicks>

- Log Aggregation
- Event Sourcing
- Stream Processing

</v-clicks>

<style>
    li {
      font-size: 2em;
    }

</style>

---

# Where  does Kafka fit in?

<div class="flex items-center justify-center">
  <img src="/kafka/fit_in.svg" class="w-2.6/4"/>
</div>


---
layout: cover
---

# Components in 
# Kafka

---

# Publishers

```ts
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'my-producer',
  brokers: ['localhost:9092'], // Replace with your broker addresses
});

const producer = kafka.producer();

const run = async () => {
  // Connect the producer
  await producer.connect();

  // Send a message
  await producer.send({
    topic: 'test-topic',
    messages: [
      { value: 'Hello Kafka from TypeScript!' },
    ],
  });

  // Disconnect the producer
  await producer.disconnect();
};
```

---

# Brokers, Topics

<div class="flex items-center justify-center">
<img src="/kafka/topics.svg" class="w-3/4"/>
</div>

---

# Partitions

<div class="flex items-center justify-center">
<img src="/kafka/partitions.svg" class="w-1/2.5"/>
</div>

---

# Partition Replication

<div class="flex items-center justify-center">
<img src="/kafka/replication.svg" class="w-5/6"/>
</div>

--- 
transition: fade-out
---

# Operations

<v-clicks>

1. Partition Leader Election and Managing Replicas
2. Metadata Management (Brokers, Topics, Partitions)
3. Maintaining the ISR (In Sync Replicas) list

</v-clicks>

<div v-click v-motion
  :initial="{ x: -50 }"
  :enter="{ x: 0 }"
  :leave="{ x: 50 }"
  class = "flex items-center justify-center"
>
  <img src="/kafka/zookeeper.png" class="w-1/2"/> 
</div>

<style>
    li {
      font-size: 2em;
    }

</style>

---
layout: image
image: /kafka/mind.webp
backgroundSize: contain
---

---

# Apache Kafka Raft (KRaft) Consensus Protocol

- Some brokers as Controller Nodes, leader election
- Raft Consensus Protocol
- Metadata stored in a distributed log 

<style>
    li {
      font-size: 2em;
    }
</style>

---

# Consumers

```ts {maxHeight:'100px'}
import { Kafka } from 'kafkajs';
const kafka = new Kafka({
  clientId: 'my-consumer',
  brokers: ['localhost:9092'],
});
const consumer = kafka.consumer({ groupId: 'test-group' });
const run = async () => {
  await consumer.connect();
  console.log('Consumer connected');

  await consumer.subscribe({ topic: 'test-topic', fromBeginning: false });
  console.log('Subscribed to topic');

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log({
        topic,
        partition,
        offset: message.offset,
        value: message.value?.toString(),
      });
      // Process message and optionally commit the offset
      // Committing the offset is automatic unless you disable autoCommit in consumer settings
    },
  });
};
```

---

# Consumers

<div class="flex items-center justify-center">
<img src="/kafka/single_consumer.svg" class="w-full"/>
</div>

---

# Consumer on Bench

<div class="flex items-center justify-center">
<img src="/kafka/no_work.svg" class="w-full"/>
</div>

---

# Multiple Consumer Groups

<div class="flex items-center justify-center">
<img src="/kafka/multi_cg.svg" class="w-2.4/4"/>
</div>

---

# Partition Level Queue

<div class="flex items-center justify-center">
<img src="/kafka/queue.svg" class="w-5/6"/>
</div>

---

# Pub Sub

<div class="flex items-center justify-center">
<img src="/kafka/pub_sub.svg" class="w-2.4/4"/>
</div>

--- 

# Kafka <> Confluent

<v-clicks>

* Founded by original creators of Apache Kafka
* Foundational Platform for data-in-motion 
* Confluent Control Center
* Optimized Kafka Distribution
* Cloud Native Apache Flink in GA (19<sup>th</sup> March, 2024)

</v-clicks>

<style>
    li {
      font-size: 2em;
    }

</style>


---
src: ./pages/connect.md
---

---
src: ./pages/qa.md
---
