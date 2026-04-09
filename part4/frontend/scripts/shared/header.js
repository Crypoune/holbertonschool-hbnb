/* =============================================
   HBnB — shared/header.js
   Logique du header (auth, logout)
   ============================================= */
import { getCookie, deleteCookie, isAuthenticated } from "../auth/cookie.js";

export function setupHeaderAuth() {
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
