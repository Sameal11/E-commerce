function fetchTopProduct() {
    fetch("/top-product")
        .then(response => response.json())
        .then(product => {
            document.getElementById("topProductName").innerText = product.name;
            document.getElementById("topProductImage").src = "{{ url_for('static', filename='') }}" + product.image;
            document.getElementById("topProductPrice").innerText = "₹" + product.price;
        })
        .catch(error => console.error("Error fetching top product:", error));
}

// Fetch new top product every 2 seconds
setInterval(fetchTopProduct, 2000);

// Fetch the first top product when the page loads
fetchTopProduct();