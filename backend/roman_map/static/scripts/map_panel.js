document.addEventListener("DOMContentLoaded", function () {
    // Megkeressük a panelt és a gombot
    var panel = document.getElementById("panel");
    var toggleBtn = document.getElementById("panel-toggle-btn");

    // Hozzáadjuk a kattintásfigyelőt
    toggleBtn.addEventListener("click", function () {
        panel.classList.toggle("open"); // Ha rajta van, leveszi; ha nincs, hozzáadja
    });
});