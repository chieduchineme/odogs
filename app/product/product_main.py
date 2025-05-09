from fastapi import FastAPI, Request
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.product.product_service import product_router


app = FastAPI(
    title="Ecommerce Chatbot API",
    description="Chatbot powered by LLM + Weaviate (Vector Database) + RAG",
    version="1.0.0"
)

# # Include chatbot router
app.include_router(product_router, prefix="/product", tags=["Product"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
