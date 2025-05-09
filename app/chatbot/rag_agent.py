"""
RAG Agent Module

This module implements the main RAG (Retrieval-Augmented Generation) workflow by integrating:
- User prompt processing
- Collection relevance identification via schema analysis
- Retrieval of contextually relevant data from Weaviate collections
- Response generation using a Cohere-powered language model

"""

from .llm_service.analyze_prompt_db_or_llm import analyze_prompt
from .llm_service.generate_response import generate_response
from .collection_retrieval.retrieve_collection_data import retrieve_collection_data
from .collection_retrieval.get_collection_summaries import get_collection_summaries
from .memory import Memory

memory = Memory()

MAX_USER_INPUT_LENGTH = 4000  # Limit to ensure input stays within model constraints


async def rag_agent(user_input: str) -> str:
    """
    Main function that handles user queries using RAG (Retrieval-Augmented Generation).

    Steps:
    - Validates input length
    - Stores user input in memory
    - Uses LLM to determine whether to query DB or generate directly
    - Retrieves relevant documents if database access is needed
    - Builds prompt context with schema and data
    - Generates a natural language response using the LLM

    Args:
        user_input (str): The query provided by the user.

    Returns:
        str: A final response string, either generated directly or augmented with DB content.
    """

    if len(user_input) > MAX_USER_INPUT_LENGTH:
        return "⚠️ The message you submitted was too long. Please shorten your input and try again."

    # Store user query in conversation memory
    memory.store_user_message(user_input)

    # Analyze whether prompt is LLM-only or database-related
    context_info = await analyze_prompt(user_input, history=memory.get_history())

    if "error" in context_info:
        return f"⚠️ {context_info['error']}"

    # If not database-related, fallback to LLM generation only
    if context_info["type"] != "database":
        llm_reply = await generate_response(user_input, [], memory.get_history())
        memory.store_bot_response(llm_reply)
        return llm_reply

    # Get list of matched collections for context retrieval
    matched_collections = context_info["collections"]
    print("matched_collections :", matched_collections)

    all_context_docs = []

    # Get schema and sample for each matched collection
    collection_summaries = get_collection_summaries(matched_collections)
    print("collection_summaries :", collection_summaries)

    # Fetch matching objects from each collection
    for collection in matched_collections:
        docs = retrieve_collection_data(collection, user_input)
        all_context_docs.extend(docs)

    # Format schema and sample summary as part of context
    schema_context = "\n\n".join([
        f"Collection: {name}\nFields: {', '.join(summary['fields'])}\nSample: {summary['sample']}"
        for name, summary in collection_summaries.items()
    ])

    # Construct final context to feed into LLM
    context_text = f"User Query: {user_input}\n\n{schema_context}\n\nRelevant Data:\n" + "\n".join(all_context_docs)
    print("context_text :", context_text)

    # Generate response using LLM with schema and data context
    llm_reply = await generate_response(user_input, [context_text], memory.get_history())
    memory.store_bot_response(llm_reply)
    return llm_reply
