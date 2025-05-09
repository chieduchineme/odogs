import pytest
from app.chatbot import userinputToQuery
from unittest.mock import MagicMock

# --- TESTS ---

def test_extract_query_logic_with_filters():
    # Simulate a query with filters
    schema_fields = ['name', 'price', 'category']
    query = "Find all products where price is greater than 50 and category is 'Electronics'"
    
    # Mock the external functionality (e.g., Cohere API call)
    result = userinputToQuery.extract_query_logic(query, schema_fields)
    
    expected_result = {
        'filters': [
            {'field': 'price', 'op': '>', 'value': 50},
            {'field': 'category', 'op': '=', 'value': 'Electronics'}
        ]
    }
    
    assert result == expected_result

def test_extract_query_logic_without_filters():
    # Simulate a query without filters
    schema_fields = ['name', 'price', 'category']
    query = "What is the price of a product?"
    
    result = userinputToQuery.extract_query_logic(query, schema_fields)
    
    expected_result = {}
    
    assert result == expected_result
