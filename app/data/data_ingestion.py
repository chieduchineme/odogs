import pandas as pd
import weaviate
from weaviate import WeaviateClient
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.data import DataObject
from .preprocess import load_product_data, load_order_data
from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

WEAVIATE_URL = "https://svukoggor4kpoaycdu91ia.c0.europe-west3.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "D1fKozPYV0QjynVmadhi6QIOLJqTZn7aFOOd"
COHERE_API_KEY = "Gtj6rQ9Z3B1lwkwi8nD17u5V96hK1E8koirk2bDh"


def create_schemas(client: WeaviateClient):
    if "Product" not in client.collections.list_all():
        client.collections.create(
            name="Product",
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
                Property(name="main_category", data_type=DataType.TEXT),
                Property(name="average_rating", data_type=DataType.NUMBER),
                Property(name="rating_number", data_type=DataType.INT),
                Property(name="features", data_type=DataType.TEXT_ARRAY),
                Property(name="price", data_type=DataType.NUMBER),
                Property(name="store", data_type=DataType.TEXT),
                Property(name="categories", data_type=DataType.TEXT_ARRAY),
                Property(name="details", data_type=DataType.TEXT),
                Property(name="parent_asin", data_type=DataType.TEXT),
            ],
            vectorizer_config=Configure.Vectorizer.none(),
        )

    if "Order" not in client.collections.list_all():
        client.collections.create(
            name="Order",
            properties=[
                Property(name="Order_Date", data_type=DataType.TEXT),
                Property(name="Time", data_type=DataType.TEXT),
                Property(name="Aging", data_type=DataType.NUMBER),
                Property(name="Customer_Id", data_type=DataType.INT),
                Property(name="Gender", data_type=DataType.TEXT),
                Property(name="Device_Type", data_type=DataType.TEXT),
                Property(name="Customer_Login_type", data_type=DataType.TEXT),
                Property(name="Product_Category", data_type=DataType.TEXT),
                Property(name="Product", data_type=DataType.TEXT),
                Property(name="Sales", data_type=DataType.NUMBER),
                Property(name="Quantity", data_type=DataType.NUMBER),
                Property(name="Discount", data_type=DataType.NUMBER),
                Property(name="Profit", data_type=DataType.NUMBER),
                Property(name="Shipping_Cost", data_type=DataType.NUMBER),
                Property(name="Order_Priority", data_type=DataType.TEXT),
                Property(name="Payment_method", data_type=DataType.TEXT),
            ],
            vectorizer_config=Configure.Vectorizer.none(),
        )

def upload_products(client: WeaviateClient):
    df = load_product_data()
    product_collection = client.collections.get("Product")
    objects = []

    for _, row in df.iterrows():
        obj = DataObject(
            properties={
                "title": row["title"],
                "description": " ".join(eval(row["description"])) if isinstance(row["description"], str) else "",
                "main_category": row["main_category"],
                "average_rating": row["average_rating"],
                "rating_number": int(row["rating_number"]),
                "features": eval(row["features"]) if isinstance(row["features"], str) else [],
                "price": row["price"],
                "store": row["store"],
                "categories": eval(row["categories"]) if isinstance(row["categories"], str) else [],
                "details": str(row["details"]),
                "parent_asin": row["parent_asin"]
            }
        )
        objects.append(obj)

    product_collection.data.insert_many(objects)

def upload_orders(client: WeaviateClient):
    from math import ceil

    df = load_order_data()
    order_collection = client.collections.get("Order")
    objects = []

    for _, row in df.iterrows():
        obj = DataObject(
            properties={
                "Order_Date": row["Order_Date"],
                "Time": row["Time"],
                "Aging": row["Aging"],
                "Customer_Id": int(row["Customer_Id"]),
                "Gender": row["Gender"],
                "Device_Type": row["Device_Type"],
                "Customer_Login_type": row["Customer_Login_type"],
                "Product_Category": row["Product_Category"],
                "Product": row["Product"],
                "Sales": row["Sales"],
                "Quantity": row["Quantity"],
                "Discount": row["Discount"],
                "Profit": row["Profit"],
                "Shipping_Cost": row["Shipping_Cost"],
                "Order_Priority": row["Order_Priority"],
                "Payment_method": row["Payment_method"]
            }
        )
        objects.append(obj)

    # Split into batches of 1000
    batch_size = 1000
    total_batches = ceil(len(objects) / batch_size)

    for i in range(total_batches):
        batch = objects[i * batch_size: (i + 1) * batch_size]
        order_collection.data.insert_many(batch)
        print(f"✅ Uploaded batch {i+1}/{total_batches} ({len(batch)} rows)")



def ingest_data():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
        # headers={"X-Cohere-Api-Key": COHERE_API_KEY},           # Replace with your Cohere API key
    )
    try:
        create_schemas(client)
        upload_products(client)
        upload_orders(client)
        print("✅ Data uploaded to Weaviate successfully.")
    finally:
        client.close()

ingest_data()