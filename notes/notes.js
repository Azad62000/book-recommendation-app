function saveNote() {
  const noteBox = document.getElementById("noteBox");
  let notes = JSON.parse(localStorage.getItem("notes")) || [];
  notes.push(noteBox.value);
  localStorage.setItem("notes", JSON.stringify(notes));
  displayNotes();
}

function displayNotes() {
  const savedNotes = document.getElementById("savedNotes");
  let notes = JSON.parse(localStorage.getItem("notes")) || [];
  savedNotes.innerHTML = "";
  notes.forEach((note, index) => {
    let div = document.createElement("div");
    div.innerHTML = `<p>${note}</p><hr>`;
    savedNotes.appendChild(div);
  });
}

displayNotes();