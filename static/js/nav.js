var nav = document.getElementById("nav");
var menu = document.getElementById("menu");

menu.addEventListener("click", function (e) {
    e.stopPropagation(); // prevent body click from firing immediately
    nav.classList.toggle("show-nav");
});

document.addEventListener("click", function (e) {
    if (!nav.contains(e.target) && e.target !== menu) {
        nav.classList.remove("show-nav");
    }
});