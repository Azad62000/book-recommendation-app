const API_BASE = (window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1")
  ? `${window.location.protocol}//${window.location.host}`
  : "http://localhost:8000";
document.getElementById("signupForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document.getElementById("confirmPassword").value.trim();
  const errorMsg = document.getElementById("error-msg");
  errorMsg.textContent = "";
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailPattern.test(email)) {
    errorMsg.textContent = "Please enter a valid email address (e.g. aa12@gmail.com).";
    return;
  }
  const passPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  if (!passPattern.test(password)) {
    errorMsg.textContent = "Password must be at least 8 characters, include uppercase, lowercase, number, and a special character.";
    return;
  }
  if (password !== confirmPassword) {
    errorMsg.textContent = "Passwords do not match.";
    return;
  }
  const body = {
    first_name: document.getElementById("firstName").value.trim(),
    last_name: document.getElementById("lastName").value.trim(),
    age: parseInt(document.getElementById("age").value.trim(), 10),
    email: email,
    password: password
  };
  try {
    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      errorMsg.textContent = data.detail || "Signup failed.";
      return;
    }
    alert("Signup successful! Redirecting to login...");
    window.location.href = "../login/login.html";
  } catch (err) {
    errorMsg.textContent = "Network error. Try again.";
  }
});