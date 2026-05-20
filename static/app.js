const messages = document.querySelector("#messages");
const form = document.querySelector("#chatForm");
const input = document.querySelector("#messageInput");
const productList = document.querySelector("#productList");

function money(value) {
  return `Rs ${Number(value).toLocaleString("en-IN")}`;
}

function addMessage(role, content) {
  const article = document.createElement("article");
  article.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  if (typeof content === "string") {
    const paragraph = document.createElement("p");
    paragraph.textContent = content;
    bubble.appendChild(paragraph);
  } else {
    bubble.appendChild(content);
  }

  article.appendChild(bubble);
  messages.appendChild(article);
  messages.scrollTop = messages.scrollHeight;
}

function renderProducts(products) {
  productList.innerHTML = "";

  products.forEach((product) => {
    const card = document.createElement("article");
    card.className = "product-card";

    const image = document.createElement("img");
    image.src = product.image;
    image.alt = product.name;

    const body = document.createElement("div");
    const title = document.createElement("h3");
    title.textContent = product.name;

    const price = document.createElement("div");
    price.className = "meta";
    price.innerHTML = `<span>${money(product.price)}</span><span>${product.rating} rating</span><span>${product.stock} in stock</span>`;

    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = product.category;

    const benefit = document.createElement("p");
    benefit.textContent = product.benefit;
    benefit.style.margin = "8px 0 0";

    body.append(title, price, tag, benefit);

    if (product.match_reasons && product.match_reasons.length) {
      const reasons = document.createElement("ul");
      reasons.className = "reason-list";
      product.match_reasons.forEach((reason) => {
        const item = document.createElement("li");
        item.textContent = reason;
        reasons.appendChild(item);
      });
      body.appendChild(reasons);
    }

    card.append(image, body);
    productList.appendChild(card);
  });
}

function renderAssistantReply(reply) {
  const wrapper = document.createElement("div");

  const intro = document.createElement("p");
  intro.textContent = reply.llm_summary || reply.intro;
  wrapper.appendChild(intro);

  if (!reply.llm_summary) {
    const explanation = document.createElement("p");
    explanation.textContent = reply.explanation;
    wrapper.appendChild(explanation);
  }

  if (reply.questions && reply.questions.length) {
    const question = document.createElement("p");
    question.textContent = `Follow-up: ${reply.questions.join(" ")}`;
    wrapper.appendChild(question);
  }

  if (reply.tradeoffs && reply.tradeoffs.length) {
    const tradeoff = document.createElement("p");
    tradeoff.textContent = `Tradeoff: ${reply.tradeoffs.join(" ")}`;
    wrapper.appendChild(tradeoff);
  }

  if (reply.cart_suggestion) {
    const cart = document.createElement("p");
    cart.textContent = reply.cart_suggestion.message;
    wrapper.appendChild(cart);
  }

  const grid = document.createElement("div");
  grid.className = "assistant-card-grid";
  reply.recommendations.forEach((product) => {
    const card = document.createElement("div");
    card.className = "mini-card";
    card.innerHTML = `<strong>${product.name}</strong><span>${money(product.price)} | ${product.rating} rating</span>`;
    grid.appendChild(card);
  });
  wrapper.appendChild(grid);

  addMessage("assistant", wrapper);
  renderProducts(reply.recommendations);
}

async function loadCatalog() {
  const response = await fetch("/api/products");
  const products = await response.json();
  renderProducts(products.slice(0, 5));
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";
  const button = form.querySelector("button");
  button.disabled = true;
  button.textContent = "Thinking";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error("Chat request failed");
    }

    const reply = await response.json();
    renderAssistantReply(reply);
  } catch (error) {
    addMessage("assistant", "Something went wrong while generating recommendations. Please try again.");
  } finally {
    button.disabled = false;
    button.textContent = "Send";
    input.focus();
  }
});

loadCatalog();
