# Task 1 – High-Level Package Diagram
 
## Overview
 
The HBnB application follows a **3-layer architecture** (Presentation → Business Logic → Persistence), using the **Facade Pattern** to decouple layers and simplify inter-layer communication.
 
---
 
## Package Diagram
 
```mermaid
flowchart TB
 
    subgraph Presentation["🖥️ Presentation Layer"]
        direction TB
        API["API Endpoints\n─────────────────\nPOST /users\nPOST /places\nPOST /reviews\nGET  /places"]
        Services["Services\n─────────────────\nRequest parsing\nResponse formatting\nAuth middleware"]
        API --> Services
    end
 
    subgraph Business["⚙️ Business Logic Layer"]
        direction TB
        Facade["HBnBFacade\n─────────────────\ncreate_user()\ncreate_place()\ncreate_review()\nget_places()"]
        Models["Domain Models\n─────────────────\nUser · Place\nReview · Amenity\n+ Validation rules\n+ Business rules"]
        Facade --> Models
    end
 
    subgraph Persistence["🗄️ Persistence Layer"]
        direction TB
        Repository["Repository (Interface)\n─────────────────\nsave()\nfind_by_id()\nfind_all()\nupdate()\ndelete()"]
        Database["Database\n─────────────────\nPersistent storage"]
        Repository --> Database
    end
 
    Services  -->|"calls via Facade"| Facade
    Models    -->|"CRUD operations"| Repository
```
 
---
 
## Layer Responsibilities
 
### Presentation Layer
Entry point for all client requests (HTTP). It handles routing, authentication middleware, request parsing and response formatting. It contains **no business logic** — it delegates everything to the Business Logic Layer through the Facade.
 
### Business Logic Layer & Facade Pattern
The heart of the application. The **Facade** (`HBnBFacade`) exposes a clean, unified interface to the Presentation Layer, hiding the complexity of model interactions. For example, creating a review requires checking user existence, place existence, and reservation status — the Facade orchestrates all of this transparently.
 
### Persistence Layer
Responsible for all data storage and retrieval. The `Repository` interface abstracts the underlying database technology (SQL, NoSQL, file storage, etc.), so the Business Logic Layer never depends on implementation details.
 
---
 
## Why the Facade Pattern?
 
| Without Facade | With Facade |
|---|---|
| API must know about User, Place, Review models | API only calls one interface |
| Changes in models break API code | Changes are isolated behind the Facade |
| Hard to test layers independently | Each layer can be mocked independently |
 
The Facade acts as a **single point of contact** between the Presentation and Business Logic layers, reducing coupling and making the codebase easier to maintain and extend.