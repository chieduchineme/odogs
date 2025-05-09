 Step 2: Microservices Design Overview
We'll create 3 microservices using FastAPI (or Flask if preferred):

1. Chat Service
Accepts user queries.

Determines whether the intent is related to a product or an order.

Routes to appropriate microservice.

2. Product Search Service
Loads the Product Dataset.

Embeds descriptions/titles using vector DB (e.g., FAISS or simple in-memory sim).

Handles similarity search based on natural queries.

3. Order Lookup Service
Interfaces with the provided mock API.

Retrieves and formats order data by Customer_Id, Category, or Priority.

🧠 Step 3: RAG Integration Plan
Use a lightweight RAG mechanism:

Preprocess & embed product titles + descriptions.

On product query:

Extract semantic meaning using sentence embeddings (e.g., sentence-transformers).

Retrieve top-N similar items.

Generate natural language response using template or LLM (e.g., OpenAI, local LLM).

