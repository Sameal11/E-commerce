document.addEventListener("DOMContentLoaded", function () {
    let wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    function updateWishlist() {
        let wishlistTable = document.getElementById("wishlist-items");
        wishlistTable.innerHTML = "";

        if (wishlist.length === 0) {
            wishlistTable.innerHTML = "<tr><td colspan='4' class='text-center'>Your wishlist is empty</td></tr>";
        } else {
            wishlist.forEach((item, index) => {
                let row = document.createElement("tr");

                let nameCell = document.createElement("td");
                nameCell.textContent = item.name;
                
                let priceCell = document.createElement("td");
                priceCell.textContent = `$${item.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}`;

                let moveToCartCell = document.createElement("td");
                let moveToCartButton = document.createElement("button");
                moveToCartButton.textContent = "Move to Cart";
                moveToCartButton.classList.add("btn", "btn-success", "btn-sm");
                moveToCartButton.onclick = function () {
                    moveToCart(index);
                };
                moveToCartCell.appendChild(moveToCartButton);

                let removeCell = document.createElement("td");
                let removeButton = document.createElement("button");
                removeButton.textContent = "X";
                removeButton.classList.add("btn", "btn-danger", "btn-sm");
                removeButton.onclick = function () {
                    removeFromWishlist(index);
                };
                removeCell.appendChild(removeButton);

                row.appendChild(nameCell);
                row.appendChild(priceCell);
                row.appendChild(moveToCartCell);
                row.appendChild(removeCell);

                wishlistTable.appendChild(row);
            });
        }

        localStorage.setItem("wishlist", JSON.stringify(wishlist));
    }

    function moveToCart(index) {
        let item = wishlist[index];
        cart.push(item);
        wishlist.splice(index, 1);
        localStorage.setItem("cart", JSON.stringify(cart));
        localStorage.setItem("wishlist", JSON.stringify(wishlist));
        updateWishlist();
        updateCart(); // Ensure cart updates in UI if needed
    }

    function removeFromWishlist(index) {
        wishlist.splice(index, 1);
        localStorage.setItem("wishlist", JSON.stringify(wishlist));
        updateWishlist();
    }

    function updateCart() {
        // Implement cart update logic if needed
    }

    updateWishlist();
});
