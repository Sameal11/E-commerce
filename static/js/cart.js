document.addEventListener("DOMContentLoaded", function () {
    // Function to update the cart quantity
    const updateCartQuantity = (itemName) => {
        const quantityInput = document.querySelector(`input[name="quantity_${itemName}"]`);
        const newQuantity = quantityInput.value;

        fetch(`/update_cart/${itemName}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ quantity: newQuantity }),
        })
        .then(response => {
            if (response.ok) {
                window.location.reload(); // Reload the cart page to reflect changes
            } else {
                alert("Failed to update quantity.");
            }
        });
    };

    // Function to remove an item from the cart
    const removeFromCart = (itemName) => {
        fetch(`/remove_from_cart/${itemName}`)
        .then(response => {
            if (response.ok) {
                window.location.reload(); // Reload the cart page to reflect changes
            } else {
                alert("Failed to remove item from cart.");
            }
        });
    };

    // Attach event listeners to update buttons
    const updateButtons = document.querySelectorAll(".update-cart");
    updateButtons.forEach(button => {
        button.addEventListener("click", function () {
            const itemName = this.dataset.itemName;
            updateCartQuantity(itemName);
        });
    });

    // Attach event listeners to remove buttons
    const removeButtons = document.querySelectorAll(".remove-from-cart");
    removeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const itemName = this.dataset.itemName;
            removeFromCart(itemName);
        });
    });
});