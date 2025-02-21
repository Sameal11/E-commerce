document.addEventListener("DOMContentLoaded", function () {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    function updateCart() {
        let cartTable = document.getElementById("cart-items");
        let subtotal = 0;
        cartTable.innerHTML = "";

        if (cart.length === 0) {
            cartTable.innerHTML = "<tr><td colspan='5' class='text-center'>Your cart is empty</td></tr>";
        } else {
            cart.forEach((item, index) => {
                let total = item.price * item.quantity;
                subtotal += total;

                cartTable.innerHTML += `
                    <tr>
                        <td>${item.name}</td>
                        <td>$${item.price.toFixed(2)}</td>
                        <td>
                            <input type="number" class="form-control" value="${item.quantity}" min="1" onchange="updateQuantity(${index}, this.value)">
                        </td>
                        <td>$${total.toFixed(2)}</td>
                        <td><button class="btn btn-danger btn-sm" onclick="removeFromCart(${index})">X</button></td>
                    </tr>
                `;
            });
        }

        document.getElementById("subtotal").innerText = subtotal.toFixed(2);
        localStorage.setItem("cart", JSON.stringify(cart));
    }

    window.updateQuantity = function (index, quantity) {
        if (quantity < 1) return;
        cart[index].quantity = parseInt(quantity);
        updateCart();
    };

    window.removeFromCart = function (index) {
        cart.splice(index, 1);
        updateCart();
    };

    document.getElementById("checkoutBtn")?.addEventListener("click", function () {
        if (cart.length === 0) {
            alert("Your cart is empty!");
        } else {
            alert("Proceeding to checkout...");
            localStorage.removeItem("cart");
            window.location.href = "checkout.html"; // Redirect to checkout page
        }
    });

    updateCart();

    // Scroll to Top functionality
    const scrollToTopBtn = document.getElementById("scrollToTopBtn");

    if (scrollToTopBtn) {
        window.addEventListener("scroll", function () {
            scrollToTopBtn.style.display = window.scrollY > 300 ? "block" : "none";
        });

        scrollToTopBtn.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
});
