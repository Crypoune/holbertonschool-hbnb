/* =============================================
   HBnB — reviews/addReview.js
   Logique de la page dédiée à l'ajout de review
   ============================================= */
import { getCookie, isAuthenticated } from "../auth/cookie.js";
import { API_URL } from "../shared/utils.js";

export async function submitReview(token, placeId, rating, reviewText) {
  return fetch(`${API_URL}/api/v1/reviews`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ place_id: placeId, rating, text: reviewText }),
  });
}

export function showReviewFeedback(message, isSuccess) {
  let el = document.getElementById("review-feedback");
  if (!el) {
    el = document.createElement("p");
    el.id = "review-feedback";
    const backLink = document.getElementById("back-link");
    if (backLink) backLink.before(el);
    else document.querySelector(".form-container").appendChild(el);
  }
  el.textContent = message;
  el.className = isSuccess ? "review-feedback success" : "form-error";
}

export function handleResponse(response, form, token, placeId) {
  if (response.ok) {
    showReviewFeedback("✓ Review submitted successfully! Thank you.", true);
    form.reset();
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

export function initAddReviewPage() {
  const reviewForm = document.getElementById("review-form");
  if (!reviewForm || document.getElementById("place-details")) return;

  const token = getCookie("token");
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  const placeId = getPlaceIdFromURL();
  const backLink = document.getElementById("back-link");
  if (backLink && placeId) {
    backLink.innerHTML = `<a href="place.html?id=${placeId}">&larr; Back to place</a>`;
  }

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
      const response = await submitReview(
        token,
        placeId,
        parseInt(rating, 10),
        reviewText,
      );
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

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}
