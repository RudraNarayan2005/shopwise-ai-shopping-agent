# Decision Log

## Decision 1: Build Track 1 as a focused product discovery assistant

We chose Track 1 because product discovery is the clearest place to demonstrate agentic commerce. A shopping agent can understand intent, ask questions, compare products, and move the user toward purchase.

## Decision 2: Use Flask and vanilla JavaScript

We chose Flask and vanilla JavaScript because the project needs to be easy to run, easy to review, and simple enough for judges to understand quickly.

## Decision 3: Use a local product catalog

We used `data/products.json` instead of a real Shopify API connection because the submission should run without requiring merchant credentials or external setup.

## Decision 4: Keep product ranking deterministic

We chose deterministic scoring for product selection because recommendation correctness matters. The system should not hallucinate products, prices, or stock.

## Decision 5: Make OpenAI optional

We made the LLM layer optional so the demo still works without an API key. The LLM only polishes the explanation and does not change the selected products.

## Decision 6: Ask follow-up questions only when useful

We avoided a long questionnaire. The assistant asks for missing category, budget, or use case only when those details are not clear.

## Decision 7: Include tradeoffs in the answer

We included tradeoff explanations because a strong shopping assistant should help the user choose, not just list products.

## Decision 8: Stop before full checkout

We did not build full checkout because the core value of this track is product discovery and recommendation. The app provides a cart-ready suggestion as the final step.
