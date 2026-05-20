# Product Document

## Project Name

ShopWise Agent - AI Shopping Agent

## Track

Track 1: AI Shopping Agent

## Problem

Most ecommerce product discovery flows still depend on search bars, category pages, and manual filters. This works when a shopper already knows the exact product or keyword, but it breaks when the shopper has a fuzzy need such as:

- "I need shoes for daily jogging under Rs 5000."
- "Suggest a gift for my mother."
- "I want headphones for travel and study."

The user has intent, constraints, and preferences, but traditional ecommerce interfaces force them to translate those into filters. That creates friction, confusion, and decision fatigue.

## Target Users

The primary target user is an online shopper who knows the outcome they want but does not know the exact product to buy.

Example users:

- A college student shopping with a fixed budget
- A gift buyer who needs safe recommendations
- A traveler comparing bags or headphones
- A fitness beginner choosing shoes or a smartwatch

The merchant benefits because shoppers get clearer recommendations and move toward purchase with less drop-off.

## Product Goal

Build a conversational shopping assistant that understands what the user needs, asks follow-up questions when needed, narrows the catalog, compares options, explains tradeoffs, and recommends a product with a clean path toward cart.

## Core User Journey

1. User opens the shopping assistant.
2. User describes a need in natural language.
3. The agent extracts intent, product category, use case, and budget.
4. If information is missing, the agent asks follow-up questions.
5. The agent searches the product catalog.
6. The agent ranks relevant products using category match, budget fit, use case match, rating, and stock.
7. The agent recommends the strongest matches.
8. The agent explains why the top product is recommended.
9. The agent gives tradeoffs between options.
10. The agent suggests the best item to add to cart.

## What We Built

ShopWise Agent includes:

- A chat interface for product discovery
- A local Shopify-style product catalog
- Intent and budget extraction
- Product ranking logic
- Follow-up question generation
- Recommendation cards
- Tradeoff explanations
- Cart-ready recommendation message
- Optional OpenAI-powered response polishing

## Key Product Decisions

### Decision 1: Conversation first, filters second

We designed the experience around a chat input because shoppers often express needs better in sentences than through filter menus.

### Decision 2: Ask only useful follow-up questions

The agent does not ask a long survey. It asks for missing information such as category, budget, or use case only when needed.

### Decision 3: Explain recommendations clearly

The submission criteria mention that strong entries should explain why products are recommended. Our assistant always includes a top-pick explanation and tradeoffs.

### Decision 4: Use deterministic ranking with optional LLM wording

Product selection should be reliable. The app uses deterministic logic for ranking so it does not invent products. If an OpenAI key is available, the LLM only improves the wording.

### Decision 5: Keep cart handoff simple

Instead of building a full checkout flow, the agent provides a cart-ready recommendation. This keeps the scope focused on discovery, comparison, and purchase intent.

## What We Chose Not To Build

- Full payment checkout
- Real Shopify Admin API integration
- User login and personalization history
- Merchant dashboard
- Large catalog ingestion
- Real inventory sync

These were left out because the hackathon track focuses on a working shopping agent, product thinking, and clear execution under time constraints.

## Tradeoffs

### Synthetic catalog vs. real store data

We used synthetic product data so the demo can run immediately without Shopify setup. The architecture can later replace `products.json` with Shopify Storefront API data.

### Simple ranking vs. complex recommendation model

A transparent scoring system is easier to explain and debug. A future version could include embeddings, user history, and sales performance.

### Optional LLM vs. required LLM

The app works without an API key, which makes it easier for evaluators to run. The optional LLM layer improves response quality but does not control product truth.

## Success Criteria

The product is successful if:

- The user can describe a shopping need naturally.
- The assistant returns relevant products.
- The assistant asks follow-up questions when needed.
- The assistant explains why a product is recommended.
- The user can understand tradeoffs and confidently choose an item.

## Future Improvements

- Connect to Shopify Storefront API
- Add cart creation and checkout links
- Add semantic search with embeddings
- Add product reviews as recommendation evidence
- Add user preference memory
- Add merchant controls for promoted products and inventory rules
