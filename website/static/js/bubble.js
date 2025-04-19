const openModalBtn = document.querySelector(".chat-bubble");
const closeBtn = document.getElementById("closeBtn");
const overlay = document.getElementById("overlay");

openModalBtn.addEventListener("click", () => {
  overlay.style.display = "flex";
});

closeBtn.addEventListener("click", () => {
  overlay.style.display = "none";
});

window.addEventListener("click", (event) => {
  if (event.target === overlay) {
    overlay.style.display = "none";
  }
});