# Import requirements
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__, template_folder="templates")
CORS(app)

# Establish MongoDB connection
mongo_uri = "mongodb+srv://TevvinStrong:SuccessMoney1.@cluster0.tqcutev.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["Inventroy"]
collection = db["productMetrics"]

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

@app.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()  # Parse JSON data from request body
    
    # Check if the required fields are present
    required_fields = ['product_id', 'product_name', 'product_category', 'price', 'available_quantity']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return f"Missing fields: {', '.join(missing_fields)}", 400
    
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
    
    collection.insert_one(product_data)
    
    return "Product added successfully!"

@app.route('/product', methods=['GET'])
def add_product_form():
    return render_template('add_product.html', added_product=True)

# Render the update product form
@app.route('/products/<string:product_id>/update', methods=['GET'])
def update_product_form(product_id):
    # Retrieve the product from MongoDB using the provided product ID
    product = collection.find_one({"product_id": product_id})
    if product is None:
        return f"Product with ID {product_id} not found", 404
    
    return render_template('update_product.html', product=product)

# Handle form submission for updating the product
@app.route('/products/<string:product_id>/update', methods=['PUT'])
def update_product(product_id):
    data = request.form  # Form data
    
    # Update the product in MongoDB
    updated_product = {
        "product_name": data['product_name'],
        "product_category": data['product_category'],
        "price": float(data['price']),
        "available_quantity": int(data['available_quantity'])
    }
    
    collection.update_one({"product_id": product_id}, {"$set": updated_product})
    
    return "Product updated successfully!"

@app.route('/products/<string:product_id>/delete', methods=['GET'])
def delete_product_form(product_id):
    # Retrieve the product from MongoDB based on product_id
    product = collection.find_one({"product_id": product_id})
    
    if product is None:
        return f"Product with ID {product_id} not found", 404
    
    return render_template('delete_product.html', product=product)


@app.route('/products/<string:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    # Delete the product from MongoDB
    result = collection.delete_one({"product_id": product_id})

    if result.deleted_count == 1:
        return "Product deleted successfully!", 200
    else:
        return f"Product with ID {product_id} not found", 404

@app.route('/products/analytics', methods=['GET'])
def fetch_product_analytics_view():
    # Aggregate data using MongoDB aggregation pipeline
    pipeline = [
        {"$group": {"_id": "$product_category", "total_count": {"$sum": 1}, "average_price": {"$avg": "$price"}}},
        {"$project": {"category": "$_id", "total_count": 1, "average_price": 1, "_id": 0}},
        {"$sort": {"total_count": -1}}
    ]
    analytics_data = list(collection.aggregate(pipeline))

    return render_template('product_analytics.html', analytics_data=analytics_data)

@app.route('/products/analytics', methods=['GET'])
def fetch_product_analytics():
    # Retrieve product data
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

    result = collection.aggregate(pipeline)

    # Format the aggregated data
    analytics_data = []
    for entry in result:
        analytics_data.append({
            'category': entry['_id'],
            'total_count': entry['count'],
            'average_price': entry['avg_price']
        })

    return jsonify(analytics_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# The application works, all is needed to be done now is the below
# Write a brief document explaining your application structure, how to run it, and how it addresses the objectives of the assignment.
# Quality of your code: We'll look for clean, well-structured, and commented code that follows best practices.(look through make sure code has comments)
# Documentation: Your write-up should be clear and easy to understand, providing sufficient detail for someone unfamiliar with your project to get it up and running.(READ.me)
# Please submit your code in a private repository (GitHub, GitLab, Bitbucket, etc.) and share the access with us. Include all the source code, Dockerfiles, and the documentation in this repository. 
