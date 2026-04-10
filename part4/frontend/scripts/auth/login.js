/* =============================================
   HBnB — auth/login.js
   Login logic
   ============================================= */
import { getCookie, setCookie, isAuthenticated } from "./cookie.js";
import { API_URL } from "../shared/utils.js";

export function showError(formEl, message) {
  let errEl = formEl.querySelector(".form-error");
  if (!errEl) {
    errEl = document.createElement("p");
    errEl.className = "form-error";
    formEl.appendChild(errEl);
  }
  errEl.textContent = message;
}

export function clearError(formEl) {
  const errEl = formEl.querySelector(".form-error");
  if (errEl) errEl.textContent = "";
}

export function initLoginPage() {
  const loginForm = document.getElementById("login-form");
  if (!loginForm) return;

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
        setCookie("token", data.access_token);
        window.location.href = "index.html";
      } else {
        let msg = "Login failed. Please check your credentials.";
        try {
          const err = await response.json();
          if (err.message || err.error) msg = err.message || err.error;
        } catch (_) {}
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
