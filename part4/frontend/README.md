# HBnB — Frontend Web Client

A simple web client built in HTML5, CSS3, and JavaScript ES6 that connects to the HBnB REST API. No frameworks, no build tools — just vanilla JS and the Fetch API.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Pages](#pages)
3. [Authentication](#authentication)
4. [Price Filter](#price-filter)
5. [Registration](#registration)

---

## Getting Started

### Option 1 — Live Server (recommended)

1. Open the `frontend/` folder in VS Code
2. Right-click `index.html` → **Open with Live Server**
3. The frontend will be available at `http://127.0.0.1:5500`

> **Important**: Make sure the API is running on `http://127.0.0.1:5000` before opening the frontend.
> The `API_URL` in `scripts.js` is set to `http://127.0.0.1:5000` — use `127.0.0.1` consistently to avoid cookie issues.

### Option 2 — Direct browser

Open `frontend/index.html` directly in your browser (`file://`). No CORS issues in this mode since there is no separate server.

### Starting the API

```bash
# From the project root
python3 run.py
```

If it's your first run, initialize the database and create an admin first:

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()

python3 create_admin.py
```

---

## Pages

| Page           | File               | Auth required    | Description                                                         |
| -------------- | ------------------ | ---------------- | ------------------------------------------------------------------- |
| List of Places | `index.html`       | ❌               | Displays all places as cards with price filter                      |
| Login          | `login.html`       | ❌               | JWT login — redirects to index on success                           |
| Place Details  | `place.html`       | ❌ (form hidden) | Place info, amenities, reviews + inline review form                 |
| Add Review     | `add_reviews.html` | ✅               | Standalone review form — redirects to index if not logged in        |
| Register       | `register.html`    | ❌               | _(bonus)_ New user registration — see [Registration](#registration) |

---

## Authentication

Authentication is handled entirely client-side using a JWT cookie.

### Login flow

```
1. User submits the login form (email + password)
2. JS sends POST to /api/v1/auth/login
3. API returns { access_token: "..." }
4. JS stores the token in a cookie (SameSite=Lax, 7-day expiry)
5. Header button switches from "Login" to "Logout"
```

### On every page load

- `setupHeaderAuth()` checks for the cookie
- If authenticated → button shows **Logout** (clears cookie on click)
- If not authenticated → button shows **Login** (links to `login.html`)

### Protected pages

- `place.html` — the inline review form is hidden if the user is not authenticated
- `add_reviews.html` — redirects to `index.html` if no token is found in the cookie

### Logout

Clicking **Logout** in the header deletes the cookie and redirects to `index.html`.

---

## Price Filter

The price filter on `index.html` works entirely client-side — no extra API call is made.

All places are fetched once on page load and stored in a `allPlaces` array. When the user selects a price range, the displayed cards are filtered from this array:

```javascript
const filtered = allPlaces.filter((p) => p.price <= maxPrice);
displayPlaces(filtered);
```

Available options: **$10**, **$50**, **$100**, **All**.

---

## Registration

`register.html` is a **bonus page** — it is not part of the official task requirements.

In the current architecture, user creation is restricted to administrators (see the main README for details). This means the registration form submits to the API but will be rejected unless an admin token is used.

This page exists as a starting point for a future improvement where a public registration or account request system could be implemented.

---

## Author

- [Arnaud Messenet](https://github.com/Crypoune) &nbsp;&nbsp; [![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/Crypoune)

---
