---
theme: seriph
class: text-center

title: Firestore Security Rules - Securing your firestore db
drawings:
    persist: false
transition: slide-left
mdc: true
background: /bg_image.png

themeConfig:
    primary: "#8EE381"
---

# Firestore Security Rules - Securing your firestore db

### By Susmit Vengurlekar (@susmitpy)

---
src: ./pages/about.md
---

---
layout: image
image: /firestore/ai.jpg
backgroundSize: contain
---

---

# Agenda

1. What is Firebase and Firebase Firestore ?
2. Why Firestore Security Rules ?
3. Basics of Firestore Security Rules
4. Firestore Security Rules - Examples
5. Rules Playground for testing
6. Best Practices for Access Control Lists


<style>
    li {
        font-size: 2.2em;
    }
</style>


---

# What is Firestore ?

* Document oriented NoSQL database

* Can be directly accessed from the client side

<br/> <br/>

```mermaid
graph LR
    DB["Firestore Database"] --> CollectionA["Collection: users"]
    DB --> CollectionB["Collection: posts"]
    CollectionA --> DocumentA1["Document: user1"]
    DocumentA1 --> SubcollectionA1["Subcollection: orders"]
    SubcollectionA1 --> SubdocumentA1["Document: order1"]
    CollectionB --> DocumentB1["Document: post1"]
```

<style>
    p {
        line-height: 1.10em;
    }
    li {
        font-size: 2.2em;
    }
</style>

--- 

# Why should you secure your Firestore DB ?

- In a web app, you can't hide the API key or the document you are fetching which reveals the structure of your database

```js
const FIREBASE_CONFIG = {
    apiKey: "AIzaPodk9k38Vx9e5S0Ceg4414_6Uq5GxleI",
    authDomain: "dummy.firebaseapp.com",
    projectId: "dummy",
    storageBucket: "dummy.appspot.com",
    messagingSenderId: "123290572890",
    appId: "1:123290572890:web:b6a9947ba1typ7b8a4ac77",
    measurementId: "G-E51DK3PKQ7"
}
```

<style>
    li {
        font-size: 1.6em;
    }

    code {
        font-size: 1.9em;
    }
</style>

---

# Why should you secure your Firestore DB ?

<div class="flex items-center justify-center">

<img src="/firestore/source.png"/>

</div>

---

# Why should you secure your Firestore DB ?

<div class="flex">

<img src="/firestore/sign in.png" class="w-full"/>

</div>

---

# Why should you secure your Firestore DB ?

<div class="flex items-center justify-center">

<img src="/firestore/fetch_doc.png" class="w-full"/>

</div>


---

# Where does Firestore Security Rules fit ?

```js
const eventSnap = await getDoc(doc(db, 'events', eventId));
```

```mermaid
graph LR

A[Get Document] --> B{Firestore Security Rules}
B --> |Allowed| C[Return Document]
B --> |Denied| D[Error]
```

<style>
    code {
        font-size: 2em
    }
</style>

---
layout: image
image: /firestore/easy.jpg
backgroundSize: contain
---

---

# Authentication vs Authorization

- Authentication: Who are you ?

- Authorization: What can you do ?

- You are authenticated to join devfest, but not authorized to just take swag and leave

<style>
    p {
        line-height: 1.10em;
    }
    li {
        font-size: 2.5em;
    }
</style>

---

# Basics of Firestore Security Rules

<ul>
  <li>read
    <ul>
      <li>list - documents in a collection </li>
      <li>get - single document</li>
    </ul>
  </li>
  <li>write
    <ul>
      <li>create</li>
      <li>update</li>
      <li>delete</li>
    </ul>
  </li>
  <li> By default, all access is denied </li>
</ul>

<style>
    li {
        font-size: 1.3em;
    }
</style>


---

# Basics of Firestore Security Rules

<ul>
<li>request - incoming request</li>
<li>resource - document being accessed</li>
<li>request.resource - document being written </li>
<li> request.auth - authentication details </li>
</ul>


<style>
    li {
        font-size: 2.5em;
    }
</style>



---

# Firestore Security Rules - Examples

## Fully Secured

<div class="flex flex-col items-center justify-center">

```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

</div>

<style>
    code {
        font-size: 2em;
    }
</style>

---

# Firestore Security Rules - Examples

## Authentication Check

<div class="flex flex-col items-center justify-center">

```js
match /doctors/{doctorId} {
    allow read, write: if request.auth != null;
}
```

</div>

<style>
    code {
        font-size: 2.5em;
    }
</style>


---

# Firestore Security Rules - Examples

## Can access own document

<div class="flex flex-col items-center justify-center">

```js
match /doctors/{doctorId} {
    allow read, write: if (request.auth != null
                 && request.auth.uid == doctorId);
}
```

</div>

<style>
    code {
        font-size: 2.5em;
    }
</style>


---

# Firestore Security Rules - Examples

## Preventing Impersonation

<div class="flex flex-col items-center justify-center">

```js
match /leaves/{leaveId} {
    allow write: if request.auth != null && (
        request.auth.uid == (
             request.resource.data.doctor_id
    )); 
}
```

</div>

<style>
    code {
        font-size: 2.7em;
    }
</style>


---

# Firestore Security Rules - Examples

## Is requester's uid in allowed list ?

<div class="flex flex-col items-center justify-center">

```js
match /Patients/{patientId}{
    allow read: if 
        (request.auth.uid in resource.data.doctorIds);
}
```

</div>

<style>
    code {
        font-size: 2.4em;
    }
</style>

---

# Firestore Security Rules - Examples

## Restrict access by sign in provider

- Normal users sign in via phone
- Admins sign in via email

<div class="flex flex-col items-center justify-center">

```js
match /payouts/{payoutId} {
    allow read, write: if (
        request.auth.token.firebase.sign_in_provider == 'password'
    );
}
```

</div>

<style>
    code {
        font-size: 2em;
    }
    li {
        font-size: 1.5em;
    }
</style>



---
layout: image
image: /firestore/more.jpg
backgroundSize: contain
---

---

# Firestore Security Rules - Some More Examples

## Auth Custom Claims and Functions

<div class="flex flex-col items-center justify-center">

```js
function isSignedIn(){
    return request.auth != null;
}

function isDoctor(){
    return request.auth.token.is_doctor;
}

match /Store/KVStore {
    allow get, update: if isSignedIn() && isDoctor();
}
```

</div>

<style>
    code {
        font-size: 1.8em;
    }
</style>

---

# Firestore Security Rules - Some More Examples

## Nesting Rules & Reading a document

<div class="flex flex-col items-center justify-center">

```js
match /Patients/{patientId}{
    match /Consultations/{consultationId} {
    allow read, write: if (
        request.auth.uid in 
            (
            get(/databases/$(database)/documents/Patients/$(patientId)
            ).data
             .doctorIds)
        )
    }
}
```

</div>

<style>
    code {
        font-size: 1.8em;
    }
</style>

---

# Firestore Security Rules - Some More Examples

## Restrict update to specific fields

<div class="flex flex-col items-center justify-center">

```js
match /events/{document=**} {
    allow update: if (
        request.resource.data
            .diff(resource.data)
            .affectedKeys()
            .hasOnly(['clicks'])
        );
}
```

</div>

<style>
    code {
        font-size: 2.5em;
    }
</style>

---

# Rules Playground for testing

<div class="flex items-center justify-center mx-auto my-auto">
    <img src="/firestore/playground.png"/>
</div>


---

# Best Practices for Access Control Lists

- Deny by default
- Allow only what is necessary (least privilege)
- Approach of write exam such that the evaluator wants to fail you

<div class="flex items-center justify-center w-1/2 mx-auto mt-4">
    <img src="/firestore/hack.jpg"/>
</div>


<style>
    li {
        font-size: 1.6em;
    }
</style>

---
src: ./pages/connect.md
---


---

# Thank You !

- Access the Slides at https://susmitpy.github.io/talks/firestore_rules

<style>
    li {
        font-size: 2.3em;
    }
</style>
