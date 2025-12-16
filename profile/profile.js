const profileInfo = document.getElementById("profile-info");
const profilePic = document.getElementById("profile-pic");
const user = JSON.parse(localStorage.getItem("loggedInUser"));

if (user && profileInfo) {
  const fname = user.fname || user.first_name || "";
  const lname = user.lname || user.last_name || "";
  profileInfo.innerHTML = `
    <p><strong>Name:</strong> ${fname} ${lname}</p>
    <p><strong>Age:</strong> ${user.age || ""}</p>
    <p><strong>Email:</strong> ${user.email}</p>
  `;

  // Load saved profile pic if exists
  const savedPic = localStorage.getItem("profilePic");
  if (savedPic) {
    profilePic.src = savedPic;
  }
} else {
  profileInfo.innerHTML = "<p>No user logged in</p>";
}

// Edit profile picture
function editProfilePic() {
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "image/*";
  
  fileInput.onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(event) {
        profilePic.src = event.target.result;
        localStorage.setItem("profilePic", event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  fileInput.click();
}

function logout() {
  localStorage.removeItem("loggedInUser");
  localStorage.removeItem("profilePic");
  window.location.href = "../login/login.html";
}