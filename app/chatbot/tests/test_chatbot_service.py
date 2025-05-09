import pytest
from httpx import AsyncClient
from ....main import app

@pytest.mark.asyncio
async def test_chatbot_ask_valid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/chatbot/ask", json={"user_input": "Hello, what products are on sale?"})
        assert response.status_code == 200
        assert "response" in response.json()

@pytest.mark.asyncio
async def test_chatbot_ask_invalid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/chatbot/ask", json={"bad_field": "Missing user_input"})
        assert response.status_code == 422
        assert "detail" in response.json()
