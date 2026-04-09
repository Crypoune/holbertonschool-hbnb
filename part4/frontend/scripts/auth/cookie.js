/* =============================================
   HBnB — auth/cookie.js
   Gestion des cookies (authentification)
   ============================================= */

export function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

export function setCookie(name, value, days = 7) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${value}; path=/; expires=${expires}; SameSite=Lax`;
}

export function deleteCookie(name) {
  document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
}

export function isAuthenticated() {
  return !!getCookie("token");
}
