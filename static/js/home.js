document.addEventListener("DOMContentLoaded", function () {
    const products = [
        { name: "Product 1", image: "product1.jpg", price: "$19.99" },
        { name: "Product 2", image: "product2.jpg", price: "$24.99" },
        { name: "Product 3", image: "product3.jpg", price: "$29.99" },
        { name: "Product 4", image: "product4.jpg", price: "$34.99" }
    ];

    let currentIndex = 0;
    const topProductBox = document.getElementById("topProductBox");

    function updateTopProduct() {
        const product = products[currentIndex];

        // Create new product element
        const newProduct = document.createElement("div");
        newProduct.classList.add("product-slide", "slide-in");
        newProduct.innerHTML = `
            <div class="card text-center">
                <img src="/static/images/${product.image}" class="card-img-top" alt="${product.name}">
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">${product.price}</p>
                    <a href="#" class="btn btn-primary">Buy Now</a>
                </div>
            </div>
        `;

        // Add new product to the box
        topProductBox.appendChild(newProduct);

        // Wait for animation to complete, then remove old product
        setTimeout(() => {
            const oldProduct = document.querySelector(".product-slide");
            if (oldProduct) {
                oldProduct.classList.add("slide-out");
                setTimeout(() => oldProduct.remove(), 500); // Remove after animation
            }
        }, 4000);

        // Move to the next product
        currentIndex = (currentIndex + 1) % products.length;
    }

    updateTopProduct(); // Show first product immediately
    setInterval(updateTopProduct, 5000); // Change product every 5 seconds
});
