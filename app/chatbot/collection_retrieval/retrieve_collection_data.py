import cohere
import weaviate
from weaviate.classes.init import Auth
from ..userinputToQuery import extract_query_logic
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

def retrieve_collection_data(collection_name: str, query: str, limit: int = 5) -> list[str]:
    """
    Retrieve objects from a Weaviate collection based on a natural language query.

    Args:
        collection_name (str): The name of the Weaviate collection.
        query (str): The user's natural language query.
        limit (int): Maximum number of records to return.

    Returns:
        list[str]: A list of string representations of the retrieved objects.
    """
    collection = client.collections.get(collection_name)
    config = collection.config.get()
    schema_fields = [p.name for p in config.properties]

    # Extract filtering and sorting logic from natural language
    logic = extract_query_logic(query, schema_fields)

    # Build the filter object based on logic
    weaviate_filter = None
    if "filters" in logic:
        conditions = []
        for f in logic["filters"]:
            field = f["field"]
            op = f["op"]
            val = f["value"]

            # Infer Weaviate value type
            filter_value = (
                {"valueText": val} if isinstance(val, str)
                else {"valueNumber": val} if isinstance(val, (int, float))
                else {"valueDate": val} if "date" in field.lower()
                else {}
            )

            condition = {
                "path": [field],
                "operator": op,
                **filter_value
            }
            conditions.append(condition)

        # Combine multiple conditions using AND
        weaviate_filter = conditions[0] if len(conditions) == 1 else {
            "operator": "And",
            "operands": conditions
        }

    # Apply sorting if specified
    sort = None
    if "sort_by" in logic:
        sort = [{
            "path": logic["sort_by"],
            "order": logic.get("order", "asc").upper()
        }]

    # Execute the query with filters and sorting
    results = collection.query.fetch_objects(
        filters=weaviate_filter,
        sort=sort,
        limit=logic.get("limit", limit),
        return_metadata=["score"],
    )

    # Format results into a readable list
    return [
        ", ".join([f"{k}: {v}" for k, v in obj.properties.items()])
        for obj in results.objects
    ]
