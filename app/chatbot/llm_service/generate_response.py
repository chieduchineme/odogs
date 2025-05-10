# llm_service.py
"""
This module handles interactions between natural language inputs and the vector database (Weaviate)
as well as the language model (Cohere). It supports routing logic, schema matching, and RAG-based responses.
"""

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Property
from ..prompts import RAG_PROMPT, clarity_check_prompt
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration: Cohere and Weaviate credentials (with fallback hardcoded values)
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "Gtj6rQ9Z3B1lwkwi8nD17u5V96hK1E8koirk2bDh")

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)


async def generate_response(prompt: str, context_docs: list, chat_history: list):
    """
    Generate a contextual response using the RAG (Retrieval-Augmented Generation) pattern.

    Args:
        prompt (str): The user’s question.
        context_docs (list): A list of context strings (retrieved from Weaviate).
        chat_history (list): Recent chat history.

    Returns:
        str: Final chatbot response, including feedback encouragement if needed.
    """
    context_text = "\n\n".join(context_docs)
    history_text = "\n".join(chat_history)

    # Prepare full prompt for RAG
    full_prompt = RAG_PROMPT.format(
        history=history_text,
        context=context_text,
        question=prompt
    )

    # Generate main response using Cohere chat
    response = co.chat(message=full_prompt)
    main_reply = response.text.strip()

    # Evaluate if the answer is clear or needs refinement
    formatted_clarity_check_prompt = clarity_check_prompt.format(
        prompt=prompt,
        main_reply=main_reply
    )

    clarity_eval = co.generate(
        model="command-r-plus",
        prompt=formatted_clarity_check_prompt,
        max_tokens=5,
        temperature=0,
        stop_sequences=["\n"]
    )

    is_clear = clarity_eval.generations[0].text.strip().lower() == "yes"

    if is_clear:
        return main_reply 
        # + "\n\n💬 Let me know if you need further assistance or have another question!"
    else:
        return main_reply + "\n\n🤔 Would you like to refine your question or add more detail?"
