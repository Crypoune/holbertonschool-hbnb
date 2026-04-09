/* =============================================
   HBnB — reviews/reviewForm.js
   Logique du formulaire d'ajout de review (inline)
   ============================================= */
import { getCookie } from "../auth/cookie.js";
import { API_URL } from "../shared/utils.js";

export function setupReviewForm(placeId) {
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
        // Rafraîchir les détails de la place pour afficher la nouvelle review
        window.location.reload();
      } else {
        let msg = "Could not submit review.";
        try {
          const err = await response.json();
          if (err.message || err.error) msg = err.message || err.error;
        } catch (_) {}
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
