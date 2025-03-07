
# E-Commerce Website

## Overview
This is an E-Commerce web application that allows users to browse products, add them to the cart, and make purchases. It includes features like product listing, shopping cart, wishlist, and user authentication.

## Features
- **Product Listing**: Displays products fetched from a MySQL database.
- **Product Details**: Shows an individual product with an image, description, and price.
- **Shopping Cart**: Users can add/remove items and update quantities.
- **Wishlist**: Users can save products for future purchases.
- **Dynamic Home Page**: Random featured products are displayed and refreshed every 2 seconds.
- **Database-Driven Content**: Products, images, and details are dynamically fetched from MySQL.

## Technologies Used
- **Frontend**: HTML, CSS (Bootstrap), JavaScript (AJAX, jQuery)
- **Backend**: Python (Flask)
- **Database**: MySQL

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- MySQL Server
- Flask and necessary dependencies

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ecommerce-project.git
   cd ecommerce-project
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure database:
   - Create a MySQL database
   - Import the provided `database.sql` file
   - Update database credentials in `config.py`
4. Run the Flask app:
   ```bash
   flask run
   ```  
   or
   ```bash
   Python -m Backend.app
   ```
   Then 
   ```bash
   Python Backend/app.py
   ```
5. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## API Routes
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home Page |
| `/electronics` | GET | Electronics category page |
| `/product/<int:product_id>` | GET | Product details page |
| `/add_to_cart` | POST | Add product to cart |
| `/add_to_wishlist` | POST | Add product to wishlist |
| `/cart` | GET | View shopping cart |

## Issues & Debugging
- If images are not loading, ensure they are stored correctly in the `/static/images/` folder and paths are correct.
- If database queries fail, verify database connection settings and schema.
- Use `flask run --reload` to enable auto-reloading for debugging.

## License
This project is licensed under the MIT License.



