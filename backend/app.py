
import os
import sys
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, render_template, request, redirect, session, flash, url_for,jsonify
from backend.db_connect import get_db_connection
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.secret_key = "your_secret_key"  # Change this to a secure key

bcrypt = Bcrypt(app)

# Flask-Session Config
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# 🏠 Home Page
@app.route('/')
def home():
    username = session.get("user_name", "Guest")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch 4 random products from the database
    cursor.execute("SELECT * FROM products ORDER BY RAND() LIMIT 4")
    products = cursor.fetchall()


    return render_template("home.html", username=username,products=products)
#top product 
@app.route("/top-product")
def top_product():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch one random product for the Top Product Box
    cursor.execute("SELECT * FROM products ORDER BY RAND() LIMIT 1")
    product = cursor.fetchone()

    conn.close()
    return jsonify(product)
@app.context_processor
def inject_user():
    return dict(username=session.get("user_name"))

@app.context_processor
def inject_globals():
    return dict(request=request)

#ADMIN 
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        action = request.form.get("action")

        # 🔍 Search for products
        if action == "search":
            search_query = request.form.get("search_query")
            cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{search_query}%",))
            products = cursor.fetchall()
            conn.close()
            return render_template("adminpanel.html", products=products)

        # ➕ Add a new product
        elif action == "add":
            name = request.form.get("name")
            description = request.form.get("description")
            price = request.form.get("price")
            stock = request.form.get("stock")
            category_id = request.form.get("category_id")
            image_url = request.form.get("image_url")

            try:
                cursor.execute(
                    "INSERT INTO products (name, description, price, stock, category_id, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, description, price, stock, category_id, image_url)
                )
                conn.commit()
                print("✅ Product added successfully!")
            except mysql.connector.Error as err:
                print(f"❌ Error inserting product: {err}")
            finally:
                conn.commit()

        # ❌ Remove a product
        elif action == "remove":
            product_id = request.form.get("product_id")
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()

        return redirect(url_for("admin"))

    
    # Fetch all products to display in admin panel
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    # Fetch categories for the dropdown
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()


    conn.close()
    return render_template("adminpanel.html", products=products, categories=categories)



# 🔑 Authentication Routes
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == "login":
            email = request.form.get('email')
            password = request.form.get('password')

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, password, role FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            conn.close()

            if user and bcrypt.check_password_hash(user['password'], password):
                session.permanent = True
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["role"] = user["role"]

                flash("Login successful!", "success")

                if user["role"] == "admin":
                    return redirect(url_for('admin'))  # Redirect to Admin Dashboard
                else:
                    return redirect(url_for('home'))  # Redirect to Home Page

            else:
                flash("Invalid email or password!", "danger")

        elif action == "register":
            name = request.form.get('name')
            email = request.form.get('email')
            mobile = request.form.get('mobile_number')
            password_plain = request.form.get('password')
            role = "customer"  # Default role for new users
            password_hashed = bcrypt.generate_password_hash(password_plain).decode('utf-8')

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (name, mobile_number, email, password, role) VALUES (%s, %s, %s, %s, %s)",
                    (name, mobile, email, password_hashed, role)
                )
                conn.commit()
                flash("Registration successful! You can now log in.", "success")
            except Exception as e:
                flash("Registration failed: " + str(e), "danger")
            finally:
                conn.close()

            return redirect(url_for('auth'))

    return render_template('auth.html')

#profile page 
@app.route("/profile")
def profile():
    if "user_name" not in session:
        return redirect(url_for("auth"))  # Redirect to login if not logged in

  
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    # Fetch user details
    cur.execute("SELECT name, email, mobile_number FROM users WHERE id = %s", (session["user_id"],))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return"user not found",404

    # Fetch wishlist
    cur.execute("SELECT name FROM wishlist WHERE user_id = %s", (session["user_id"],))
    wishlist = [row["name"] for row in cur.fetchall()]

    # Fetch cart items
    cur.execute("SELECT name FROM cart WHERE user_id = %s", (session["user_id"],))
    cart = [row["name"] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return render_template("profile.html", username=user["name"], email=user["email"], mobile=user["mobile_number"], wishlist=wishlist, cart=cart)

# 🛒 Cart Routes
@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    subtotal = sum(float(item["price"]) * item["quantity"] for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, subtotal=subtotal)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    name = request.form["name"]
    price = float(request.form["price"])
    image = request.form["image"]

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    for item in cart:
        if item["name"] == name:
            item["quantity"] += 1
            session.modified = True
            return redirect(url_for("cart"))

    cart.append({"name": name, "price": price, "image": image, "quantity": 1})
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/update_cart/<item_name>", methods=["POST"])
def update_cart(item_name):
    new_quantity = int(request.form["quantity"])

    if "cart" in session:
        for item in session["cart"]:
            if item["name"] == item_name:
                item["quantity"] = new_quantity
                break
        session.modified = True

    return redirect(url_for("cart"))

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

# ❤️ Wishlist Routes
@app.route('/wishlist')
def wishlist():
    wishlist_items = session.get("wishlist", [])
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
    session["wishlist"] = wishlist
    return redirect(url_for('wishlist'))

@app.route('/remove_from_wishlist/<int:product_id>')
def remove_from_wishlist(product_id):
    wishlist = session.get("wishlist", [])
    if 0 <= product_id < len(wishlist):
        wishlist.pop(product_id)
    session["wishlist"] = wishlist
    return redirect(url_for('wishlist'))

@app.route('/move_to_cart/<int:product_id>')
def move_to_cart(product_id):
    if "wishlist" in session:
        wishlist = session["wishlist"]
        if 0 <= product_id < len(wishlist):
            item = wishlist.pop(product_id)
            if "cart" not in session:
                session["cart"] = []
            session["cart"].append({"name": item["name"], "price": item["price"], "image": item["image"], "quantity": 1})
            session.modified = True
    return redirect(url_for("wishlist"))
#product page
@app.route('/product/<int:product_id>')
def product_page(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch product details based on product_id
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    conn.close()

    if not product:
        return "Product not found", 404  # Show error if product doesn't exist
    
    return render_template("product.html", product=product)


# 🔥 categories Pages
#electtronic
@app.route('/electronics')
def electronics():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Electronics Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Electronics'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Electronics category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("electronics.html", products=products)
#fashion page 
@app.route('/fashion')
def fashion():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Electronics Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Fashion'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Electronics category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("fashion.html", products=products)

# Home & Kitchen Route
@app.route('/home-kitchen')
def home_kitchen():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Home & Kitchen Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Home & Kitchen'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Home & Kitchen category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("home_kitchen.html", products=products)

# Sports & Fitness Route
@app.route('/sports-fitness')
def sports_fitness():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Sports & Fitness Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Sports & Fitness'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Sports & Fitness category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("sports_fitness.html", products=products)
# Books Route
@app.route('/books')
def books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Books Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Books'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Books category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("books.html", products=products)

# Toys & Games Route
@app.route('/toys_games')
def toys_games():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Toys & Games Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Toys & Games'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Toys & Games category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("toys_games.html", products=products)

# Beauty & Health Route
@app.route('/beauty_health')
def beauty_health():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Beauty & Health Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Beauty & Health'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Beauty & Health category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("beauty_health.html", products=products)

# Automobiles Route
@app.route('/automobiles')
def automobiles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Automobiles Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Automobiles'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Automobiles category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("automobiles.html", products=products)

# Groceries Route
@app.route('/groceries')
def groceries():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Groceries Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Groceries'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Groceries category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("groceries.html", products=products)

# Furniture Route
@app.route('/furniture')
def furniture():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Furniture Category ID
    cursor.execute("SELECT id FROM categories WHERE name = 'Furniture'")
    category = cursor.fetchone()

    products = []
    if category:
        category_id = category["id"]
        # Fetch products in Furniture category
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        products = cursor.fetchall()

    conn.close()
    return render_template("furniture.html", products=products)


# 📩 Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        print(f"Received message from {name} ({email}): {message}")
        flash("Your message has been sent!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')
# place order 
@app.route('/place_order')
def place_order():
    cart_items = session.get('cart', [])  # Retrieve cart from session

    # Convert price to float after stripping '$', and quantity to int
    subtotal = sum(
    (float(item['price'].replace('$', '')) if isinstance(item['price'], str) else item['price']) * int(item['quantity']) 
    for item in cart_items
)
    total = subtotal + 5.00  # Add shipping cost
    return render_template("place_order.html", cart_items=cart_items, subtotal=subtotal, total=total)
# payment
@app.route('/payment')
def payment():
    total = request.args.get('total', default=0, type=float)
    return render_template('payment.html', total=total)

# 🚪 Logout Route (Fix)
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth'))

# ✅ Run the App
if __name__ == '__main__':
    app.run(debug=True)
