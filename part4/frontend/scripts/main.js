/* =============================================
   HBnB — main.js
   Point d'entrée principal
   ============================================= */
import { setupHeaderAuth } from "./shared/header.js";
import { initLoginPage } from "./auth/login.js";
import { initIndexPage } from "./places/index.js";
import { initPlacePage } from "./places/place.js";
import { initAddReviewPage } from "./reviews/addReview.js";

document.addEventListener("DOMContentLoaded", () => {
  setupHeaderAuth();
  initLoginPage();
  initIndexPage();
  initPlacePage();
  initAddReviewPage();
});
