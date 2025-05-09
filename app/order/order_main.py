from fastapi import FastAPI, Request
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.order.order_service import order_router


app = FastAPI(
    title="Ecommerce Order API",
    description="Order API.",
    version="1.0.0"
)

# # Include chatbot router
app.include_router(order_router, prefix="/order", tags=["Order"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
