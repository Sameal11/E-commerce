document.addEventListener("DOMContentLoaded", function () {
    const categoryBtn = document.getElementById("categoryBtn");
    const categorySlider = document.getElementById("categorySlider");

    if (categoryBtn && categorySlider) {
        categoryBtn.addEventListener("click", function () {
            categorySlider.classList.toggle("show");
        });

        // Close slider when clicking outside
        document.addEventListener("click", function (event) {
            if (!categoryBtn.contains(event.target) && !categorySlider.contains(event.target)) {
                categorySlider.classList.remove("show");
            }
        });
    }
});
