import pytest
from app.chatbot.llm_service.analyze_prompt_db_or_llm import analyze_prompt
from app.chatbot.llm_service.generate_response import generate_response
from app.chatbot.llm_service.get_collection_schemas import get_collection_schemas
from unittest.mock import patch, MagicMock


@patch("app.llm_service.get_collection_schemas.client")
def test_get_collection_schemas(mock_client):
    mock_config = MagicMock()
    mock_config.properties = [MagicMock(name="id"), MagicMock(name="price")]
    mock_collection = MagicMock()
    mock_collection.config.get.return_value = mock_config

    mock_client.collections.list_all.return_value = ["product"]
    mock_client.collections.get.return_value = mock_collection

    schemas = get_collection_schemas()
    assert "product" in schemas
    assert "id" in schemas["product"]

@patch("app.llm_service.analyze_prompt_db_or_llm.co")
@patch("app.llm_service.analyze_prompt_db_or_llm.get_collection_schemas")
@pytest.mark.asyncio
async def test_analyze_prompt(mock_get_schemas, mock_co):
    mock_get_schemas.return_value = {
        "product": ["id", "name", "price"],
        "order": ["id", "total"]
    }

    # Routing decision
    routing_response = MagicMock()
    routing_response.generations = [MagicMock(text="[database]")]
    mock_co.generate.side_effect = [routing_response, routing_response]

    result = await analyze_prompt("How much did I spend?", history=[])
    assert result["type"] == "database"

@patch("app.llm_service.generate_response.co")
@pytest.mark.asyncio
async def test_generate_response(mock_co):
    mock_co.chat.return_value.text = "You spent $100."
    clarity_check = MagicMock()
    clarity_check.generations = [MagicMock(text="yes")]
    mock_co.generate.return_value = clarity_check

    result = await generate_response("How much did I spend?", ["Order data..."], [])
    assert "💬" in result
