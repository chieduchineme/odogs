from fastapi import APIRouter
import pandas as pd
import numpy as np
from app.data.preprocess import load_product_data

product_router = APIRouter()
df_products = load_product_data()

@product_router.get("/all")
def get_all_products():
    df = load_product_data()
    return df.to_dict(orient="records")

@product_router.get("/search/{title}")
def search_product_by_title(title: str):
    data = df_products[df_products["title"].str.contains(title, case=False, na=False)]
    if data.empty:
        return {"error": f"No products found for title '{title}'"}
    return data.to_dict(orient="records")

@product_router.get("/category/{category}")
def get_product_by_main_category(category: str):
    data = df_products[df_products["main_category"].str.contains(category, case=False, na=False)]
    if data.empty:
        return {"error": f"No products found in main category '{category}'"}
    return data.to_dict(orient="records")

@product_router.get("/rating/above/{threshold}")
def get_products_by_rating(threshold: float):
    data = df_products[df_products["average_rating"] >= threshold]
    return data.to_dict(orient="records")

@product_router.get("/store/{store_name}")
def get_products_by_store(store_name: str):
    data = df_products[df_products["store"].str.contains(store_name, case=False, na=False)]
    if data.empty:
        return {"error": f"No products found from store '{store_name}'"}
    return data.to_dict(orient="records")
