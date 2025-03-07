document.addEventListener("DOMContentLoaded", function () {
    const categoryBtn = document.getElementById("categoryBtn");
    const categorySlider = document.getElementById("categorySlider");
    const profileBtn = document.querySelector(".profile");
    const profilePanel = document.getElementById("profilePanel");

    // Category Slider Toggle
    if (categoryBtn && categorySlider) {
        categoryBtn.addEventListener("click", function (event) {
            event.stopPropagation(); // Prevents closing immediately
            categorySlider.classList.toggle("show");
        });
    }

    // Profile Panel Toggle
    if (profileBtn && profilePanel) {
        profileBtn.addEventListener("click", function (event) {
            event.stopPropagation(); // Prevents closing immediately
            profilePanel.classList.toggle("show");
        });
    }

    // Close panels when clicking outside
    document.addEventListener("click", function (event) {
        if (categorySlider && !categoryBtn.contains(event.target) && !categorySlider.contains(event.target)) {
            categorySlider.classList.remove("show");
        }
        if (profilePanel && !profileBtn.contains(event.target) && !profilePanel.contains(event.target)) {
            profilePanel.classList.remove("show");
        }
    });
});
