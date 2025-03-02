   document.addEventListener("DOMContentLoaded", function () {
        // Select all "Add to Cart" buttons
        const cartButtons = document.querySelectorAll(".add-to-cart");
        const wishlistButtons = document.querySelectorAll(".add-to-wishlist");
    
        cartButtons.forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.dataset.productId;
                addToCart(productId);
            });
        });
    
        wishlistButtons.forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.dataset.productId;
                addToWishlist(productId);
            });
        });
    
        function addToCart(productId) {
            fetch("/add-to-cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ product_id: productId })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => console.error("Error:", error));
        }
    
        function addToWishlist(productId) {
            fetch("/add-to-wishlist", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ product_id: productId })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => console.error("Error:", error));
        }
    });

