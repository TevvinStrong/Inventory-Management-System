# Import installed packages
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# Initialize flask app
app = Flask(__name__, template_folder="templates")
# Prevent CORS errors
CORS(app)

# Establish MongoDB connection
mongo_uri = "mongodb+srv://TevvinStrong:SuccessMoney1.@cluster0.tqcutev.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["Inventroy"]
collection = db["productMetrics"]

# Render html template view responsible for the home page.
@app.route('/', methods=['GET', 'POST'])
def home():
    found_product = None
    # Store mongodb collection
    products_cursor = collection.find({})

    if request.method == 'POST':
        search_term = request.form.get('search_term')

        # Search db collection for the product by product_name
        for product in products_cursor:
            product_name = product.get('product_name')
            if product_name and product_name.lower() == search_term.lower():
                found_product = product
                break

    return render_template('home.html', found_product=found_product, product_metrics=products_cursor)

# Add a new product
@app.route('/product', methods=['POST'])
def add_product():
    # Parse JSON data from request body
    data = request.get_json()
    
    # Check if the required fields are present
    required_fields = ['product_id', 'product_name', 'product_category', 'price', 'available_quantity']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return f"Missing fields: {', '.join(missing_fields)}", 400
    
    # Extract the values
    product_id = data['product_id']
    product_name = data['product_name']
    product_category = data['product_category']
    price = data['price']
    available_quantity = data['available_quantity']
    
    # Convert price and available_quantity to appropriate types
    try:
        price = float(price)
        available_quantity = int(available_quantity)
    except ValueError:
        return "Invalid price or available quantity format", 400
    
    # Insert the new product into MongoDB
    product_data = {
        "product_id": product_id,
        "product_name": product_name,
        "product_category": product_category,
        "price": price,
        "available_quantity": available_quantity
    }

    # Insert into mongodb collection
    collection.insert_one(product_data)
    
    return "Product added successfully!"

# Render html template view responsible for creating a product.
@app.route('/product', methods=['GET'])
def add_product_form():
    return render_template('add_product.html', added_product=True)

# Render html template view responsible for updating a product.
@app.route('/products/<string:product_id>/update', methods=['GET'])
def update_product_form(product_id):
    # Retrieve the product from MongoDB using the provided product ID
    product = collection.find_one({"product_id": product_id})
    if product is None:
        return f"{product_id} does not exists", 404
    
    return render_template('update_product.html', product=product)

# Update an existing product  
@app.route('/products/<string:product_id>/update', methods=['PUT'])
def update_product(product_id):
    # Capture form data
    data = request.form
    
    # Update the product in MongoDB
    updated_product = {
        "product_name": data['product_name'],
        "product_category": data['product_category'],
        "price": float(data['price']),
        "available_quantity": int(data['available_quantity'])
    }
    # Search for product_id that matches the given product_id
    collection.update_one({"product_id": product_id}, {"$set": updated_product})
    
    return "Product updated successfully!"

# Render html template view responsible for product deletion.
@app.route('/products/<string:product_id>/delete', methods=['GET'])
def delete_product_form(product_id):
    # Retrieve the product from MongoDB based on product_id
    product = collection.find_one({"product_id": product_id})
    
    if product is None:
        return f"{product_id} does not exists", 404
    
    return render_template('delete_product.html', product=product)

# Delete a product
@app.route('/products/<string:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    # Delete the product from MongoDB
    result = collection.delete_one({"product_id": product_id})

    if result.deleted_count == 1:
        return "Product deleted successfully!", 200
    else:
        return f"{product_id} does not exists", 404

# Render html template to view aggrageted product metrics. 
@app.route('/products/analytics', methods=['GET'])
def fetch_product_analytics_view():
    # Aggregate data using MongoDB aggregation pipeline
    pipeline = [
        {"$group": {"_id": "$product_category", "total_count": {"$sum": 1}, "average_price": {"$avg": "$price"}}},
        {"$project": {"category": "$_id", "total_count": 1, "average_price": 1, "_id": 0}},
        {"$sort": {"total_count": -1}}
    ]
    analytics_data = list(collection.aggregate(pipeline))
    # return html template responsible for the view
    return render_template('product_analytics.html', analytics_data=analytics_data)

# Get aggrageted data that consist of the most popular product category, the total count of products, and the average price within that category.
@app.route('/products/analytics', methods=['GET'])
def fetch_product_analytics():
    # Aggregate data using MongoDB aggregation pipeline
    pipeline = [
        {
            '$group': {
                '_id': '$product_category',
                'count': { '$sum': 1 },
                'avg_price': { '$avg': '$price' }
            }
        },
        {
            '$sort': { 'count': -1 }
        },
        {
            '$limit': 1
        }
    ]
    # Store the results in a variable
    result = collection.aggregate(pipeline)

    # Format the aggregated data
    analytics_data = []
    for entry in result:
        analytics_data.append({
            'category': entry['_id'],
            'total_count': entry['count'],
            'average_price': entry['avg_price']
        })
    # Convert to a JSON response object
    return jsonify(analytics_data)

# Run app at this IP address (http://127.0.0.1:5000/)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    