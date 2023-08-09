# Inventory-Management-System

### Application Structure:

The application consists of the following components:

### API Implementation (api.py):
- This file contains the Flask application setup and routing. It defines the various endpoints for CRUD operations and product analytics.

### Templates (templates/):
- This folder contains the HTML templates used for rendering the user interface for adding, updating, and deleting products, as well as for displaying product analytics.

### Static Files (static/):
- This folder contains static files such as CSS stylesheets and JavaScript files used for enhancing the user interface.

### Dockerfile (Dockerfile):
- This file defines the Docker image for the application. It specifies the base image, installs necessary dependencies, copies application files into the image, and sets the entry point to run the Flask application.

### Requirements File (requirements.txt):
- This file lists the required Python packages and their versions. It is used to install the required packages when building the Docker image.

### Prerequisites:
1. Docker: Ensure you have Docker installed on your machine. If not, you can download and install it from the official website.

# Step-by-Step Setup(How to Run):
### Clone the Repository:
Clone the repository containing the application code to your local machine:
```
git clone git@github.com:TevvinStrong/Inventory-Management-System.git
cd dev

(This could be different based on where you store the repo on your local machine)
```

### Build Docker Image:
Open a terminal window and navigate to the root directory of the cloned repository. Build the Docker image using the following command:
```
docker build -t flask-docker-app . 
```
### Run Docker Container:
Once the image is built, run the Docker container:
```
docker run -p 5000:5000 flask-docker-app
```
This command starts the application within a Docker container and maps port 5000 of the container to port 5000 on your machine.

# Using the Application:
- ### Viewing All Products:
    When you first access the home page at `http://localhost:5000/`, you will see a list of all the products fetched from the database. This list is displayed below the search bar. Each product's name is shown in an unordered list format.



- ### Adding a Product:
    Click the "Add Product" button on the home page. Fill in the product details and click "Add Product." You'll see a success message if the product is added successfully.



- ### Updating a Product:
    Get the id of the product you want to update for example: `http://127.0.0.1:5000/products/555/update`. Once the page renders update the data you want to update then select the `Update Product` button. You will then get a success message, from here naviagte back to the home page by selecting the `Go back to home` link to see that product using the updated data.



- ### Deleting a Product:
    Similar to updating a product get the id of the product you want to delete for example: `http://127.0.0.1:5000/products/555/delete`. Again similar to updating a product, once the page renders hit the `Delete Product` button. A alert will then fire to confirm with you which product is getting deleted, once you confim the product will be deleted. You can then return to the home page and see that specific product was indeed deleted.



- ### Product Analytics:
    Last but not least, to view the products analytics all is needed is to key in this URL to view the page:
    `http://127.0.0.1:5000/products/analytics`

    Do keep in mind that you will need some product data populated in your local database for the analytics page to pull in each product metrics.


# Conclusion
In conclusion, the "Inventory Management System with Product Analytics" application fulfills the assignment objectives by providing a functional inventory management system with CRUD operations, product analytics, full-text search, and a user-friendly interface. The application is built using Flask and MongoDB, and it can be run in a Docker container for easy deployment.