---
theme: seriph
class: text-center

title: Real-Time Click-Through Rate Analysis with Flink & Kafka
info: |
  ## Real-time computation of CTR from streaming impressions and clicks. PyFlink · Kafka · Go · Docker
drawings:
  persist: false
transition: slide-left
mdc: true
background: /bg_image.png
---

<style>
:root {
  /* IIT Bombay Inspired Theme */
  --iitb-blue: #004A99;
  --iitb-accent: #00e1ffff;
  --iitb-light: #f8f9fa;
  --iitb-dark: #001f3f;

  /* Theme Colors */
  --slidev-theme-primary: var(--iitb-light);
  --slidev-theme-secondary: var(--iitb-accent);
  --slidev-theme-accent: var(--iitb-accent);
  --slidev-theme-background: linear-gradient(135deg, var(--iitb-dark) 0%, #002b5c 100%);
  --slidev-theme-foreground: var(--iitb-light);
  --slidev-code-background: rgba(13, 17, 23, 0.95);
  --slidev-code-foreground: #f0f6fc;
}

.slidev-layout {
  background: var(--slidev-theme-background);
  color: var(--slidev-theme-foreground);
}

/* Headers */
h1, h2, h3, h4 {
  color: var(--iitb-light);
  font-weight: 600;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
}

h1 {
  color: #FFFFFF !important;
  border-bottom: 3px solid var(--iitb-accent);
  padding-bottom: 0.5rem;
  display: inline-block;
}

h2 {
  color: var(--iitb-accent);
}

/* General Text */
p, li {
  color: #e8e8e8;
  font-size: 1.25rem;
}

/* Links */
a {
  color: var(--iitb-accent);
  text-decoration: none;
  border-bottom: 2px solid var(--iitb-accent);
  transition: all 0.3s ease;
}

a:hover {
  color: #66b3ff;
  border-bottom-color: #66b3ff;
}

/* Code blocks */
pre {
  background: var(--slidev-code-background) !important;
  border: 2px solid var(--iitb-blue);
  border-radius: 8px;
}

/* Table styling */
table {
  width: 100%;
  background: rgba(0, 31, 63, 0.8);
  border-radius: 8px;
  overflow: hidden;
}

th {
  background: var(--iitb-blue);
  color: #FFFFFF;
  padding: 0.75rem;
}

td {
  padding: 0.75rem;
  border-top: 1px solid var(--iitb-blue);
}

/* Re-apply background image only on the first slide */
.slidev-layout.text-center {
  background: var(--slidev-theme-background);
}
</style>

<!-- Override style for the first slide -->
<div class="h-full flex flex-col justify-center items-center">
  <div style="color: white !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.8);">
    <h1 style="color: white !important; font-size: 3.5rem; font-weight: 700; border-color: white;">Real-Time Click-Through Rate Analysis with Flink & Kafka</h1>
    <h3 style="color: white !important; margin-top: 1.5rem;">By Susmit Vengurlekar</h3>
  </div>
</div>

<!---
1. "Hello everyone, and welcome. My name is Susmit Vengurlekar."
2. "Today, we're going to dive into a fascinating and highly practical topic: building a system for real-time Click-Through Rate analysis using some of the most powerful tools in the data streaming world: Apache Flink and Apache Kafka."
3. "We'll see how we can go from a continuous stream of user impressions and clicks to live, actionable business insights."
-->


---
src: ./pages/disclaimer.md
---

---
src: ./pages/about.md
---

---

# Agenda

<div class="grid grid-cols-2 gap-8 mt-8 text-left">
  <div>
    <ol class="text-xl space-y-2">
      <li>The Problem: Why CTR Matters</li>
      <li>Why Real-Time? Batch vs. Streaming</li>
      <li>Foundational Patterns: Queuing & Pub-Sub</li>
      <li>Introduction to Apache Kafka</li>
      <li>Kafka Architecture: Resilience & Parallelism</li>
      <li>Understanding Streams & Windows</li>
      <li>Introduction to Apache Flink</li>
      <li>Flink Architecture: How it Works</li>
    </ol>
  </div>
  <div>
    <ol class="text-xl space-y-2" start="9">
      <li>The Problem: Out-of-Order Events</li>
      <li>The Solution: Watermarks</li>
      <li>Handling Idle Streams</li>
      <li>Allowed Lateness</li>
      <li>System Architecture</li>
      <li>Components</li>
      <li>PyFlink Logic Walkthrough</li>
      <li>Demo</li>
      <li>Q&A</li>
    </ol>
  </div>
</div>
<!---
1. "Here's our roadmap for today. We'll start with the 'why' – understanding the business problem of CTR."
2. "Then, we'll build up our technical foundation, starting with core patterns like message queues and pub-sub, which will lead us directly into Apache Kafka."
3. "Next, we'll get into the heart of stream processing, talking about streams, windows, and how to handle the complexities of real-world data with Flink's watermarking system."
4. "Finally, we'll put it all together, look at the system architecture, walk through the code logic, and see a live demo. We'll wrap up with a Q&A."
-->

---

# The Problem: The Pulse of Advertising

## Why Every Second Counts

<div class="text-3xl font-bold p-6 my-8 bg-slate-800 rounded-lg border-2 border-cyan-400">
  CTR = (Clicks / Impressions) * 100%
</div>

<div class="text-3xl font-bold p-6 my-8">
  Businesses need real-time CTR to:

- 🚀 Optimize live campaigns
- 📉 Detect underperforming ads instantly
- 💰 Allocate budget effectively

</div>

<style>
  li, li * {
    font-size: 1.8rem;
  }
</style>

<!---
1. "So, what problem are we trying to solve? At the core of online advertising is a simple but vital metric: the Click-Through Rate, or CTR."
2. "It's the percentage of people who saw an ad (an impression) and actually clicked on it. The formula is simple: Clicks divided by Impressions."
3. "But the *timing* of this metric is critical. Businesses can't wait hours or days for this data. They need to know *right now* if a campaign is working to optimize ad spend, pull underperforming ads, and react to market changes instantly."
-->


---

# Why Real-Time? Batch vs. Streaming

<div class="grid grid-cols-2 gap-8 mt-12 text-center text-4xl">
  <div>
    <p class="text-6xl">🕒</p>
    <span class="mt-10 text-4xl">Batch Processing</span>
    <p class="text-2xl">The Past</p>
    <p class="text-2xl opacity-80">Delayed Insights (Hours)</p>
    <p class="text-2xl font-mono">"What happened?"</p>
  </div>
  <div>
    <p class="text-6xl">⚡</p>
    <span class="mt-10 text-4xl">Streaming Processing</span>
    <p class="text-2xl">The Present</p>
    <p class="text-2xl opacity-80">Live Feedback Loop (Seconds)</p>
    <p class="text-2xl font-mono">"What is happening now?"</p>
  </div>
</div>

<!---
1. "This need for immediacy highlights a fundamental shift in data processing."
2. "Historically, we used Batch Processing. We'd collect data over a period—like a day—and then run a big job overnight. This answers the question, 'What happened yesterday?' It's historical analysis."
3. "Streaming Processing, on the other hand, analyzes data as it arrives, moment by moment. It gives us a live feedback loop, answering the question, 'What is happening *right now*?' This allows us to be proactive instead of reactive."
-->


---
layout: two-cols-header
---

# Foundational Pattern: Message Queuing

## One-to-One Communication

::left::

<div class="mt-8 text-center">

```mermaid
graph TD
  Producer[Service A] --sends--> Queue[(Message Queue)];
  Queue --delivers--> Consumer[Service B];
```

</div>

::right::

<div class="mt-4 flex flex-col justify-center h-full">

<p class="text-3xl" style="line-height: 1.4;">
  <b>Analogy:</b> A Post Office Mailbox 
</p>
<p class="text-3xl" style="line-height: 1.4;">
  Decouples services. The sender doesn't need to wait for the receiver.
</p>

</div>

<style>
.two-cols-header {
  column-gap: 20px;
}
</style>

<!---
1. "To build a streaming system, we need a way for different services to communicate reliably. The first foundational pattern is the Message Queue."
2. "Think of it like a post office mailbox. A producer service sends a message to the queue and can immediately move on. It doesn't need to know if the consumer is ready or even online."
3. "Later, a consumer service comes and picks up the message. This decouples the services, making the whole system more resilient. It’s a one-to-one communication channel."
-->

---
layout: two-cols-header
---

# Foundational Pattern: Pub-Sub

## One-to-Many Broadcast

::left::

<div class="mb-16 mt-12 text-center">

```mermaid
graph LR
  Publisher --> Topic((Topic));
  Topic --> Subscriber1[Analytics Service];
  Topic --> Subscriber2[Archiving Service];
  Topic --> SubscriberN[Monitoring Service];
```

</div>

::right::

<div class="mb-30 flex flex-col justify-center h-full">

<p class="text-3xl" style="line-height: 1.4;">
  <b>Analogy:</b> A Radio Broadcast 📻
</p>
<p class="text-3xl" style="line-height: 1.4;">
  A single event can be consumed by many different services for different purposes.
</p>

</div>

<style>
.two-cols-header {
  column-gap: 20px;
}
</style>

<!---
1. "The second key pattern is Publish-Subscribe, or Pub-Sub. This is a one-to-many broadcast model."
2. "The analogy here is a radio station. A publisher broadcasts a message to a central 'topic', not to any specific receiver."
3. "Multiple subscribers can then tune into that topic to receive a copy of the message. This is incredibly powerful because the same event—like a user click—can be used by an analytics service, an archiving service, and a monitoring service simultaneously, without them knowing about each other."
-->

---

# Introduction to Apache Kafka

## The Holding Area for Data

<div class="grid grid-cols-2 gap-8 items-center mt-8">
  <div class="text-left">
    <span class="text-3xl">Key Features:</span>
    <ul class="list-disc pl-8 mt-4">
      <li>Combines Queuing & Pub-Sub</li>
      <li>Distributed & Fault-Tolerant</li>
      <li>Immutable, Replayable Log</li>
    </ul>
  </div>
  <div>
    <img src="/kafka/fit_in.svg" class="w-full p-2" />
  </div>
</div>

<style>
  li, li * {
    font-size: 1.5rem;
  }
</style>

<!---
1. "So, where does Apache Kafka fit in? Kafka is a distributed streaming platform that brilliantly combines both of these patterns."
2. "It allows for both point-to-point delivery like a queue and broadcast capabilities like pub-sub. But its real power comes from being a distributed, fault-tolerant, and replayable log."
3. "This means data is stored safely across multiple machines, and if something goes wrong, you can 'replay' the data stream. It’s the perfect backbone for a reliable real-time pipeline."
-->

---

# Partition Replication

<div class="flex items-center justify-center">
<img src="/kafka/replication.svg" class="w-5/6"/>
</div>

<!---
1. "Let's quickly visualize how Kafka achieves its fault tolerance. This slide shows a core concept: replication."
2. "Kafka doesn't just store data in one place; it makes copies of it across different servers, which it calls brokers."
3. "We'll see on the next slide how this leader-and-follower model prevents data loss."
-->

---
layout: two-cols-header
---

# Kafka Architecture: Built for Resilience

::left::

<div class="mt-0 text-center">

```mermaid
graph TD
  subgraph Topic: Campaign Ads
    direction LR
    P1["Partition 0 (Leader)<br/>Broker 1"]
    P1_R1["Partition 0 (Follower)<br/>Broker 2"]
    P1_R2["Partition 0 (Follower)<br/>Broker 3"]
    P1 -- "replicates to" --> P1_R1
    P1 -- "replicates to" --> P1_R2
  end
  Producer -- Writes to --> P1
  Consumer -- Pulls From --> P1
```

</div>

::right::

<div class="mt-0 flex flex-col justify-center h-full">

<ul class="text-2xl space-y-4">
  <li>A topic is split into <b>Partitions</b> for parallelism.</li>
  <li>Each partition is replicated across multiple <b>Brokers</b> (servers).</li>
  <li>One replica is the <b>Leader</b> (handles reads/writes); others are <b>Followers</b>.</li>
  <li>If a Leader fails, a Follower is automatically elected as the new Leader.</li>
</ul>

</div>

<style>
.two-cols-header {
  column-gap: 20px;
}
</style>

<!---
1. "Let's break that down. A single data feed in Kafka is called a Topic. For performance, a topic is split into multiple Partitions."
2. "Each partition is then replicated across several servers, or Brokers. One of these replicas is elected the 'Leader'—it handles all the new data."
3. "The other replicas are 'Followers' that just copy the leader. The magic is, if the leader's server fails, Kafka automatically elects one of the followers to become the new leader. This makes the system incredibly resilient to hardware failure."
-->

---

# Consumer Groups

## A partition can only be read by one consumer in a group

<div class="flex items-center justify-center">
<img src="/kafka/multi_cg.svg" class="w-2.2/4"/>
</div>

<!---
1. "Kafka also gives us massive scalability on the reading side using a concept called Consumer Groups."
2. "You can have multiple instances of your application running, all belonging to the same group. Kafka ensures that each partition is consumed by exactly ONE consumer within that group."
3. "This means if you have a topic with 4 partitions, you can run up to 4 instances of your service to process the data in parallel. If you need to re-process the data for a different purpose, you just create a *new* consumer group, as shown here with the 'Archiving' group."
-->

---

# What is a Stream
<div class="flex flex-col items-center justify-center">
  <div class="flex flex-row justify-between px-6 mx-4 w-full max-w-4xl">
  <v-click>
    <div class="flex flex-col items-center mt-4">
      <h2 class="text-lg font-semibold mb-2">Nature's Stream</h2>
      <img src="/mongo/water_stream.webp" class="w-80 h-auto pt-2" alt="Nature's Stream"/>
    </div>
    </v-click>
    <v-click>
    <div class="flex flex-col items-center mt-4">
      <h2 class="text-lg font-semibold mb-2">Data Stream</h2>
      <img src="/mongo/data_stream.webp" class="w-80 h-auto pt-2" alt="Data Stream"/>
    </div>
    </v-click>
  </div>

  <!-- Footer Text -->
  <v-after>
  <h4 class="mt-4 text-center text-sm font-medium">
    Not all streams are the same
  </h4>
  </v-after>
</div>

<!---
1. "So we've talked about the pipes—Kafka—now let's talk about what flows through them: streams."
2. "On the left, we have a stream in nature: a continuous, unbounded flow of water. On the right, a data stream: a continuous, unbounded flow of events."
3. "The key takeaway is that, unlike a file or a database table, a stream has no end. And we need special techniques to handle this infinite nature."
-->


---

# Understanding Streams & Windows

## Taming an Infinite Flow

<div class="mt-12">
  <p class="text-3xl">An unbounded stream of events:</p>
  <p class="font-mono mt-2 tracking-widest text-3xl">... ● ● ● ● ● ● ● ● ● ● ● ● ...</p>

  <br/>
  
  <v-click>
    <p class="mt-12 text-3xl">Windows create finite slices for aggregation:</p>
    <p class="font-mono mt-2 tracking-widest text-cyan-400 text-3xl">... [● ● ● ●] [● ● ● ●] [● ● ● ●] ...</p>
  </v-click>
</div>

<!---
1. "So, how do you perform calculations like 'count' or 'average' on an infinite stream? You can't. The number would just go up forever."
2. "The solution is to impose boundaries. We create finite, manageable slices of the stream called 'windows'."
3. "By doing this, we can change the question from 'How many clicks have happened ever?' to 'How many clicks happened in the last 30 seconds?' This is the fundamental concept behind nearly all stream processing."
-->

---

# Types of Windows

## Slicing by Fixed Time vs. User Activity

<div class="grid grid-cols-2 gap-8 mt-8 text-center">

  <!-- Tumbling Window -->
  <div class="p-4 bg-slate-800 rounded-lg">
    <h3>Tumbling</h3>
    <pre class="text-2xl text-cyan-400 mt-4"><code>[● ● ●] [● ● ●]</code></pre>
    <p class="mt-4 text-lg">Fixed-size, non-overlapping chunks of time.</p>
    <hr class="opacity-20 my-3" />
    <p class="text-base text-gray-400"><b>Use Case:</b> A report of total clicks every 30 seconds.</p>
  </div>

  <!-- Session Window -->
  <div class="p-4 bg-slate-800 rounded-lg">
    <h3>Session</h3>
    <pre class="text-2xl text-cyan-400 mt-4"><code>[● ●]   [● ● ● ●]</code></pre>
    <p class="mt-4 text-lg">Groups events by activity, closes after an inactivity gap.</p>
    <hr class="opacity-20 my-3" />
    <p class="text-base text-gray-400"><b>Use Case:</b> Analyzing a user's entire visit to a website until they go idle.</p>
  </div>

</div>

<!---
1. "There are several ways to create these windows. Let's look at two common types."
2. "On the left are **Tumbling Windows**, which are what we'll use in our demo. They are fixed-size, non-overlapping chunks. Think of them as a perfect grid slicing up time. An event belongs to exactly one window."
3. "On the right are **Session Windows**, which are defined by user activity. A window opens when a user does something and closes only after a period of inactivity. This is great for analyzing a user's entire visit as a single unit."
-->

---

# Types of Windows

## Analyzing Rolling Time Frames

<div class="grid grid-cols-2 gap-8 mt-8 text-center">

  <!-- Hopping Window -->
  <div class="p-4 bg-slate-800 rounded-lg">
    <h3>Hopping</h3>
    <pre class="text-2xl text-cyan-400 mt-4"><code>[● ● ● ●]<br>  [● ● ● ●]</code></pre>
    <p class="mt-4 text-lg">Triggered by a fixed **TIME** interval (the 'hop').</p>
    <hr class="opacity-20 my-3" />
    <p class="text-base text-gray-400"><b>Use Case:</b> A dashboard showing sales in the last 10 minutes, updated every 5 minutes.</p>
  </div>

  <!-- Sliding Window -->
  <div class="p-4 bg-slate-800 rounded-lg">
    <h3>Sliding</h3>
    <pre class="text-xl text-cyan-400 mt-4"><code>[● ● ● ●]  <br>[○ ● ● ● <span style="color:white">●</span>]</code></pre>
    <p class="mt-4 text-lg">Triggered by a new **EVENT** arriving.</p>
    <hr class="opacity-20 my-3" />
    <p class="text-base text-gray-400"><b>Use Case:</b> A real-time alert if a user makes 5 purchases in the last 1 minute.</p>
  </div>

</div>

<!---
1. "We can also have windows that overlap. The key difference between these two is what *triggers* the calculation."
2. "A **Hopping Window** is time-triggered. It has a size (e.g., 10 minutes) and a 'hop' (e.g., 5 minutes). Every 5 minutes, a new window is created covering the last 10 minutes of data. This is perfect for dashboards."
3. "A **Sliding Window**, however, is event-triggered. A window of a fixed size moves with each new event. This is ideal for things that require an immediate reaction, like detecting if a user made 5 purchases in the last 1 minute."
-->

---

# Introduction to Apache Flink

## The Brain of the Operation 🧠

**What is it?** A stateful stream processing framework.

<div class="mt-8 text-left pl-20">
  <span class="text-3xl">Superpowers:</span>
  <ul class="list-disc pl-8 mt-4">
    <li><b>Stateful:</b> Remembers information across events (e.g., running counts).</li>
    <li><b>Exactly-Once Guarantees:</b> Ensures correctness, even with failures.</li>
    <li><b>PyFlink:</b> The powerful Python API we're using today.</li>
  </ul>
</div>

<style>
  li, li * {
    font-size: 1.6rem;
  }
</style>

<!---
1. "If Kafka is the circulatory system of our pipeline, Apache Flink is the brain. It's the engine that will actually perform our windowed calculations."
2. "Flink is a true stream processing framework, and its superpowers are threefold."
3. "First, it's **Stateful**. It can remember things, like the running count of clicks in a window. Second, it provides **Exactly-Once Guarantees**, which is a fancy way of saying it's extremely accurate and won't miscount data even if machines fail. And finally, it has a fantastic Python API called **PyFlink**, which is what we'll be using."
-->

---

# Flink Architecture: How it Works

```mermaid
graph TD
    Client -- "Submits Job" --> JM(JobManager);
    JM -- "Deploys Tasks" --> TM1(TaskManager 1);
    JM -- "Deploys Tasks" --> TM2(TaskManager 2);

    subgraph TaskManager 2
        Slot1[Task Slot]
        Slot2[Task Slot]
    end
    subgraph TaskManager 1
        Slot3[Task Slot]
        Slot4[Task Slot]
    end
```
- **JobManager (The Brain):** Coordinates the entire job execution.
- **TaskManagers (The Muscle):** Worker processes that execute the actual data processing tasks in parallel **Slots**.

<!---
1. "At a high level, a Flink cluster has two types of components."
2. "The **JobManager** is the brain. It receives your code, figures out how to execute it, and coordinates the whole process."
3. "The **TaskManagers** are the muscle. They are the worker nodes that actually run your code on the data. Each TaskManager has multiple 'Slots', allowing it to perform several tasks in parallel."
-->

---

# Recap of Kafka Example

<div class="flex items-center justify-center">
<img src="/kafka/multi_cg.svg" class="w-2.4/4"/>
</div>

<!---
1. "Just to quickly remind you of the Kafka consumer group model we saw earlier..."
2. "We have multiple consumers in a group processing data in parallel from different partitions."
3. "Now let's see how Flink's architecture maps directly onto this."
-->

---

# How Flink reads from Kafka

```mermaid
flowchart LR
  KA[(Kafka Partition A–M)] --> S1[Source Subtask #1]
  KB[(Kafka Partition N–Z)] --> S2[Source Subtask #2]

  S1 -->|map/filter| S1a[Parallel stream]
  S2 -->|map/filter| S2a[Parallel stream]

  S1a -->|keyBy userId| KX[Keyed Operator\n window/agg/join p=2]
  S2a -->|keyBy userId| KX

  KX --> OUT[(Sink / Dashboard / DB)]
```

<!---
1. "This is how Flink achieves parallelism. When you tell Flink to read from a Kafka topic, it will spin up a parallel 'source' task for each Kafka partition."
2. "Simple operations like mapping or filtering can happen in parallel, with no communication needed."
3. "But when you do a grouping operation, like our `keyBy('campaign_id')`, Flink performs a network shuffle to ensure all events for the same key end up on the same machine. This is what makes stateful operations like windowing possible."
-->

---

# The Problem: Out-of-Order Events

## The Messiness of Reality

Events don't always arrive in the order they occurred due to network latency, device issues, etc

<div class="p-4 mt-8 bg-slate-800 rounded font-mono text-lg text-left">
  <p>Actual Event Order (10:00:00 - 10:05:00 window): (10:02:59), (10:03:01)</p>
  <v-click>
    <p class="mt-4">Arrival Order at Processor:</p>
    <p class="text-yellow-400">Event @ 10:03:01 arrives</p>
    <p class="text-red-500">Event @ 10:02:59 arrives LATE!</p>
  </v-click>
</div>

<v-click>
<h3 class="mt-8">Question: How does our system know when a time window (e.g., 10:00-10:05) is "complete"?</h3>
</v-click>

<!---
1. "Now we get to one of the hardest problems in stream processing: reality is messy."
2. "Just because an event happened at 10:02, doesn't mean it will arrive at our processor at 10:02. Due to network lag or mobile device issues, events often arrive out of order."
3. "As you can see, the event from 10:02 arrived *after* the event from 10:03. This creates a huge problem: How does our system ever know that it has received all the data for the 10:00 to 10:05 window and that it's safe to calculate the result?"
-->

---

# The Solution: Watermarks

## Flink's Event-Time Clock

A **Watermark** is a special message in the stream that acts as a progress indicator.

<div class="p-6 mt-3 bg-slate-800 rounded text-xl border-l-4 border-cyan-400">
  It is a declaration: <br/>
  <em class="text-cyan-400">"I am now confident all events before timestamp `T` have arrived."</em>
</div>

This allows Flink to safely close windows and emit results.

<v-click>

Watermark is defined to be 10 seconds behind the latest event time
<div class="mt-3 p-6 m-3 rounded font-mono text-lg bg-slate-800 border-l-4 border-cyan-400">

  WATERMARK FOR event_time AS event_time - INTERVAL '10' SECOND
</div>
</v-click>

<!---
1. "Flink's elegant solution to this problem is called Watermarks."
2. "A Watermark is a special message that flows through the data stream. It's Flink's internal clock, but it's based on the timestamps of the data itself, not the wall clock on the server."
3. "A watermark with a timestamp 'T' is a declaration from Flink saying, 'I am now confident that we will not see any more events with a timestamp earlier than T.' This signal gives Flink the confidence it needs to close a window and finalize the result."
-->

---

# Watermarks in Action: The Flow of Time

## Let’s trace a few events with a 10-second watermark delay and a 30-second tumbling window (`10:00:00 – 10:00:30`)

<div>

| Event  | Event Time | Processing Time | Max Event Time | Current Watermark (= maxET − 10 s) | System Action                                        |
| :----- | :--------- | :-------------- | :------------- | :--------------------------------- | :--------------------------------------------------- |
| **E1** | 10:00:15   | 10:00:16        | 10:00:15       | **10:00:05**                       | Buffer E1 (assign to window 00-30)                   |
| **E2** | 10:00:25   | 10:00:26        | 10:00:25       | **10:00:15**                       | Buffer E2; watermark advances                        |
| **E3** | 10:00:18   | 10:00:27        | 10:00:25       | **10:00:15**                       | Buffer E3; watermark holds                 |
| **E4** | 10:00:42   | 10:00:43        | 10:00:42       | **10:00:32**                       | ✅ **Trigger window 00-30**; Buffer E4 in next window |

</div>

<!---
1. "Let's walk through this. We have a 10-second watermark delay and a 30-second window."
2. "Event E1 arrives with a time of 10:00:15. This is the latest event we've seen, so Flink sets the watermark to 10 seconds before that: 10:00:05."
3. "E2 arrives at 10:00:25. This is our new max time, so the watermark advances to 10:00:15."
4. "E3 arrives. It's an out-of-order event at 10:00:18, but that's okay. It's not later than our max time of 25, so the watermark doesn't move. The event is correctly placed in the 0-30 second window."
5. "Finally, E4 arrives at 10:00:42. The new max time advances the watermark to 10:00:32. As soon as the watermark passes the end of our window (10:00:30), Flink says 'Aha! This window is complete,' and it triggers the calculation for that window."
-->

---

# What if the Stream Stops? Idle Source Problem

No new events ➞ No new watermarks ➞ Stuck windows & no results!

<div class="grid grid-cols-2 gap-8 mt-8 text-left">

  <!-- Solution A: The Flink Way -->
  <div class="p-4 bg-slate-800 rounded-lg">
    <span>Solution A: Configure Idleness in Flink</span>
    <p class="mt-2">Flink can detect when a source partition is idle and automatically advance its watermark.</p>
    <div class="mt-4 p-2 bg-slate-900 rounded font-mono text-sm">
      <pre><code>WatermarkStrategy
  .forBoundedOutOfOrderness(...)
  .withIdleness(Duration.ofMinutes(1));</code></pre>
    </div>
    <hr class="opacity-20 my-4" />
    <p><b>Best for:</b> Simplicity. The logic is self-contained within the Flink job, requiring no changes to the data producer.</p>
  </div>

  <!-- Solution B: The Producer Way -->
  <div class="p-4 bg-slate-800 rounded-lg">
    <span>Solution B: Send Heartbeat Messages</span>
    <p class="mt-2">The data producer sends periodic dummy messages with a current timestamp to keep watermarks flowing.</p>
```mermaid
graph LR
  A[Producer] -- "Event" --> K((Kafka));
  B[Heartbeat Generator];
  B -- "<br/>Heartbeat<br/>(every 30s)" --> K;
  K --> F[Flink];
```
    <hr class="opacity-20 my-4" />
    <p><b>Best for:</b> Portability. This pattern works with any stream processing engine, not just Flink.</p>
  </div>
</div>

<!---
1. "This leads to a critical edge case. Watermarks only advance when new events arrive. What happens if there's no activity for a few minutes? Our windows will get stuck and never trigger!"
2. "There are two great solutions. Solution A is the Flink way: you can simply configure your source to detect idleness. If no message comes for a minute, Flink will automatically advance the watermark for you. It's clean and self-contained."
3. "Solution B is to solve it at the source. You can have your data producer send a periodic 'heartbeat' message. This dummy event's only job is to carry a fresh timestamp to keep the watermarks flowing. This pattern is more portable across different stream processors."
-->

---

# Allowed Lateness

## Handling Stragglers

**What if an event is *very* late and arrives after its window is closed?**

<div class="mt-8">

```mermaid
graph LR
    A[Late Event Arrives] --> B{Is its window closed?};
    B -- Yes --> C{Is it within the 'lateness' period?};
    C -- Yes --> D[✅ Update the Window Result];
    C -- No --> E[❌ Discard Event];
```

</div>

**Allowed Lateness:** A grace period that lets Flink accept late events and **update** the previously emitted result for that window. Works only for retractable sinks.


<!---
1. "But what if an event is *extremely* late? What if it arrives after the watermark has already closed its window?"
2. "By default, Flink would just drop this event. But we can configure a grace period called 'Allowed Lateness'."
3. "If a late event arrives and its window is closed, Flink checks if it's still within this grace period. If it is, Flink will actually process the event and emit an *updated result* for the window. This is a powerful feature for improving accuracy, but it requires your downstream system, like a database, to be able to handle updates."
-->


---

# System Architecture

## The End-to-End Pipeline

<br/>

```mermaid
graph LR
    subgraph Data Generation
        A[Go Producer]
    end
    subgraph Transport Layer
        B((Apache Kafka))
    end
    subgraph Real-Time Processing
        C[Apache Flink <br/> PyFlink Job]
    end
    subgraph Storage
        D[/File Sink Results/]
    end
    A -- "impressions, clicks" --> B;
    B -- "reads streams" --> C;
    C -- "writes CTR" --> D;
```

<!---
1. "Okay, let's put all those concepts together and look at our final system architecture."
2. "It's a clean, linear pipeline. We start with a Go Producer generating our impression and click data."
3. "That data is sent to Apache Kafka, which acts as our durable, high-throughput transport layer."
4. "Our PyFlink job reads from Kafka, performs the real-time join and windowed CTR calculation."
5. "And finally, the results are written out to a file sink on the filesystem."
-->

---

# Components

## A Look Under the Hood

<div class="grid grid-cols-2 gap-6 mt-8 text-left">
  <div class="p-4 bg-slate-800 rounded-lg">
    <h3 class="text-cyan-400">Go Producer</h3>
    <p>Generates synthetic impressions & clicks with realistic random delays.</p>
  </div>
  <div class="p-4 bg-slate-800 rounded-lg">
    <h3 class="text-cyan-400">Apache Kafka</h3>
    <p>Acts as a durable buffer, ingesting events on `impressions` and `clicks` topics.</p>
  </div>
  <div class="p-4 bg-slate-800 rounded-lg">
    <h3 class="text-cyan-400">PyFlink Job</h3>
    <p>The core logic: joins streams, applies windows, and calculates CTR.</p>
  </div>
  <div class="p-4 bg-slate-800 rounded-lg">
    <h3 class="text-cyan-400">File Sink</h3>
    <p>Persists the final results to the filesystem with exactly-once guarantees.</p>
  </div>
</div>

<!---
1. "Here's a closer look at each component's role."
2. "The **Go Producer** is a simple application designed to mimic real-world ad traffic, even introducing random delays to simulate out-of-order events."
3. "**Kafka** acts as the central nervous system and buffer for our data."
4. "The **PyFlink Job** is the core logic engine where all the stateful computation happens."
5. "And the **File Sink** is our destination. Flink ensures that even when writing to something as simple as a file, it does so with exactly-once guarantees, meaning no duplicate or missing results."
-->

---

# PyFlink Logic Walkthrough

<div class="text-left mt-8 pl-12">
  <ol class="text-2xl space-y-4">
    <li><span class="text-cyan-400">Source:</span> Read from Kafka `impressions` and `clicks` topics.</li>
    <li><span class="text-cyan-400">Interval Join:</span> Match clicks to impressions if `impr_id` matches AND the click occurs within 15 seconds.</li>
    <li><span class="text-cyan-400">Window:</span> Group matched pairs into 30-second Tumbling Windows by `campaign_id`.</li>
    <li><span class="text-cyan-400">Aggregate:</span> For each window, count impressions, count clicks, and calculate `CTR`.</li>
    <li><span class="text-cyan-400">Sink:</span> Write the results to a partitioned CSV file.</li>
  </ol>
</div>

<!---
1. "Let's walk through the five logical steps inside the Flink job itself."
2. "First, we define our **Sources**: we connect to the 'impressions' and 'clicks' topics in Kafka."
3. "Second, we perform an **Interval Join**. This is key. We match a click to an impression if they share the same ID *and* the click happened within 15 seconds of the impression. This prevents us from associating a click with an ad someone saw yesterday."
4. "Third, we apply a 30-second Tumbling **Window** to the stream of matched pairs, grouping them by campaign."
5. "Fourth, we **Aggregate**. Within each window, we simply count the unique impressions and clicks to calculate the CTR."
6. "Finally, our **Sink** writes these final results to a CSV file."
-->

---

# Demo

## Let's See It in Action!

<div class="grid grid-cols-2 gap-8 items-center mt-8">
  <div class="text-left">
    <h3>Let's Run It!</h3>
    <ol class="list-decimal pl-6 mt-4 text-xl space-y-3">
      <li>
        <b>Start Pipeline:</b>
        <pre><code class="text-sm">sh run_demo.sh</code></pre>
      </li>
      <li>
        <b>Monitor Flink UI:</b>
        <a href="http://localhost:8081" target="_blank"> http://localhost:8081</a>
      </li>
      <li>
        <b>View Results:</b>
        <pre><code class="text-sm">python read_results.py</code></pre>
      </li>
    </ol>
  </div>
  <div class="text-center">
    <img src="/stream_adtech/stream_adtech_qr.png" class="w-2/3 mx-auto bg-white p-2 rounded-lg" />
    <p class="mt-4">
      <a href="https://github.com/susmitpy/stream_analytics_adtech_ctr" target="_blank">
        github.com/susmitpy/stream_analytics_adtech_ctr
      </a>
    </p>
  </div>
</div>

<!---
1. "Now for the fun part. Let's see this all in action."
2. "The entire pipeline is containerized with Docker, so it's very easy to run. The `run_demo.sh` script will start Kafka, Zookeeper, Flink, and submit our job."
3. "You can monitor the job's progress and see the data flowing through the Flink UI at localhost:8081."
4. "And the `read_results.py` script will continuously tail the output files, so we can see our real-time CTR results as they are computed."
5. "You can find all the code at the GitHub link on the screen."
-->

---
src: ./pages/connect.md
---

---
src: ./pages/qa.md
---
