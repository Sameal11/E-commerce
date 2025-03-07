document.addEventListener("DOMContentLoaded", function () {
    const profileBtn = document.getElementById("profileBtn");
    const profilePanel = document.getElementById("profilePanel");

    if (profileBtn && profilePanel) {
        profileBtn.addEventListener("click", function (event) {
            event.stopPropagation();
            profilePanel.classList.toggle("show");
        });

        // Close panel when clicking outside
        document.addEventListener("click", function (event) {
            if (!profileBtn.contains(event.target) && !profilePanel.contains(event.target)) {
                profilePanel.classList.remove("show");
            }
        });
    }
});
