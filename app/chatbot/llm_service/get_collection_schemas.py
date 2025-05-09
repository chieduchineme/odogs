"""
This module handles interactions between natural language inputs and the vector database (Weaviate)
as well as the language model (Cohere). It supports routing logic, schema matching, and RAG-based responses.
"""

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Property
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration: Cohere and Weaviate credentials (with fallback hardcoded values)
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://svukoggor4kpoaycdu91ia.c0.europe-west3.gcp.weaviate.cloud")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "D1fKozPYV0QjynVmadhi6QIOLJqTZn7aFOOd")


def get_collection_schemas():
    """
    Retrieve schema information (field names) for all collections in the Weaviate instance.

    Returns:
        dict: Dictionary with collection names as keys and lists of property names as values.
    """
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    )

    collections = client.collections.list_all()
    class_keywords = {}

    for name in collections:
        collection = client.collections.get(name)
        config = collection.config.get()
        properties = [prop.name for prop in config.properties]
        class_keywords[name.lower()] = properties

    client.close()
    return class_keywords

