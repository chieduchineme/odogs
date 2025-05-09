from fastapi import FastAPI, Request
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot.chatbot_service import router as chatbot_router

app = FastAPI(
    title="🛍️ Ecommerce Chatbot API",
    description="""
    This API enables interaction with an intelligent ecommerce chatbot.

    **Tech Stack**:
    - LLM (Language Model)
    - Vector Database: Weaviate
    - Retrieval-Augmented Generation (RAG)

    **Main Features**:
    - Ask product-related questions
    - Get recommendations based on vector similarity
    - Integrates with semantic search
    """,
    version="1.0.0",
    contact={
        "name": "Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# 🔄 Include chatbot endpoint
app.include_router(
    chatbot_router,
    prefix="/chatbot",
    tags=["Chatbot"],
    responses={404: {"description": "Not found"}},
)

# 🌐 Enable CORS for development/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific domains for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚨 Global handler for validation (422) errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Please enter a valid question or sentence."},
    )

# 🚀 Entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
