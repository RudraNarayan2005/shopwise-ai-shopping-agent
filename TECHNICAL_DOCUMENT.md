# Technical Document

## Project Name

ShopWise Agent - AI Shopping Agent

## System Overview

ShopWise Agent is a Flask-based web application with a browser frontend and a Python backend. The frontend provides the chat interface and product cards. The backend handles product loading, intent extraction, product scoring, follow-up question generation, and optional LLM response polishing.

## Architecture

```text
User
  |
  v
Browser UI
  |
  v
Flask API
  |
  +--> Intent parser
  |
  +--> Product ranking engine
  |
  +--> Follow-up question generator
  |
  +--> Local product catalog
  |
  +--> Optional OpenAI response polishing
  |
  v
Recommendation response
```

## Components

### Frontend

Files:

- `static/index.html`
- `static/styles.css`
- `static/app.js`

Responsibilities:

- Render chat messages
- Send user messages to `/api/chat`
- Render recommendation responses
- Render product cards
- Show prices, ratings, stock, and match reasons

### Backend

File:

- `app.py`

Responsibilities:

- Serve the web app
- Load product data from JSON
- Expose `/api/products`
- Expose `/api/chat`
- Parse user budget and category
- Infer use cases
- Score and rank products
- Generate follow-up questions
- Return structured recommendation data

### Product Catalog

File:

- `data/products.json`

Each product contains:

- `id`
- `name`
- `category`
- `price`
- `rating`
- `stock`
- `image`
- `benefit`
- `tags`
- `use_cases`

## API Design

### GET `/api/products`

Returns the available product catalog.

Example response:

```json
[
  {
    "id": "shoe-001",
    "name": "AeroRun Daily Trainers",
    "category": "Shoes",
    "price": 3999
  }
]
```

### POST `/api/chat`

Request:

```json
{
  "message": "I need running shoes under 5000 for daily jogging"
}
```

Response:

```json
{
  "intro": "Based on your needs, these are the best matches from the catalog.",
  "questions": [],
  "recommendations": [],
  "explanation": "My top pick is AeroRun Daily Trainers...",
  "tradeoffs": [],
  "cart_suggestion": {
    "product_id": "shoe-001",
    "name": "AeroRun Daily Trainers",
    "message": "Add AeroRun Daily Trainers to cart if you want the strongest overall match."
  }
}
```

## Product Ranking Logic

The backend scores each product using:

- Category match
- Budget fit
- Use case match
- Tag match
- Customer rating
- Stock availability

This keeps recommendations explainable and prevents the assistant from inventing products.

## LLM Usage

The app has an optional OpenAI integration. If `OPENAI_API_KEY` is present, the backend sends the already-selected product recommendations to the model and asks it to rewrite the response in a concise shopping-assistant tone.

Important boundary:

The LLM does not choose products or prices. It only improves the natural-language explanation. Product truth comes from the catalog and ranking logic.

## Failure Handling

### Empty message

The backend returns a `400` error if the user sends an empty message.

### Missing budget or unclear request

The assistant asks follow-up questions instead of guessing too much.

### No exact product match

The assistant returns the closest available products and says it could not find an exact match.

### Out-of-stock products

Out-of-stock products receive a negative score and are not prioritized.

### OpenAI API failure

If the optional LLM call fails, the app falls back to deterministic recommendation text.

## Security Notes

- API keys are loaded from `.env`.
- `.env` should not be committed.
- `.env.example` is included to show required variables.
- The app does not store user messages in a database.

## Known Limitations

- Uses local sample data instead of live Shopify data
- No real cart creation
- No login or user memory
- Simple keyword-based intent parser
- No embeddings or semantic search yet

## Future Technical Improvements

- Replace local JSON with Shopify Storefront API
- Add cart and checkout URL creation
- Add embeddings for semantic product matching
- Add conversation memory
- Add product review summarization
- Add automated tests for ranking behavior
- Deploy using Render, Railway, or Vercel plus a Python backend
