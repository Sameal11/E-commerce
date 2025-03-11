// document.addEventListener("DOMContentLoaded", function () {
//     // Fetch cart data (assuming stored in localStorage)
//     let cart = JSON.parse(localStorage.getItem("cart")) || [];

//     // Select elements
//     const orderSummaryTable = document.querySelector("tbody");
//     const subtotalElement = document.getElementById("subtotal");
//     const totalElement = document.getElementById("total");

//     let subtotal = 0;
//     let shipping = 5.00; // Fixed shipping cost

//     // Populate the order summary table
//     orderSummaryTable.innerHTML = "";
//     cart.forEach(item => {
//         let row = document.createElement("tr");
//         row.innerHTML = `
//             <td>${item.name}</td>
//             <td>${item.quantity}</td>
//             <td>$${(item.price * item.quantity).toFixed(2)}</td>
//         `;
//         orderSummaryTable.appendChild(row);

//         // Calculate subtotal
//         subtotal += item.price * item.quantity;
//     });

//     // Update totals
//     subtotalElement.textContent = subtotal.toFixed(2);
//     totalElement.textContent = (subtotal + shipping).toFixed(2);

//     // Handle form submission
//     document.getElementById("order-form").addEventListener("submit", function (event) {
//         event.preventDefault();

//         // Collect user input
//         const orderData = {
//             name: document.getElementById("name").value,
//             address: document.getElementById("address").value,
//             city: document.getElementById("city").value,
//             state: document.getElementById("state").value,
//             zip: document.getElementById("zip").value,
//             email: document.getElementById("email").value,
//             cart: cart,
//             total: (subtotal + shipping).toFixed(2)
//         };

//         console.log("Order placed:", orderData);

//         // Send order data to the server
//         fetch("/submit_order", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify(orderData)
//         })
//         .then(response => response.json())
//         .then(data => {
//             alert("Order placed successfully!");
//             localStorage.removeItem("cart"); // Clear cart after order
//             window.location.href = "/order_success"; // Redirect to success page
//         })
//         .catch(error => console.error("Error placing order:", error));
//     });
// });
