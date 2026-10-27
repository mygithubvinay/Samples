import os
from flask import Flask, render_template_string, session, redirect, url_for, request

app = Flask(__name__)
# Set SECRET_KEY as an environment variable in production
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

# Sample products (in-memory). Replace with a database later.
PRODUCTS = {
    1: {"name": "Wireless Mouse", "price": 799.00, "emoji": "🖱️"},
    2: {"name": "Mechanical Keyboard", "price": 3499.00, "emoji": "⌨️"},
    3: {"name": "USB-C Hub", "price": 1599.00, "emoji": "🔌"},
    4: {"name": "Headphones", "price": 2999.00, "emoji": "🎧"},
    5: {"name": "Laptop Stand", "price": 1299.00, "emoji": "💻"},
    6: {"name": "Webcam", "price": 2199.00, "emoji": "📷"},
}

BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Simple Shop</title>
  <style>
    * { box-sizing: border-box; }
    body { margin:0; font-family: system-ui, sans-serif; background:#f4f6fb; color:#1f2937; }
    nav { background:#4f46e5; color:#fff; padding:14px 20px; display:flex; justify-content:space-between; align-items:center; }
    nav a { color:#fff; text-decoration:none; font-weight:600; }
    main { max-width:900px; margin:20px auto; padding:0 16px; }
    .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:16px; }
    .card { background:#fff; border-radius:12px; padding:18px; box-shadow:0 2px 8px rgba(0,0,0,.08); text-align:center; }
    .emoji { font-size:3rem; }
    .price { color:#4f46e5; font-weight:700; margin:8px 0; }
    button, .btn { background:#4f46e5; color:#fff; border:0; border-radius:8px; padding:10px 16px;
                   cursor:pointer; text-decoration:none; display:inline-block; font-size:1rem; }
    .btn.danger { background:#ef4444; padding:6px 12px; font-size:.9rem; }
    table { width:100%; border-collapse:collapse; background:#fff; border-radius:12px; overflow:hidden; }
    th, td { padding:12px; text-align:left; border-bottom:1px solid #e5e7eb; }
    .total { text-align:right; font-size:1.3rem; font-weight:700; margin:16px 0; }
    .msg { background:#dcfce7; padding:14px; border-radius:8px; margin-bottom:16px; }
  </style>
</head>
<body>
  <nav>
    <a href="{{ url_for('index') }}">🛒 Simple Shop</a>
    <a href="{{ url_for('cart') }}">Cart ({{ cart_count }})</a>
  </nav>
  <main>{% block content %}{% endblock %}</main>
</body>
</html>
"""

INDEX = BASE.replace("{% block content %}{% endblock %}", """
<h2>Products</h2>
<div class="grid">
  {% for id, p in products.items() %}
  <div class="card">
    <div class="emoji">{{ p.emoji }}</div>
    <h3>{{ p.name }}</h3>
    <div class="price">₹{{ "%.2f"|format(p.price) }}</div>
    <form method="post" action="{{ url_for('add', pid=id) }}">
      <button type="submit">Add to cart</button>
    </form>
  </div>
  {% endfor %}
</div>
""")

CART = BASE.replace("{% block content %}{% endblock %}", """
<h2>Your Cart</h2>
{% if message %}<div class="msg">{{ message }}</div>{% endif %}
{% if items %}
<table>
  <tr><th>Item</th><th>Price</th><th>Qty</th><th>Subtotal</th><th></th></tr>
  {% for i in items %}
  <tr>
    <td>{{ i.name }}</td>
    <td>₹{{ "%.2f"|format(i.price) }}</td>
    <td>{{ i.qty }}</td>
    <td>₹{{ "%.2f"|format(i.subtotal) }}</td>
    <td>
      <form method="post" action="{{ url_for('remove', pid=i.id) }}">
        <button class="btn danger" type="submit">Remove</button>
      </form>
    </td>
  </tr>
  {% endfor %}
</table>
<div class="total">Total: ₹{{ "%.2f"|format(total) }}</div>
<form method="post" action="{{ url_for('checkout') }}"><button type="submit">Checkout</button></form>
{% else %}
<p>Your cart is empty. <a href="{{ url_for('index') }}">Continue shopping</a></p>
{% endif %}
""")


def cart_data():
    cart = session.get("cart", {})
    items, total = [], 0.0
    for pid, qty in cart.items():
        p = PRODUCTS.get(int(pid))
        if not p:
            continue
        subtotal = p["price"] * qty
        total += subtotal
        items.append({"id": int(pid), "name": p["name"], "price": p["price"],
                      "qty": qty, "subtotal": subtotal})
    return items, total


@app.context_processor
def inject_count():
    return {"cart_count": sum(session.get("cart", {}).values())}


@app.route("/")
def index():
    return render_template_string(INDEX, products=PRODUCTS)


@app.route("/add/<int:pid>", methods=["POST"])
def add(pid):
    if pid in PRODUCTS:
        cart = session.get("cart", {})
        cart[str(pid)] = cart.get(str(pid), 0) + 1
        session["cart"] = cart
    return redirect(request.referrer or url_for("index"))


@app.route("/cart")
def cart():
    items, total = cart_data()
    return render_template_string(CART, items=items, total=total, message=request.args.get("message"))


@app.route("/remove/<int:pid>", methods=["POST"])
def remove(pid):
    cart = session.get("cart", {})
    cart.pop(str(pid), None)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["POST"])
def checkout():
    session["cart"] = {}
    return redirect(url_for("cart", message="Thank you! Your order has been placed (demo)."))


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
