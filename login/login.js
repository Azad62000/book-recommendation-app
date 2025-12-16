const API_BASE = "http://localhost:8000";
async function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById("login-username").value;
  const pass = document.getElementById("login-password").value;
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password: pass })
    });
    if (!res.ok) {
      alert("Invalid credentials!");
      return;
    }
    const user = await res.json();
    localStorage.setItem("loggedInUser", JSON.stringify(user));
    alert("Login successful!");
    window.location.href = "../profile/profile.html";
  } catch (err) {
    alert("Network error. Try again.");
  }
}