const API_BASE = (window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1")
  ? `${window.location.protocol}//${window.location.host}`
  : "http://localhost:8000";
const popularTitle = document.getElementById("popularTitle");
const recommendTitle = document.getElementById("recommendTitle");
let currentIndex = 0;
const slider = document.getElementById("book-slider");
let popularBooks = [];
const popularGrid = document.getElementById("popular-grid");
const viewAllBtn = document.getElementById("viewAllBtn");
const recommendBox = document.getElementById("recommend-box");

async function loadPopular() {
  try {
    const res = await fetch(`${API_BASE}/books/popular?limit=20`);
    popularBooks = await res.json();
    renderSlider();
  } catch (e) {
    popularBooks = [];
    renderSlider();
  }
}

function renderSlider() {
  slider.innerHTML = "";
  const visibleBooks = popularBooks.slice(currentIndex, currentIndex + 5);
  if (visibleBooks.length > 0) {
    popularTitle.style.display = "block";
  }
  visibleBooks.forEach(book => {
    const div = document.createElement("div");
    div.classList.add("book-card");
    div.innerHTML = `
      <img src="${book.image}" alt="${book.title}">
      <h4>${book.title}</h4>
    `;
    div.onclick = () => addRecommendation(book.title);
    slider.appendChild(div);
  });
}

document.getElementById("nextBtn").onclick = () => {
  if (currentIndex < 10) currentIndex += 5;
  renderSlider();
};
document.getElementById("prevBtn").onclick = () => {
  if (currentIndex > 0) currentIndex -= 5;
  renderSlider();
};

loadPopular();

if (viewAllBtn) {
  viewAllBtn.onclick = async () => {
    try {
      const res = await fetch(`${API_BASE}/books/popular?limit=50`);
      const all = await res.json();
      popularGrid.innerHTML = "";
      all.forEach(book => {
        const div = document.createElement("div");
        div.classList.add("book-card");
        div.innerHTML = `
          <img src="${book.image}" alt="${book.title}">
          <h4>${book.title}</h4>
        `;
        div.onclick = () => addRecommendation(book.title);
        popularGrid.appendChild(div);
      });
    } catch (e) {}
  };
}

const searchBox = document.getElementById("searchBox");
searchBox.addEventListener("input", async function() {
  const value = this.value.toLowerCase();
  const results = document.getElementById("search-results");
  results.innerHTML = "";
  if (value.length > 0) {
    try {
      const res = await fetch(`${API_BASE}/books/search?q=${encodeURIComponent(value)}&limit=10`);
      const filtered = await res.json();
      filtered.forEach(book => {
        const div = document.createElement("div");
        div.classList.add("book-card");
        div.innerHTML = `
          <img src="${book.image}" alt="${book.title}">
          <h4>${book.title}</h4>
        `;
        div.onclick = () => addRecommendation(book.title);
        results.appendChild(div);
      });
    } catch (e) {}
  }
});

async function addRecommendation(title) {
  recommendTitle.style.display = "block";
  const recommended = document.getElementById("recommended-books");
  recommended.innerHTML = "";
  try {
    const res = await fetch(`${API_BASE}/recommend/by-title?title=${encodeURIComponent(title)}&limit=8`);
    const books = await res.json();
    if (!books || books.length === 0) {
      if (recommendBox) recommendBox.textContent = "";
      return;
    }
    if (recommendBox) recommendBox.textContent = "";
    books.forEach(book => {
      const div = document.createElement("div");
      div.classList.add("book-card");
      div.innerHTML = `
        <img src="${book.image}" alt="${book.title}">
        <h4>${book.title}</h4>
      `;
      recommended.appendChild(div);
    });
  } catch (e) {}
}

const recommendBtn = document.getElementById("recommendBtn");
if (recommendBtn) {
  recommendBtn.onclick = async () => {
    const q = searchBox.value.trim();
    if (!q) return;
    try {
      const res = await fetch(`${API_BASE}/books/search?q=${encodeURIComponent(q)}&limit=1`);
      const arr = await res.json();
      if (arr && arr.length > 0) {
        await addRecommendation(arr[0].title);
      } else {
        if (recommendBox) recommendBox.textContent = "";
      }
    } catch (e) {}
  };
}