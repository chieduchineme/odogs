import cohere
from dotenv import load_dotenv
from .get_collection_schemas import get_collection_schemas
from ..prompts import routing_prompt
import os

# Load environment variables
load_dotenv()

# Configuration: Cohere and Weaviate credentials (with fallback hardcoded values)
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "Gtj6rQ9Z3B1lwkwi8nD17u5V96hK1E8koirk2bDh")

co = cohere.Client(COHERE_API_KEY)

async def analyze_prompt(prompt: str, history: list[str] = []):
    """
    Analyze the user prompt to determine whether it should be routed to the LLM or database (Weaviate).

    If routed to the database, also determine which collections are relevant.

    Args:
        prompt (str): The user’s input.
        history (list[str], optional): Recent conversation history. Defaults to [].

    Returns:
        dict: A routing result like:
              - {"type": "llm"} if handled by LLM
              - {"type": "database", "collections": [...] } if routed to vector DB
    """
    schemas = get_collection_schemas()
    schema_summary = "\n".join(
        [f"- {cls}: {', '.join(props)}" for cls, props in schemas.items()]
    )
    history_text = "\n".join(history[-5:])  # Last few turns of conversation

    # Generate a routing decision
    formatted_routing_prompt = routing_prompt.format(
        schema_summary=schema_summary,
        history_text=history_text,
        prompt=prompt
    )

    response = co.generate(
        model="command-r-plus",
        prompt=formatted_routing_prompt,
        max_tokens=10,
        temperature=0,
        stop_sequences=["\n"]
    )

    route = response.generations[0].text.strip().lower()
    print("Routing decision:", route)

    if "[database]" not in route:
        return {"type": "llm"}

    # Schema identification: determine relevant collections
    schema_identification_prompt = f"""Based on the following user query and recent conversation:

User: "{prompt}"
History:
{history_text}

And the available collections with fields:
{schema_summary}

List the relevant collection names (comma-separated) from: {', '.join(schemas.keys())}
Answer:"""

    schema_response = co.generate(
        model="command-r-plus",
        prompt=schema_identification_prompt,
        max_tokens=20,
        temperature=0,
        stop_sequences=["\n"]
    )

    raw_result = schema_response.generations[0].text.strip().lower()
    print("Matched collections:", raw_result)

    matched_collections = [
        coll.strip() for coll in raw_result.split(",") if coll.strip() in schemas
    ]

    if not matched_collections:
        return {"type": "llm"}

    return {
        "type": "database",
        "collections": matched_collections
    }