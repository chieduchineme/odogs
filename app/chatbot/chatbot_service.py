from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..chatbot.rag_agent import rag_agent

router = APIRouter()


class ChatRequest(BaseModel):
    user_input: str = Field(..., example="What are the best electronic devices under $100?")

    class Config:
        schema_extra = {
            "example": {
                "user_input": "Can you recommend a good product with a great camera?"
            }
        }


class ChatResponse(BaseModel):
    response: str = Field(..., example="Sure! Based on reviews, the Google Pixel 7 is highly rated for its camera.")


@router.post(
    "/ask",
    response_model=ChatResponse,
    summary="Ask the chatbot a product-related question",
    description="""
    This endpoint lets users interact with the ecommerce chatbot.

    It uses a Retrieval-Augmented Generation (RAG) approach backed by a Weaviate vector database.
    The chatbot provides intelligent product recommendations and answers.

    **Request Body**:
    - `user_input` (str): The user's question or query.

    **Response**:
    - `response` (str): The chatbot's reply.
    """,
    tags=["Chatbot"]
)
async def ask_chatbot(payload: ChatRequest):
    """
    Ask the chatbot a question about products or categories.

    Uses a RAG agent with vector similarity search to provide contextual answers.
    """
    try:
        result = await rag_agent(payload.user_input)
        return ChatResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error from chatbot: {str(e)}")
