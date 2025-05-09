import pytest
from app.chatbot.rag_agent import rag_agent
from app.chatbot.memory import Memory

@pytest.fixture(autouse=True)
def reset_memory():
    # Clear memory before each test to avoid cross-test state
    Memory()._history.clear()

def test_rag_agent_too_long_input():
    long_input = "a" * 5000
    response = pytest.run(rag_agent(long_input))
    assert "too long" in response.lower()

@pytest.mark.asyncio
async def test_rag_agent_llm_only(monkeypatch):
    async def mock_analyze_prompt(prompt, history):
        return {"type": "llm"}

    async def mock_generate_response(prompt, context_docs, chat_history):
        return "This is a mock LLM-only response."

    monkeypatch.setattr("app.chatbot.rag_agent.analyze_prompt", mock_analyze_prompt)
    monkeypatch.setattr("app.chatbot.rag_agent.generate_response", mock_generate_response)

    response = await rag_agent("What is the weather today?")
    assert "mock llm-only response" in response.lower()

@pytest.mark.asyncio
async def test_rag_agent_database_path(monkeypatch):
    async def mock_analyze_prompt(prompt, history):
        return {"type": "database", "collections": ["products"]}

    async def mock_generate_response(prompt, context_docs, chat_history):
        return "This is a mock DB-enhanced response."

    def mock_get_collection_summaries(names):
        return {"products": {"fields": ["name", "price"], "sample": {"name": "ItemX"}}}

    def mock_retrieve_collection_data(collection, query, limit=50000):
        return ["name: ItemX, price: 10"]

    monkeypatch.setattr("app.chatbot.rag_agent.analyze_prompt", mock_analyze_prompt)
    monkeypatch.setattr("app.chatbot.rag_agent.generate_response", mock_generate_response)
    monkeypatch.setattr("app.chatbot.rag_agent.get_collection_summaries", mock_get_collection_summaries)
    monkeypatch.setattr("app.chatbot.rag_agent.retrieve_collection_data", mock_retrieve_collection_data)

    response = await rag_agent("Show me all cheap products")
    assert "mock db-enhanced response" in response.lower()
