const API_BASE = "http://localhost:8000";
const grid = document.getElementById("popular-grid");

async function loadPopularAll() {
  try {
    const res = await fetch(`${API_BASE}/books/popular?limit=50`);
    const books = await res.json();
    grid.innerHTML = "";
    books.forEach(book => {
      const div = document.createElement("div");
      div.classList.add("book-card");
      div.innerHTML = `
        <img src="${book.image}" alt="${book.title}">
        <h4>${book.title}</h4>
      `;
      grid.appendChild(div);
    });
  } catch (e) {
    grid.innerHTML = "<p style='margin-left:20px;'>Failed to load popular books.</p>";
  }
}

loadPopularAll();