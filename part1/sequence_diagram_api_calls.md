# Task 2 – Sequence Diagrams: API Interaction Flows
 
## Overview
 
These four diagrams illustrate how the three layers (Presentation, Business Logic, Persistence) collaborate to handle typical API requests. Each diagram follows the same pattern: the API delegates to the Facade, which orchestrates validation and model creation before persisting data.
 
---
 
## 4.1 – User Registration (`POST /users`)
 
```mermaid
sequenceDiagram
    actor Client
    participant API        as API (Presentation)
    participant Facade     as HBnBFacade
    participant Logic      as Business Logic
    participant Repo       as Repository
    participant DB         as Database
 
    Client ->> API: POST /users {first_name, last_name, email, password}
 
    API ->> Facade: create_user(data)
 
    alt Missing required fields
        Facade -->> API: 400 Bad Request
        API -->> Client: "Please fill all required fields"
 
    else Invalid email format
        Facade -->> API: 400 Bad Request
        API -->> Client: "Invalid email address"
 
    else Email already in use
        Facade -->> API: 409 Conflict
        API -->> Client: "Email already registered"
 
    else Valid data
        Facade ->> Logic: build_user(data)
        Logic -->> Logic: hash password · assign UUID
        Logic ->> Repo: save(user)
        Repo ->> DB: INSERT INTO users
 
        alt DB error
            DB -->> Repo: Error
            Repo -->> Logic: Failure
            Logic -->> Facade: 500 Internal Server Error
            Facade -->> API: 500
            API -->> Client: "An error occurred, please try again"
        else Success
            DB -->> Repo: OK + user_id
            Repo -->> Logic: saved
            Logic -->> Facade: user object
            Facade -->> API: 201 Created + user object
            API -->> Client: "Account created" + user_id
        end
    end
```
 
> **Key point:** Password hashing and email uniqueness checks happen inside the Facade / Business Logic — never at the API level.
 
---
 
## 4.2 – Place Creation (`POST /places`)
 
```mermaid
sequenceDiagram
    actor Client
    participant API        as API (Presentation)
    participant Facade     as HBnBFacade
    participant Logic      as Business Logic
    participant Repo       as Repository
    participant DB         as Database
 
    Client ->> API: POST /places {title, price, lat, lng, amenities}
    Note over API: JWT verified by middleware
 
    API ->> Facade: create_place(data, owner_id)
 
    alt Missing required fields
        Facade -->> API: 400 Bad Request
        API -->> Client: "Fill all required fields"
 
    else Invalid price or coordinates
        Facade -->> API: 400 Bad Request
        API -->> Client: "Check price / location values"
 
    else Valid data
        Facade ->> Logic: build_place(data)
        Logic -->> Logic: validate · assign UUID · link owner
        Logic ->> Repo: save(place)
        Repo ->> DB: INSERT INTO places
 
        alt DB error
            DB -->> Repo: Error
            Repo -->> Logic: Failure
            Logic -->> Facade: 500
            Facade -->> API: 500
            API -->> Client: "An error occurred, please try again"
        else Success
            DB -->> Repo: OK + place_id
            Repo -->> Logic: saved
            Logic -->> Facade: place object
            Facade -->> API: 201 Created + place object
            API -->> Client: "Place created" + place_id
        end
    end
```
 
> **Key point:** Authentication happens at the API middleware level. The Facade only receives already-authenticated `owner_id`.
 
---
 
## 4.3 – Review Submission (`POST /reviews`)
 
```mermaid
sequenceDiagram
    actor Client
    participant API        as API (Presentation)
    participant Facade     as HBnBFacade
    participant Logic      as Business Logic
    participant Repo       as Repository
    participant DB         as Database
 
    Client ->> API: POST /reviews {place_id, rating, text}
 
    API ->> Facade: create_review(data, user_id)
 
    alt Invalid input (missing fields or bad rating)
        Facade -->> API: 400 Bad Request
        API -->> Client: "Review data invalid"
 
    else User has not reserved this place
        Facade ->> Logic: check_reservation(user_id, place_id)
        Logic ->> Repo: find_reservation(user_id, place_id)
        Repo ->> DB: SELECT FROM reservations
        DB -->> Repo: No match
        Repo -->> Logic: not found
        Logic -->> Facade: 403 Forbidden
        Facade -->> API: 403
        API -->> Client: "You must stay at the place before reviewing"
 
    else Valid data + stay confirmed
        Facade ->> Logic: build_review(data)
        Logic -->> Logic: validate · assign UUID
        Logic ->> Repo: save(review)
        Repo ->> DB: INSERT INTO reviews
 
        alt DB error
            DB -->> Repo: Error
            Repo -->> Logic: Failure
            Logic -->> Facade: 500
            Facade -->> API: 500
            API -->> Client: "An error occurred, please try again"
        else Success
            DB -->> Repo: OK + review_id
            Repo -->> Logic: saved
            Logic -->> Facade: review object
            Facade -->> API: 201 Created + review object
            API -->> Client: "Review submitted"
        end
    end
```
 
> **Key point:** The Facade enforces the **business rule** that only users with a confirmed stay can post a review — this logic never leaks into the API layer.
 
---
 
## 4.4 – Fetch Places (`GET /places`)
 
```mermaid
sequenceDiagram
    actor Client
    participant API        as API (Presentation)
    participant Facade     as HBnBFacade
    participant Logic      as Business Logic
    participant Repo       as Repository
    participant DB         as Database
 
    Client ->> API: GET /places?city=Paris&max_price=100
 
    alt Invalid query parameters
        API -->> Client: 400 Bad Request
    else Unauthorized request
        API -->> Client: 401 Unauthorized
    else Valid request
        API ->> Facade: get_places(filters)
        Facade ->> Logic: get_places(filters)
        Logic ->> Repo: find_all(query)
        Repo ->> DB: SELECT * FROM places WHERE ...
 
        alt DB error
            DB -->> Repo: SQL Error
            Repo -->> Logic: Error
            Logic -->> Facade: 500
            Facade -->> API: 500
            API -->> Client: "An error occurred, please try again"
 
        else No results
            DB -->> Repo: Empty result
            Repo -->> Logic: []
            Logic -->> Facade: PlaceCollectionDTO (empty)
            Facade -->> API: PlaceCollectionDTO
            API -->> Client: 200 OK + empty list
 
        else Results found
            DB -->> Repo: Rows
            Repo -->> Logic: List[Place]
            Logic -->> Facade: PlaceCollectionDTO (places + metadata)
            Facade -->> API: PlaceCollectionDTO
            API -->> Client: 200 OK + places + pagination info
        end
    end
```
 
> **Key point:** The `PlaceCollectionDTO` wraps both the list of places and metadata (total count, applied filters, pagination) into a single clean response object, avoiding raw database exposure.
 
---
 
## Summary: Common Flow Pattern
 
Every API call follows the same layered flow:
 
```
Client → API (auth + parsing) → Facade (orchestration) → Business Logic (rules + validation) → Repository → Database
```
 
Errors are caught at the appropriate layer and propagated back with the correct HTTP status code, keeping each layer's responsibility clearly separated.