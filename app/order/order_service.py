from fastapi import APIRouter
import pandas as pd
from app.data.preprocess import load_order_data

order_router = APIRouter()
df = load_order_data()

@order_router.get("/all")
def get_all_orders():
    return df.to_dict(orient="records")


# Endpoint to filter data by Customer ID
@order_router.get("/data/customer/{customer_id}")
def get_customer_data(customer_id: int):
    """Retrieve all records for a specific Customer ID."""
    filtered_data = df[df["Customer_Id"] == customer_id]
    if filtered_data.empty:
        return {"error": f"No data found for Customer ID {customer_id}"}
    return filtered_data.to_dict(orient="records")

# Endpoint to filter data by Product Category
@order_router.get("/data/product-category/{category}")
def get_product_category_data(category: str):
    """Retrieve all records for a specific Product Category."""
    filtered_data = df[df["Product_Category"].str.contains(category, case=False, na=False)]
    if filtered_data.empty:
        return {"error": f"No data found for Product Category '{category}'"}
    return filtered_data.to_dict(orient="records")

# Endpoint to get orders with specific priorities
@order_router.get("/data/order-priority/{priority}")
def get_orders_by_priority(priority: str):
    """Retrieve all orders with the given priority."""
    filtered_data = df[df["Order_Priority"].str.contains(priority, case=False, na=False)]
    if filtered_data.empty:
        return {"error": f"No data found for Order Priority '{priority}'"}
    return filtered_data.to_dict(orient="records")

# Endpoint to calculate total sales by Product Category
@order_router.get("/data/total-sales-by-category")
def total_sales_by_category():
    """Calculate total sales by Product Category."""
    sales_summary = df.groupby("Product_Category")["Sales"].sum().reset_index()
    return sales_summary.to_dict(orient="records")

# Endpoint to get high-profit products
@order_router.get("/data/high-profit-products")
def high_profit_products(min_profit: float = 100.0):
    """Retrieve products with profit greater than the specified value."""
    filtered_data = df[df["Profit"] > min_profit]
    if filtered_data.empty:
        return {"error": f"No products found with profit greater than {min_profit}"}
    return filtered_data.to_dict(orient="records")

# Endpoint to get shipping cost summary
@order_router.get("/data/shipping-cost-summary")
def shipping_cost_summary():
    """Retrieve the average, minimum, and maximum shipping cost."""
    summary = {
        "average_shipping_cost": df["Shipping_Cost"].mean(),
        "min_shipping_cost": df["Shipping_Cost"].min(),
        "max_shipping_cost": df["Shipping_Cost"].max()
    }
    return summary

# Endpoint to calculate total profit by Gender
@order_router.get("/data/profit-by-gender")
def profit_by_gender():
    """Calculate total profit by customer gender."""
    profit_summary = df.groupby("Gender")["Profit"].sum().reset_index()
    return profit_summary.to_dict(orient="records")