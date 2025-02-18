from flask import Flask, render_template, request, redirect, session, flash, url_for
from db_connect import get_db_connection
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key

bcrypt = Bcrypt(app)

# Flask-Session Config
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route('/')
def home():
    if "user_id" in session:
        return render_template("home.html", username=session["user_name"])
    return redirect('/auth')


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
                flash("Registration successful! You can now login.", "success")
            except Exception as e:
                # Log error (you can print e or log it)
                flash("Registration failed: " + str(e), "danger")
            finally:
                conn.close()

            return redirect(url_for('auth'))

    return render_template('auth.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth'))

if __name__ == '__main__':
    app.run(debug=True)
