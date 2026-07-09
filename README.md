# Roast Memory Bot 🔥🧠

A FastAPI chatbot that combines **persistent conversation memory**, a **sarcastic-but-supportive roast personality**, **error handling**, and full **history management (view + delete)** — all backed by PostgreSQL and powered by Groq.

## Features

- **Session-based conversation memory** — each conversation is tracked using a UUID `session_id`, with full message history persisted in PostgreSQL.
- **Custom personality via system prompt** — the bot roasts you casually like a friend, but switches to genuine motivation and advice when things get real.
- **Context-aware replies** — every request rebuilds the full conversation (system prompt + history + new message) before calling the LLM.
- **Error handling** — Groq API failures are caught and return a clean error response instead of crashing the server.
- **History endpoint** — retrieve the full conversation history for any session.
- **Delete endpoint** — clear/reset a session's conversation history.
- **Groq-powered** — uses `llama-3.3-70b-versatile` for fast inference.

## Tech Stack

- FastAPI
- PostgreSQL + SQLAlchemy (ORM)
- Groq API
- Pydantic (request/response validation)
- python-dotenv

## Project Structure

```
├── main.py            # FastAPI app, all routes
├── models.py           # SQLAlchemy Message model (session_id, role, content, created_at)
├── schemas.py           # Pydantic request/response models
├── database.py           # DB engine, session, and Base setup
├── groq_client.py         # Groq API call wrapper
├── system_prompt.py        # Bot personality definition
├── requirements.txt
├── .gitignore
└── README.md
```

## Endpoints

### `POST /chat`
Send a message and get a reply. Maintains conversation memory per session.

**Request:**
```json
{
  "message": "bhai kya haal hai",
  "session_id": null
}
```

**Response:**
```json
{
  "response": "Kya haal hai, dost? Sab theek?",
  "session_id": "1ff6e321-e847-4cec-937e-455dd4b07a88"
}
```

Leave `session_id` as `null` to start a new conversation. Use the returned `session_id` in subsequent requests to continue with full memory.

### `GET /history/{session_id}`
Returns the full message history for a given session.

**Response:**
```json
{
  "session_id": "1ff6e321-e847-4cec-937e-455dd4b07a88",
  "messages": [
    {"role": "user", "content": "bhai kya haal hai"},
    {"role": "assistant", "content": "Kya haal hai, dost? Sab theek?"}
  ]
}
```

### `DELETE /history/{session_id}`
Deletes all stored messages for a given session, effectively resetting the conversation.

**Response:**
```json
{
  "message": "chat is deleted!"
}
```

## How It Works

1. Client sends a `message` and optional `session_id`.
2. If no `session_id` is provided, a new UUID is generated for the session.
3. Previous messages for that session are fetched from PostgreSQL.
4. A conversation list is assembled: `[system prompt] + [past messages] + [new message]`.
5. This list is sent to Groq, wrapped in a try/except block so failures return a clean 500 error instead of crashing.
6. Both the user's message and the bot's reply are saved to the database under the same `session_id`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Create a `.env` file:
   ```
   database_url=postgresql://user:password@localhost:5432/your_db
   groq_api_key=your_groq_api_key
   ```
3. Run the server:
   ```
   uvicorn main:app --reload
   ```
4. Test via `/docs` (Swagger UI).

## Author

Built by Bilal (Dhani Baksh) as part of an ongoing series of FastAPI + AI integration projects, exploring conversation memory, personality design, error handling, and CRUD operations on top of an LLM-backed API.
