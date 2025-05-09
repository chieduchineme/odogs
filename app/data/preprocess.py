import pandas as pd
import numpy as np

# Define the paths to your datasets
PRODUCT_DATA_PATH = "app/data/Product_Information_Dataset.csv"
ORDER_DATA_PATH = "app/data/Order_Data_Dataset.csv"

def load_data(csv_file):
    """Load and clean a CSV file."""
    df = pd.read_csv(csv_file)
    df.replace([np.inf, -np.inf], None, inplace=True)

    # Fill missing values based on data type
    for col in df.columns:
        df[col] = df[col].fillna("" if df[col].dtype == "object" else 0)
    
    return df

def load_product_data():
    return load_data(PRODUCT_DATA_PATH)


def load_order_data():
    return load_data(ORDER_DATA_PATH)

