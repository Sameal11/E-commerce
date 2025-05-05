document.addEventListener("DOMContentLoaded", function () {
    const cardOption = document.getElementById("card-option");
    const upiOptions = ["gpay-option", "phonepe-option", "paytm-option"];
    const cardDetails = document.getElementById("card-details");
    const upiDetails = document.getElementById("upi-details");
    const paymentMethods = document.querySelectorAll("input[name='payment-method']");
    const payBtn = document.getElementById("pay-btn");
    const message = document.getElementById("message");

    // Hide details by default
    cardDetails.style.display = "none";
    upiDetails.style.display = "none";

    // Add event listener to all payment methods
    paymentMethods.forEach(method => {
        method.addEventListener("change", function () {
            if (cardOption.checked) {
                cardDetails.style.display = "block";
                upiDetails.style.display = "none"; // Hide UPI if card is selected
            } else if (upiOptions.includes(method.id)) {
                cardDetails.style.display = "none"; // Hide card details
                upiDetails.style.display = "block"; // Show UPI input
            } else {
                cardDetails.style.display = "none";
                upiDetails.style.display = "none"; // Hide everything for other methods
            }
        });
    });

    // Handle payment confirmation
    payBtn.addEventListener("click", function () {
        const selectedMethod = document.querySelector("input[name='payment-method']:checked");

        if (!selectedMethod) {
            message.innerHTML = `<span style="color: red;">Please select a payment method!</span>`;
            return;
        }

        let reward = (Math.random() * 100).toFixed(2); // Generate random cash under $100

        message.innerHTML = `<span style="color: green; font-size: 18px;">
            ✅ Payment successful! You have received a cashback of $${reward} 🎉
        </span>`;

        // Disable the button after payment
        payBtn.disabled = true;
    });
});

    document.querySelectorAll('input[name="payment-method"]').forEach((radio) => {
        radio.addEventListener('change', function () {
            if (this.value === 'card') {
                cardDetails.style.display = 'block';
                upiDetails.style.display = 'none';
            } else if (upiOptions.includes(this.id)) {
                upiDetails.style.display = 'block';
                cardDetails.style.display = 'none';
            } else {
                cardDetails.style.display = 'none';
                upiDetails.style.display = 'none';
            }
        });
    });