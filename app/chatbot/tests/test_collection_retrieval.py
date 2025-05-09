import pytest
from app.chatbot.collection_retrieval.get_collection_summaries import get_collection_summaries
from app.chatbot.collection_retrieval.retrieve_collection_data import retrieve_collection_data
import pytest
from unittest.mock import patch, MagicMock

mock_collections = {
    "product": {
        "properties": ["id", "name", "price"],
        "sample": {"id": "p1", "name": "Widget", "price": 25.0},
        "data": [
            {"id": "p1", "name": "Widget", "price": 25.0},
            {"id": "p2", "name": "Gadget", "price": 15.5}
        ]
    }
}

@patch("app.collection_retrieval.get_collection_summaries.client")
def test_get_collection_summaries(mock_client):
    mock_collection = MagicMock()
    mock_collection.config.get.return_value.properties = [
        MagicMock(name="id"), MagicMock(name="name"), MagicMock(name="price")
    ]
    mock_collection.query.fetch_objects.return_value.objects = [MagicMock(properties=mock_collections["product"]["sample"])]

    mock_client.collections.get.return_value = mock_collection

    result = get_collection_summaries(["product"])
    assert "product" in result
    assert "id" in result["product"]["fields"]
    assert isinstance(result["product"]["sample"], dict)

@patch("app.collection_retrieval.retrieve_collection_data.client")
@patch("app.collection_retrieval.retrieve_collection_data.extract_query_logic")
def test_retrieve_collection_data(mock_extract, mock_client):
    mock_extract.return_value = {"filters": [], "limit": 2}
    mock_collection = MagicMock()
    mock_collection.config.get.return_value.properties = [
        MagicMock(name="id"), MagicMock(name="name"), MagicMock(name="price")
    ]
    mock_collection.query.fetch_objects.return_value.objects = [
        MagicMock(properties=d) for d in mock_collections["product"]["data"]
    ]

    mock_client.collections.get.return_value = mock_collection

    result = retrieve_collection_data("product", "List all products", limit=2)
    assert len(result) == 2
    assert "name: Widget" in result[0]
