"""
This module defines logic to extract structured query constraints from natural language inputs,
using Cohere's language model. The extracted query logic is intended to be used for filtering
Weaviate database collections.
"""

import cohere
import weaviate
from weaviate.classes.init import Auth
from .prompts import extract_query_logic_prompt
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Get API key from env or use fallback
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "Gtj6rQ9Z3B1lwkwi8nD17u5V96hK1E8koirk2bDh")

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

def extract_query_logic(query: str, schema_fields: list[str]) -> dict:
    """
    Extracts logical filter and sort constraints from a natural language query using Cohere.

    Args:
        query (str): The natural language user query.
        schema_fields (list[str]): List of valid field names from the collection schema.

    Returns:
        dict: A dictionary with keys like 'filters', 'sort_by', 'order', and 'limit', e.g.:
              {
                  "filters": [{"field": "price", "op": "GreaterThan", "value": 100}],
                  "sort_by": "price",
                  "order": "desc",
                  "limit": 50
              }
              Returns an empty dict if parsing fails.
    """
    # Create a comma-separated list of fields for the prompt
    field_list = ", ".join(schema_fields)

    # Fill in the prompt template with the schema and user query
    formatted_prompt = extract_query_logic_prompt.format(
        field_list=field_list,
        query=query
    )

    # Generate a response from Cohere's model
    response = co.generate(
        model="command-r-plus",
        prompt=formatted_prompt,
        max_tokens=10000,
        temperature=0,
        stop_sequences=[";"]  # Optional stop character
    )

    # Parse the result as JSON and return it
    try:
        return json.loads(response.generations[0].text.strip())
    except Exception as e:
        print("JSON parsing error:", e)
        print("Raw output:", response.generations[0].text.strip())
        return {}
