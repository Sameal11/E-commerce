import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, redirect, session, flash, url_for
from db_connect import get_db_connection
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__, template_folder="../templates",
            static_folder="../static")

app.secret_key = "your_secret_key"  # Change this to a secure key

bcrypt = Bcrypt(app)

# Flask-Session Config
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


products = {
    "1": {"name": "Elegant Dress", "price": 79.99, "image": "images/dress.jpg"},
    "2": {"name": "Casual Shirt", "price": 39.99, "image": "images/shirt.jpg"},
    "3": {"name": "Stylish Sneakers", "price": 89.99, "image": "images/sneakers.jpg"},
}

#cart pages
@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    subtotal = sum(float(item["price"]) * item["quantity"] for item in cart_items)  # Ensure price is float
    return render_template("cart.html", cart_items=cart_items, subtotal=subtotal)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    name = request.form["name"]
    price = float(request.form["price"])
    image = request.form["image"]

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    # Check if the product is already in the cart
    for item in cart:
        if item["name"] == name:
            item["quantity"] += 1  # Increase quantity
            session.modified = True
            return redirect(url_for("cart"))

    # If not found, add a new entry
    cart.append({"name": name, "price": price, "image": image, "quantity": 1})
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/update_cart/<item_name>", methods=["POST"])
def update_cart(item_name):
    new_quantity = int(request.form["quantity"])

    if "cart" in session:
        for item in session["cart"]:
            if item["name"] == item_name:
                item["quantity"] = new_quantity  # Update quantity
                break
        session.modified = True

    return redirect(url_for("cart"))
@app.route('/move_to_cart/<int:product_id>')
def move_to_cart(product_id):
    print(f"Moving item with index {product_id} to cart.")
    if "wishlist" in session:
        wishlist = session["wishlist"]
        if 0 <= product_id < len(wishlist):
            item = wishlist.pop(product_id)  # Remove the item from the wishlist
            print(f"Item moved: {item}")
            # Add the item to the cart
            if "cart" not in session:
                session["cart"] = []
            session["cart"].append({"name": item["name"], "price": item["price"], "image": item["image"], "quantity": 1})
            session.modified = True
    return redirect(url_for("wishlist"))

@app.route("/remove_from_cart/<item_name>")
def remove_from_cart(item_name):
    if "cart" in session:
        session["cart"] = [item for item in session["cart"] if item["name"] != item_name]
        session.modified = True

    return redirect(url_for("cart"))

@app.route("/checkout")
def checkout():
    cart_items = session.get("cart", [])
    subtotal = sum(item["price"] * item["quantity"] for item in cart_items)
    return render_template("checkout.html", cart_items=cart_items, subtotal=subtotal)



# wishlist page
@app.route('/wishlist')
def wishlist():
    wishlist_items = session.get("wishlist", [])  # Retrieve wishlist items from session
    return render_template('wishlist.html', wishlist=wishlist_items)

@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    product = {
        "name": request.form.get("name"),
        "price": request.form.get("price"),
        "image": request.form.get("image")
    }

    wishlist = session.get("wishlist", [])
    wishlist.append(product)
    session["wishlist"] = wishlist  # Save to session
    return redirect(url_for('wishlist'))


@app.route('/remove_from_wishlist/<int:product_id>')
def remove_from_wishlist(product_id):
    wishlist = session.get("wishlist", [])
    if 0 <= product_id < len(wishlist):
        wishlist.pop(product_id)
    session["wishlist"] = wishlist
    return redirect(url_for('wishlist'))



# fashion page
@app.route('/fashion')
def fashion():
    return render_template('fashion.html', products=products)  # Pass products

# electronic page
@app.route('/electronics')
def electronics(): 
    return render_template('electronics.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # You can save this data to a database or send an email notification
        print(f"Received message from {name} ({email}): {message}")
        
        return redirect(url_for('contact'))  # Redirect after submission

    return render_template('contact.html')
#gor skip or guest 
@app.route('/')
def home():
    username = session.get("user_name", "Guest")  # Default to 'Guest' if not logged in
    return render_template("home.html", username=username)

@app.context_processor
def inject_user():
    return dict(username=session.get("user_name"))

@app.context_processor
def inject_globals():
    return dict(request=request)

# Combined Login & Register Page
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')  # Determine if it's login or register

        if action == "login":
            email = request.form.get('email')
            password = request.form.get('password')

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            conn.close()

            if user and bcrypt.check_password_hash(user['password'], password):
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid email or password!", "danger")

        elif action == "register":
            name = request.form.get('name')
            email = request.form.get('email')
            mobile = request.form.get('mobile_number')  # Adjust if your column name is different (e.g., mobile_number)
            password_plain = request.form.get('password')
            password_hashed = bcrypt.generate_password_hash(password_plain).decode('utf-8')

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                # Ensure the column names match your MySQL table
                cursor.execute(
                    "INSERT INTO users (name, mobile_number, email, password) VALUES (%s, %s, %s, %s)",
                    (name, mobile, email, password_hashed)
                )
                conn.commit()
                flash("Registration successful! You can now log in.", "success")
            except Exception as e:
                flash("Registration failed: " + str(e), "danger")
            finally:
                conn.close()

            return redirect(url_for('auth'))

    return render_template('auth.html')


# ✅ Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth'))


if __name__ == '__main__':
    app.run(debug=True)
