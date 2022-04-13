const elBody = document.getElementsByTagName("body")[0];
const btnTheme = document.getElementById("change_theme");
var theme = localStorage.getItem("theme") || "LIGHT";
changeTheme();

btnTheme.onclick = (e) => {
  theme = theme === "DARK" ? "LIGHT" : "DARK";
  localStorage.setItem("theme", theme);
  changeTheme();
};

function changeTheme() {
  if (theme === "DARK") {
    elBody.classList.add("dark");
    btnTheme.innerHTML = '<i class="fa-solid fa-sun fa-2x"></i>';
  } else {
    elBody.classList.remove("dark");
    btnTheme.innerHTML = '<i class="fa-solid fa-moon fa-2x"></i>';
  }
}


