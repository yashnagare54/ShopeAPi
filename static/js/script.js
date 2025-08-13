document.getElementById("paymentForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    let product = document.getElementById("product").value;
    let amount = document.getElementById("amount").value;

    try {
        let response = await fetch("http://127.0.0.1:5000/create-order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"  // 👈 Important for JSON
            },
            body: JSON.stringify({
                product: product,
                amount: amount
            })
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        let data = await response.json();
        document.getElementById("message").innerText = "✅ Order Created! ID: " + data.order_id;

    } catch (error) {
        document.getElementById("message").innerText = "❌ Error: " + error.message;
    }
});
