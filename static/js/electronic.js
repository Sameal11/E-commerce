document.addEventListener("DOMContentLoaded", function () {
    // Select all "Add to Cart" and "Add to Wishlist" buttons
    const cartButtons = document.querySelectorAll(".add-to-cart");
    const wishlistButtons = document.querySelectorAll(".add-to-wishlist");

    // Add to Cart event listener
    cartButtons.forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.dataset.productId;
            if (productId) addToCart(productId);
        });
    });

    // Add to Wishlist event listener
    wishlistButtons.forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.dataset.productId;
            if (productId) addToWishlist(productId);
        });
    });

    // Function to add product to cart
    function addToCart(productId) {
        fetch("/add_to_cart", {  // Ensure route matches Flask endpoint
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || "Added to cart successfully!");
        })
        .catch(error => {
            console.error("Error adding to cart:", error);
            alert("Error adding to cart. Please try again.");
        });
    }

    // Function to add product to wishlist
    function addToWishlist(productId) {
        fetch("/add_to_wishlist", {  // Ensure route matches Flask endpoint
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || "Added to wishlist successfully!");
        })
        .catch(error => {
            console.error("Error adding to wishlist:", error);
            alert("Error adding to wishlist. Please try again.");
        });
    }
});
