from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time

app = Flask(__name__, template_folder="templates")
CORS(app)

ORDERS = {}
PAYMENTS = {}
_order_counter = 0
_payment_counter = 0

def next_order_id():
    global _order_counter
    _order_counter += 1
    return f"order_mock_{_order_counter:06d}"

def next_payment_id():
    global _payment_counter
    _payment_counter += 1
    return f"pay_mock_{_payment_counter:06d}"

@app.route("/")
def home():
    # serves templates/index.html
    return render_template("index.html")

@app.route("/create_order", methods=["POST"])
def create_order():
    ctype = (request.headers.get('Content-Type') or "").lower()
    if "application/json" in ctype:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict() or {}

    amount = data.get("amount") or data.get("amount_rupees") or 100
    try:
        amount = int(amount)
    except:
        amount = 100

    order_id = next_order_id()
    order = {
        "id": order_id,
        "amount_rupees": amount,
        "amount_paise": amount * 100,
        "status": "CREATED",
        "created_at": time.time(),
        "meta": { "name": data.get("name"), "email": data.get("email") }
    }
    ORDERS[order_id] = order
    print("Created order:", order_id)
    return jsonify(order), 201

@app.route("/confirm_payment", methods=["POST"])
def confirm_payment():
    ctype = (request.headers.get('Content-Type') or "").lower()
    if "application/json" in ctype:
        payload = request.get_json(silent=True) or {}
    else:
        payload = request.form.to_dict() or {}

    order_id = payload.get("order_id")
    result = (payload.get("result") or "success").lower()
    if not order_id or order_id not in ORDERS:
        return jsonify({"detail":"order not found"}), 404

    payment_id = next_payment_id()
    status = "PAID" if result == "success" else "FAILED"
    payment = {
        "payment_id": payment_id,
        "order_id": order_id,
        "status": status,
        "amount_rupees": ORDERS[order_id]["amount_rupees"],
        "created_at": time.time(),
        "payload": payload
    }
    PAYMENTS[payment_id] = payment
    ORDERS[order_id]["status"] = status
    print(f"Payment {payment_id} for {order_id}: {status}")
    return jsonify(payment), 200

@app.route("/order/<order_id>", methods=["GET"])
def get_order(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"detail":"not found"}), 404
    return jsonify(order)

@app.route("/payments", methods=["GET"])
def list_payments():
    return jsonify(list(PAYMENTS.values()))

@app.route("/payment_success")
def payment_success_page():
    return render_template("payment_success.html")

@app.route("/payment_failed")
def payment_failed_page():
    return render_template("payment_failed.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
