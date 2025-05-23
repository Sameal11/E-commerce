
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

    cur.close()
    conn.close()

    return render_template("profile.html", username=user["name"], email=user["email"], mobile=user["mobile_number"], wishlist=wishlist, cart=cart)

# 🛒 Cart Routes
@app.route("/cart")
def cart():
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Fetch cart items along with quantity and product details
    cur.execute("""
        SELECT c.product_id, c.quantity, p.name, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))
    cart_items = cur.fetchall()

    cur.close()
    conn.close()

    # Calculate subtotal
    subtotal = sum(item["price"] * item["quantity"] for item in cart_items)

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

# ❤️ Wishlist Routes
@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Fetch wishlist items with product details
    cur.execute("""
        SELECT w.product_id, p.name, p.price
        FROM wishlist w
        JOIN products p ON w.product_id = p.id
        WHERE w.user_id = %s
    """, (user_id,))
    wishlist_items = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('wishlist.html',wishlist=wishlist_items)


@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    product_id = request.form.get("product_id")

    # print("Form Data:", request.form)
    # print("Product ID:", product_id)
    try:
        conn = get_db_connection()
        cur = conn.cursor()


         # Fetch product details based on product_id
        cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cur.fetchone()

        # Check if product already in wishlist
        cur.execute("SELECT id FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        existing = cur.fetchone()

        if not existing:
            cur.execute("INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
            conn.commit()
            flash("Product added to wishlist successfully!", "success")
        else:
            flash("productis already in  wishlist")
            
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('wishlist'))

@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
def remove_from_wishlist(product_id):
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']
    product_id = request.form.get('product_id')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('wishlist'))


@app.route('/move_to_cart/<int:product_id>')
def move_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if product exists in wishlist
    cur.execute("SELECT product_id FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    item = cur.fetchone()

    if item:
        # Insert into cart (assuming you have a cart table)
        cur.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, product_id, 1))

        # Remove from wishlist
        cur.execute("DELETE FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))

        conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('wishlist'))
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
    
    return render_template("product.html", product=product , product_id=product_id)


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

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        email = request.form['email']
        total = request.form['total']

        cur.execute("""
            INSERT INTO orders (user_id, name, address, city, state, zip, email, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, address, city, state, zip_code, email, total))
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('payment'))

    cur.execute("""
        SELECT p.name, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))
    cart_items = cur.fetchall()

    subtotal = sum(float(item['price']) * float(item['quantity']) for item in cart_items)

    shipping_cost = float('5.00')
    total_cost = subtotal + shipping_cost

    cur.close()
    conn.close()

    return render_template('place_order.html', cart_items=cart_items, subtotal=subtotal, total=total_cost)
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    if request.method == 'POST':
        payment_method = request.form.get('payment-method')
        card_number = request.form.get('card-number')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        upi_id = request.form.get('upi-id')
        total = request.form.get('total')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO payments (user_id, method, card_number, expiry, cvv, upi_id, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (session['user_id'], payment_method, card_number, expiry, cvv, upi_id, total))
        conn.commit()

        cur.close()
        conn.close()

        return render_template('payment_success.html')

    total = request.args.get('total', 0.0)
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
