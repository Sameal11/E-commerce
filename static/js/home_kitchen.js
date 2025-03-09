document.addEventListener("DOMContentLoaded", function () {
    const productCards = document.querySelectorAll(".product-card");

    productCards.forEach(card => {
        card.addEventListener("mouseover", function () {
            this.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
        });

        card.addEventListener("mouseout", function () {
            this.style.boxShadow = "none";
        });
    });
});
