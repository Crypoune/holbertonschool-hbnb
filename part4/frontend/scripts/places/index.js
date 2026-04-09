/* =============================================
   HBnB — places/index.js
   Logique de la page d'accueil (liste des places)
   ============================================= */
import { getCookie } from "../auth/cookie.js";
import { API_URL } from "../shared/utils.js";

let allPlaces = [];

export function initIndexPage() {
  if (!document.getElementById("places-list")) return;

  const token = getCookie("token");
  const loginLink = document.getElementById("login-link");

  if (loginLink) loginLink.style.display = "block";

  fetchPlaces();
  setupPriceFilter();
}

export async function fetchPlaces() {
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

export function displayPlaces(places) {
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

export function showPlacesError(message) {
  const list = document.getElementById("places-list");
  if (list) list.innerHTML = `<p class="no-results">${message}</p>`;
}

export function setupPriceFilter() {
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
