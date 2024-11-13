# EBS Integrator

## Project Overview

This project is a Django-based application designed to monitor and manage the prices of products on the market. The system allows users to add products, set prices for specific time intervals, and calculate average prices over different periods. The application also supports CRUD operations for product categories and products.

## Features

1. **Category Management**:
   - Add, edit, delete, and list categories.
   - Each category consists of a name.

2. **Product Management**:
   - Add, edit, delete, and list products.
   - Each product consists of a name, category, SKU, and description.

3. **Price Management**:
   - Set prices for products over specific date ranges.
   - Handle overlapping price intervals.
   - Change prices for an indefinite period or specific past intervals.
   - Track the history of price changes.

4. **Average Price Calculation**:
   - Calculate the average price for a product category over a specified date range.
   - Calculate average prices per week or month for a specific product.

## Endpoints

1. **Category Endpoints**:
   - `GET /api/v1/storage/categories/`: List all categories.
   - `POST /api/v1/storage/categories/`: Add a new category.
   - `GET /api/v1/storage/categories/{id}/`: Retrieve a specific category.
   - `PUT /api/v1/storage/categories/{id}/`: Update a specific category.
   - `DELETE /api/v1/storage/categories/{id}/`: Delete a specific category.

2. **Product Endpoints**:
   - `GET /api/v1/storage/products/`: List all products.
   - `POST /api/v1/storage/products/`: Add a new product.
   - `GET /api/v1/storage/products/{id}/`: Retrieve a specific product.
   - `PUT /api/v1/storage/products/{id}/`: Update a specific product.
   - `DELETE /api/v1/storage/products/{id}/`: Delete a specific product.

3. **Price Endpoints**:
   - `POST /api/v1/storage/products/{product_id}/price/`: Set a price for a product over a specified date range.
   - `PUT /api/v1/storage/categories/{category_id}/price/`: Change the price for all products in a specific category.
   - `GET /api/v1/storage/categories/{category_id}/price/average/`: Get the average price for a category over a specified date range.
   - `GET /api/v1/storage/products/{product_id}/price/average/`: Get the average price for a product over a specified date range, per week or month.

## Swagger Documentation

The project includes automatically generated Swagger documentation for the API endpoints. You can access the documentation at the following URLs:
- Swagger UI: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- Redoc: `http://127.0.0.1:8000/api/schema/redoc/`
- OpenAPI Schema: `http://127.0.0.1:8000/api/schema/`

## Error Handling

The project uses `drf-standardized-errors[openapi]` to handle error responses in a standardized format.

## Future Enhancements

1. **User Roles**:
   - Implement different user roles (e.g., admin, manager, viewer) with specific permissions.

2. **Logging**:
   - Add comprehensive logging to track user actions and system events.

3. **Session Login View**:
   - Implement session-based login views to enhance user authentication and security.

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:nickita14/ebs-integrator.git
   cd ebs-integrator
    ```
