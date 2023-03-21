const clouds = document.querySelector(".clouds");

window.addEventListener("scroll", () => {
  const win = window.pageYOffset;

  if (win > 1901) {
    clouds.style.height = 146 - +win / 50 + "%";
  }
});

const sidebar = document.querySelector(".sidebar");
const toggle = document.querySelector(".toggle");
const toggleDiv = document.querySelector(".toggle div");
const body = document.body;
let showMenu = false;

toggle.addEventListener("click", () => {
  if (!showMenu) {
    sidebar.classList.add("open");
    toggleDiv.classList.add("open");
    body.classList.add("fix");
  } else {
    sidebar.classList.remove("open");
    toggleDiv.classList.remove("open");
    body.classList.remove("fix");
  }

  showMenu = !showMenu;
});
