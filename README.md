# ShopWise Agent - AI Shopping Agent

Track 1 submission for the Kasparro Agentic Commerce Hackathon.

ShopWise Agent is a conversational shopping assistant that helps users discover products from a Shopify-style catalog. It asks follow-up questions, narrows choices, compares products, explains recommendations, and guides the user toward adding an item to cart.

## Problem Statement

Online shoppers often know what they need but struggle to choose from large product catalogs. Filters are rigid, search needs exact keywords, and product pages do not explain tradeoffs clearly. ShopWise Agent turns product discovery into a guided conversation.

## Core Features

- Chat-based product discovery
- Intent extraction from natural language
- Smart follow-up questions when the request is unclear
- Product filtering by category, price, use case, rating, and availability
- Recommendation explanations with tradeoffs
- Side-by-side product comparison
- Cart-ready recommendation summary
- Works with local sample catalog data
- Optional OpenAI integration through `OPENAI_API_KEY`

## Tech Stack

- Python
- Flask
- Vanilla JavaScript
- HTML/CSS
- Local JSON product catalog
- Optional OpenAI API

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── .env.example
├── data/
│   └── products.json
├── static/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── PRODUCT_DOCUMENT.md
├── TECHNICAL_DOCUMENT.md
├── DECISION_LOG.md
└── CONTRIBUTION_NOTE.md
```

## Setup

1. Create a virtual environment.

```bash
python -m venv .venv
```

2. Activate it.

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Optional: create a `.env` file from `.env.example`.

```bash
cp .env.example .env
```

5. Run the app.

```bash
python app.py
```

6. Open the app.

```text
http://127.0.0.1:5000
```

## Demo Script

Try these prompts:

```text
I need running shoes under 5000 for daily jogging.
Suggest a gift for my mother under 3000.
Compare the best headphones for travel.
I want a backpack for college and laptop use.
```

## Demo Video

```text
Demo video: https://drive.google.com/file/d/1Tw18RKi_ZOilHvz5-BGaP0-e38NQz_Ah/view?usp=sharing
```

## Screenshots

```text
assets/screenshots/demo-chat.png
```
