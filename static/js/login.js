function togglePasswordVisibility() {
  const input = document.getElementById("password");
  const icon = document.getElementById("eye-icon");
  const isPassword = input.type === "password";

  input.type = isPassword ? "text" : "password";

  if (isPassword) {
    icon.innerHTML =
      '<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"></path><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"></path><path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"></path><path d="m2 2 20 20"></path>';
  } else {
    icon.innerHTML =
      '<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path><circle cx="12" cy="12" r="3"></circle>';
  }
}

// Limpar erros quando o usuário focar em um input
document.querySelectorAll("input").forEach(function (input) {
  input.addEventListener("focus", function () {
    document.getElementById("errorContainer").textContent = "";
  });
});
function togglePasswordVisibility() {
  const input = document.getElementById("password");
  const icon = document.getElementById("eye-icon");
  const isPassword = input.type === "password";

  input.type = isPassword ? "text" : "password";

  if (isPassword) {
    icon.innerHTML =
      '<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"></path><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"></path><path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"></path><path d="m2 2 20 20"></path>';
  } else {
    icon.innerHTML =
      '<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path><circle cx="12" cy="12" r="3"></circle>';
  }
}
var errorsDivs = document.getElementsByClassName("errors");
document.querySelectorAll("input").forEach(function (input) {
  input.addEventListener("focus", function () {
    console.log(`Input ${input.name} recebeu foco!`);
    Array.from(errorsDivs).forEach(function (div) {
      div.textContent = "";
    });
  });
});
