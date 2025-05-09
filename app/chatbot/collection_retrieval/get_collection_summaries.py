import cohere
import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setup Cohere and Weaviate configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "Gtj6rQ9Z3B1lwkwi8nD17u5V96hK1E8koirk2bDh")
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://svukoggor4kpoaycdu91ia.c0.europe-west3.gcp.weaviate.cloud")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "D1fKozPYV0QjynVmadhi6QIOLJqTZn7aFOOd")

# Initialize Cohere and Weaviate clients
cohere_client = cohere.Client(COHERE_API_KEY)

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)

# Example alternative for vector search
# from weaviate.classes.query import MetadataQuery
# def retrieve_collection_data(collection_name: str, query: str, limit: int = 5) -> list[str]:
#     collection = client.collections.get(collection_name)
#     results = collection.query.hybrid(
#         query=query,
#         limit=limit,
#         return_metadata=MetadataQuery(score=True)
#     )
#     return [
#         ", ".join([f"{k}: {v}" for k, v in obj.properties.items()])
#         for obj in results.objects
#     ]

def get_collection_summaries(collection_names: list[str]) -> dict:
    """
    Return the schema fields and a sample record from each specified collection.

    Args:
        collection_names (list[str]): A list of collection names.

    Returns:
        dict: A dictionary with collection names as keys and summaries as values,
              including 'fields' and 'sample'.
    """
    summaries = {}

    for name in collection_names:
        try:
            collection = client.collections.get(name)
            config = collection.config.get()
            props = [p.name for p in config.properties]

            # Get sample record (if available)
            results = collection.query.fetch_objects(limit=1)
            first = results.objects[0].properties if results.objects else {}

            summaries[name] = {
                "fields": props,
                "sample": first
            }
        except Exception as e:
            summaries[name] = {
                "fields": [],
                "sample": {"error": str(e)}
            }

    return summaries
