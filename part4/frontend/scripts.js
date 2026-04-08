/* =============================================
   HBnB — scripts.js
   Task 01 : Login with JWT cookie
   Task 02 : Index — fetch & filter places
   Task 03 : Place details — fetch & display
   ============================================= */

const API_URL = "http://127.0.0.1:5000";

/* ════════════════════════════════════════════
   COOKIE HELPERS
   ════════════════════════════════════════════ */

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

function setCookie(name, value, days = 7) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${value}; path=/; expires=${expires}; SameSite=Lax`;
}

function deleteCookie(name) {
  document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
}

function isAuthenticated() {
  return !!getCookie("token");
}

/* ════════════════════════════════════════════
   SHARED — HEADER AUTH
   ════════════════════════════════════════════ */

function setupHeaderAuth() {
  const loginBtn = document.querySelector(".login-button");
  if (!loginBtn) return;

  if (isAuthenticated()) {
    loginBtn.textContent = "Logout";
    loginBtn.removeAttribute("href");
    loginBtn.style.cursor = "pointer";
    loginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      deleteCookie("token");
      window.location.href = "index.html";
    });
  }
}

/* ════════════════════════════════════════════
   TASK 01 — LOGIN PAGE
   ════════════════════════════════════════════ */

function showError(formEl, message) {
  let errEl = formEl.querySelector(".form-error");
  if (!errEl) {
    errEl = document.createElement("p");
    errEl.className = "form-error";
    formEl.appendChild(errEl);
  }
  errEl.textContent = message;
}

function clearError(formEl) {
  const errEl = formEl.querySelector(".form-error");
  if (errEl) errEl.textContent = "";
}

function initLoginPage() {
  const loginForm = document.getElementById("login-form");
  if (!loginForm) return;

  // Already logged in → skip to index
  if (isAuthenticated()) {
    window.location.href = "index.html";
    return;
  }

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearError(loginForm);

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const submitBtn = loginForm.querySelector(".submit-btn");

    submitBtn.disabled = true;
    submitBtn.textContent = "Signing in…";

    try {
      const response = await fetch(`${API_URL}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("data reçu:", data);
        setCookie("token", data.access_token);
        window.location.href = "index.html";
      } else {
        let msg = "Login failed. Please check your credentials.";
        try {
          const err = await response.json();
          if (err.message || err.error) msg = err.message || err.error;
        } catch (_) {
          /* keep default */
        }
        showError(loginForm, msg);
      }
    } catch (err) {
      showError(loginForm, "Network error — make sure the API is running.");
      console.error(err);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Sign in";
    }
  });
}

/* ════════════════════════════════════════════
   TASK 02 — INDEX PAGE
   ════════════════════════════════════════════ */

let allPlaces = [];

function initIndexPage() {
  if (!document.getElementById("places-list")) return;

  const token = getCookie("token");
  const loginLink = document.getElementById("login-link");

  if (loginLink) loginLink.style.display = "block";

  if (!token) {
    fetchPlaces(null);
  } else {
    fetchPlaces(token);
  }

  setupPriceFilter();
}

async function fetchPlaces() {
  try {
    const response = await fetch(`${API_URL}/api/v1/places`, {
      method: "GET",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      showPlacesError(`Could not load places (${response.status}).`);
      return;
    }

    allPlaces = await response.json();
    displayPlaces(allPlaces);
  } catch (err) {
    showPlacesError("Network error — make sure the API is running.");
    console.error(err);
  }
}

function displayPlaces(places) {
  const list = document.getElementById("places-list");
  if (!list) return;

  list.innerHTML = "";

  if (!places || places.length === 0) {
    list.innerHTML = '<p class="no-results">No places match your filter.</p>';
    return;
  }

  places.forEach((place) => {
    const article = document.createElement("article");
    article.className = "place-card";
    article.dataset.price = place.price;

    article.innerHTML = `
      <img src="images/places/${place.image_url || "default_place.jpg"}" alt="${place.title}" />
      <div class="place-card-body">
        <h3>${place.title}</h3>
        <p class="price">$${place.price} <span>/ night</span></p>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      </div>
    `;

    list.appendChild(article);
  });
}

function showPlacesError(message) {
  const list = document.getElementById("places-list");
  if (list) list.innerHTML = `<p class="no-results">${message}</p>`;
}

function setupPriceFilter() {
  const select = document.getElementById("price-filter");
  if (!select) return;

  select.addEventListener("change", (event) => {
    const value = event.target.value;

    if (value === "all") {
      displayPlaces(allPlaces);
      return;
    }

    const maxPrice = parseInt(value, 10);
    const filtered = allPlaces.filter((p) => p.price <= maxPrice);
    displayPlaces(filtered);
  });
}

/* ════════════════════════════════════════════
   TASK 03 — PLACE DETAILS PAGE
   ════════════════════════════════════════════ */

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function initPlacePage() {
  if (!document.getElementById("place-details")) return;

  const token = getCookie("token");
  const placeId = getPlaceIdFromURL();
  const addReviewSec = document.getElementById("add-review");

  // Show or hide add-review section based on auth
  if (!token) {
    if (addReviewSec) addReviewSec.style.display = "none";
  } else {
    if (addReviewSec) addReviewSec.style.display = "block";
  }

  if (!placeId) {
    document.getElementById("place-details").innerHTML =
      '<p class="no-results">No place ID provided. <a href="index.html">Go back</a></p>';
    return;
  }

  fetchPlaceDetails(placeId);
}

async function fetchPlaceDetails(placeId) {
  try {
    const [placeRes, reviewsRes] = await Promise.all([
      fetch(`${API_URL}/api/v1/places/${placeId}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }),
      fetch(`${API_URL}/api/v1/places/${placeId}/reviews`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }),
    ]);

    if (!placeRes.ok) {
      document.getElementById("place-details").innerHTML =
        `<p class="no-results">Could not load place details (${placeRes.status}).</p>`;
      return;
    }

    const place = await placeRes.json();
    console.log("place details:", place);
    const reviews = reviewsRes.ok ? await reviewsRes.json() : [];

    place.reviews = await Promise.all(
      reviews.map(async (r) => {
        try {
          const userRes = await fetch(`${API_URL}/api/v1/users/${r.user_id}`);
          if (userRes.ok) {
            const user = await userRes.json();
            r.user = `${user.first_name} ${user.last_name}`;
          }
        } catch (_) {
          /* ignore */
        }
        return r;
      }),
    );

    displayPlaceDetails(place);
  } catch (err) {
    document.getElementById("place-details").innerHTML =
      '<p class="no-results">Network error — make sure the API is running.</p>';
    console.error(err);
  }
}

function displayPlaceDetails(place) {
  const section = document.getElementById("place-details");
  if (!section) return;

  // Build amenities list
  const amenitiesHTML =
    place.amenities && place.amenities.length
      ? `<ul class="amenities-list">
        ${place.amenities.map((a) => `<li>${a.name || a}</li>`).join("")}
       </ul>`
      : '<p class="no-results" style="padding:0">No amenities listed.</p>';

  // Build reviews list
  const reviewsHTML =
    place.reviews && place.reviews.length
      ? place.reviews
          .map((r) => {
            const initials = (r.user || r.user_name || "U")
              .split(" ")
              .map((w) => w[0])
              .join("")
              .toUpperCase()
              .slice(0, 2);
            const stars =
              "★".repeat(r.rating || 0) + "☆".repeat(5 - (r.rating || 0));
            return `
          <article class="review-card">
            <div class="review-header">
              <div class="review-avatar">${initials}</div>
              <strong>${r.user || r.user_name || "Anonymous"}</strong>
              <span class="review-rating">${stars}</span>
            </div>
            <p>${r.text || r.comment || ""}</p>
          </article>`;
          })
          .join("")
      : '<p class="no-results" style="padding:8px 0">No reviews yet. Be the first!</p>';

  // Render full place details
  section.innerHTML = `
    <article class="place-details">
      <img
        class="place-hero"
        src="images/places/${place.image_url || "default_place.jpg"}"
        alt="${place.title}"
      />
      <div class="place-info">
        <h1>${place.title}</h1>

        <div class="place-meta">
          <span>🏠 <strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name || "N/A"}</span>
          <span>📍 <strong>Location:</strong> ${place.latitude && place.longitude ? `${place.latitude}, ${place.longitude}` : "N/A"}</span>
          ${place.max_guests ? `<span>👥 <strong>Guests:</strong> ${place.max_guests} max</span>` : ""}
          ${place.rooms ? `<span>🛏 <strong>Rooms:</strong> ${place.rooms}</span>` : ""}
        </div>

        <p class="place-price-badge">
          $${place.price} <small>/ night</small>
        </p>

        <p class="place-description">${place.description || ""}</p>

        <h2 class="amenities-title">Amenities</h2>
        ${amenitiesHTML}
      </div>
    </article>

    <section class="reviews-section">
      <h2 class="reviews-title">Guest Reviews</h2>
      ${reviewsHTML}
    </section>
  `;

  // Update the page title
  document.title = `HBnB — ${place.name}`;

  // Wire up the add-review form with the place id
  const addReviewSec = document.getElementById("add-review");
  if (addReviewSec && isAuthenticated()) {
    setupReviewForm(place.id);
  }
}

/* ════════════════════════════════════════════
   TASK 03 — REVIEW FORM (inline, in place page)
   ════════════════════════════════════════════ */

function setupReviewForm(placeId) {
  const form = document.getElementById("review-form");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const token = getCookie("token");
    const rating = form.querySelector('input[name="rating"]:checked')?.value;
    const text = document.getElementById("review-text").value.trim();
    const btn = form.querySelector(".submit-btn");

    if (!rating) {
      alert("Please select a star rating.");
      return;
    }

    btn.disabled = true;
    btn.textContent = "Submitting…";

    try {
      const response = await fetch(`${API_URL}/api/v1/reviews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          place_id: placeId,
          rating: parseInt(rating),
          text,
        }),
      });

      if (response.ok) {
        alert("Review submitted! Thank you.");
        form.reset();
        // Refresh place details to show the new review
        fetchPlaceDetails(placeId);
      } else {
        let msg = "Could not submit review.";
        try {
          const err = await response.json();
          if (err.message || err.error) msg = err.message || err.error;
        } catch (_) {
          /* keep default */
        }
        alert(msg);
      }
    } catch (err) {
      alert("Network error — make sure the API is running.");
      console.error(err);
    } finally {
      btn.disabled = false;
      btn.textContent = "Submit Review";
    }
  });
}

/* ════════════════════════════════════════════
   TASK 04 — ADD REVIEW PAGE (add_review.html)
   ════════════════════════════════════════════ */

/**
 * Submits a review to the API.
 * @param {string} token  - JWT access token
 * @param {string} placeId - UUID of the place
 * @param {number} rating  - star rating 1–5
 * @param {string} reviewText - review body
 * @returns {Response}
 */
async function submitReview(token, placeId, rating, reviewText) {
  return fetch(`${API_URL}/api/v1/reviews`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ place_id: placeId, rating, text: reviewText }),
  });
}

/**
 * Displays a feedback message inside the form container
 * (replaces any previous message).
 */
function showReviewFeedback(message, isSuccess) {
  let el = document.getElementById("review-feedback");
  if (!el) {
    el = document.createElement("p");
    el.id = "review-feedback";
    // Insert before the back-link paragraph
    const backLink = document.getElementById("back-link");
    if (backLink) backLink.before(el);
    else document.querySelector(".form-container").appendChild(el);
  }
  el.textContent = message;
  el.className = isSuccess ? "review-feedback success" : "form-error";
}

function handleResponse(response, form, token, placeId) {
  if (response.ok) {
    showReviewFeedback("✓ Review submitted successfully! Thank you.", true);
    form.reset();
    // Update back-link to return to the specific place
    const backLink = document.getElementById("back-link");
    if (backLink && placeId) {
      backLink.innerHTML = `<a href="place.html?id=${placeId}">&larr; Back to place</a>`;
    }
  } else {
    response
      .json()
      .then((err) => {
        const msg = err.message || err.error || "Failed to submit review.";
        showReviewFeedback(msg, false);
      })
      .catch(() => showReviewFeedback("Failed to submit review.", false));
  }
}

function initAddReviewPage() {
  const reviewForm = document.getElementById("review-form");
  // Only run on add_review.html (form exists but place-details does NOT)
  if (!reviewForm || document.getElementById("place-details")) return;

  // 1. Check authentication — redirect if not logged in
  const token = getCookie("token");
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  // 2. Get place ID from URL (?id=...)
  const placeId = getPlaceIdFromURL();

  // Update back-link with place id if available
  const backLink = document.getElementById("back-link");
  if (backLink && placeId) {
    backLink.innerHTML = `<a href="place.html?id=${placeId}">&larr; Back to place</a>`;
  }

  // 3. Event listener for form submission
  reviewForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const rating = reviewForm.querySelector(
      'input[name="rating"]:checked',
    )?.value;
    const reviewText = document.getElementById("review-text").value.trim();
    const btn = reviewForm.querySelector(".submit-btn");

    if (!rating) {
      showReviewFeedback("Please select a star rating.", false);
      return;
    }

    btn.disabled = true;
    btn.textContent = "Submitting…";

    try {
      // 4. AJAX POST to API
      const response = await submitReview(
        token,
        placeId,
        parseInt(rating, 10),
        reviewText,
      );
      // 5. Handle response
      handleResponse(response, reviewForm, token, placeId);
    } catch (err) {
      showReviewFeedback(
        "Network error — make sure the API is running.",
        false,
      );
      console.error(err);
    } finally {
      btn.disabled = false;
      btn.textContent = "Submit Review";
    }
  });
}

/* ════════════════════════════════════════════
   ENTRY POINT
   ════════════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {
  setupHeaderAuth();
  initLoginPage();
  initIndexPage();
  initPlacePage();
  initAddReviewPage();
});
