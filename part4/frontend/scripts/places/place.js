/* =============================================
   HBnB — places/place.js
   Logique de la page de détail d'une place
   ============================================= */
import { getCookie, isAuthenticated } from "../auth/cookie.js";
import { API_URL } from "../shared/utils.js";
import { setupReviewForm } from "../reviews/reviewForm.js";

export function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

export function initPlacePage() {
  if (!document.getElementById("place-details")) return;

  const token = getCookie("token");
  const placeId = getPlaceIdFromURL();
  const addReviewSec = document.getElementById("add-review");
  const loginPromptSec = document.getElementById("login-prompt");

  if (!token) {
    if (addReviewSec) addReviewSec.style.display = "none";
    if (loginPromptSec) loginPromptSec.style.display = "block";
  } else {
    if (addReviewSec) addReviewSec.style.display = "block";
    if (loginPromptSec) loginPromptSec.style.display = "none";
  }

  if (!placeId) {
    document.getElementById("place-details").innerHTML =
      '<p class="no-results">No place ID provided. <a href="index.html">Go back</a></p>';
    return;
  }

  fetchPlaceDetails(placeId);
}

export async function fetchPlaceDetails(placeId) {
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
    const reviews = reviewsRes.ok ? await reviewsRes.json() : [];

    place.reviews = await Promise.all(
      reviews.map(async (r) => {
        try {
          const userRes = await fetch(`${API_URL}/api/v1/users/${r.user_id}`);
          if (userRes.ok) {
            const user = await userRes.json();
            r.user = `${user.first_name} ${user.last_name}`;
          }
        } catch (_) {}
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

export function displayPlaceDetails(place) {
  const section = document.getElementById("place-details");
  if (!section) return;

  const amenitiesHTML =
    place.amenities && place.amenities.length
      ? `<ul class="amenities-list">
        ${place.amenities.map((a) => `<li>${a.image_url ? `<img src="images/amenities/${a.image_url}" alt="${a.name}" />` : ""}${a.name || a}</li>`).join("")}
       </ul>`
      : '<p class="no-results" style="padding:0">No amenities listed.</p>';

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

  document.title = `HBnB — ${place.name}`;

  const addReviewSec = document.getElementById("add-review");
  const loginPromptSec = document.getElementById("login-prompt");

  if (isAuthenticated()) {
    if (addReviewSec) addReviewSec.style.display = "block";
    if (loginPromptSec) loginPromptSec.style.display = "none";
    setupReviewForm(place.id);
  } else {
    if (addReviewSec) addReviewSec.style.display = "none";
    if (loginPromptSec) loginPromptSec.style.display = "block";
  }
}
