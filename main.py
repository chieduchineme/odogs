# ecommerce-chatbot/main.py

from fastapi import FastAPI, Request
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot.chatbot_service import router as chatbot_router
from app.product.product_service import product_router
from app.order.order_service import order_router


app = FastAPI(
    title="Ecommerce APP",
    description="Ecommerce app facilitating orders, products and powered by chatbot",
    version="1.0.0"
)

# # Include chatbot, product and order routers
app.include_router(product_router, prefix="/product", tags=["Product"])
app.include_router(order_router, prefix="/order", tags=["Order"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Global exception handler for validation errors (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Please enter a valid question or sentence."},
    )
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
