# prompts.py

extract_query_logic_prompt = """
You are an assistant that converts user questions into SQL queries.

Available fields: {field_list}

Write a SQL query (no explanation) that best captures the intent of the following question:
"{query}"
Only return the SQL string.
"""


RAG_PROMPT = """
You are an AI assistant. You are given a chat history, context documents, and a user question.

History:
{history}

Context:
{context}

Question:
{question}

Answer the question using only the context and chat history. Be concise and helpful.
"""


routing_prompt = """You are an intelligent router that decides whether a user question should be answered using a vector database or a language model.

The following collections and their fields exist in the vector database:
{schema_summary}

Conversation history:
{history_text}

Current user query: "{prompt}"

If the user's query can be answered using any of this data, classify it as [Database]. Otherwise, classify it as [LLM].

Answer:"""


schema_identification_prompt = """Based on the following user query and recent conversation:

User: "{prompt}"
History:
{history_text}

And the available collections with fields:
{schema_summary}

List the relevant collection names (comma-separated) from: {', '.join(schemas.keys())}
Answer:"""


clarity_check_prompt = """
You are an assistant that evaluates if a given response provides a clear and complete answer to a user's question.

User Question: {prompt}

Assistant Response: {main_reply}

Answer "Yes" if the response fully addresses the user's query and needs no follow-up.
Answer "No" if the response is vague, partial, uncertain, or could benefit from clarification.
Answer:"""
