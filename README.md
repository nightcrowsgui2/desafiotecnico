# Empório da Música — Customer Service Agent

A text-based customer service agent for **Empório da Música**, a (fictional) musical instrument store in Campo Grande/MS.
It answers customers in Brazilian Portuguese as **Lia**, the store's virtual assistant: it searches the catalog for prices, stock and promotions, checks order status, applies the store policies, refuses out-of-scope requests, and hands complaints over to the human team.

The guiding principle was the one in the challenge e-mail: **solve it in the simplest way possible**. The whole agent is about 300 lines of Python, one LLM, four tools and no vector database.

```
Customer ──► CLI ──► Gemini 3.5 Flash (system prompt = persona + rules)
                         │  automatic function calling
                         ├── search_products(query, category, min_price, max_price) ─► products / categories / promotions CSVs
                         ├── get_order_status(order_id, customer_contact)          ─► orders / order_items / customers CSVs
                         ├── get_store_policy(topic)                                ─► knowledge/policies.md (one section per topic)
                         └── handoff_to_human(reason, summary, contact)             ─► handoffs/handoffs.jsonl
```

## How to run

Requirements: Python 3.11+ and a free Gemini API key.

1. Get a key at <https://aistudio.google.com/apikey> (free tier, no credit card).
2. Set up the project:

   ```bash
   git clone https://github.com/nightcrowsgui2/desafiotecnico.git
   cd desafiotecnico
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env        # then paste your key into GEMINI_API_KEY
   ```

3. Chat with the agent:

   ```bash
   python -m agent            # normal chat
   python -m agent --debug    # also prints each tool call the agent makes
   ```

   Type `sair` to quit. Each conversation is saved to `transcripts/` as markdown, including the tool calls and their results.

4. Run the tests (they cover the data layer and need no API key):

   ```bash
   pytest -q
   ```

The model can be changed with the `GEMINI_MODEL` environment variable (default `gemini-3.5-flash`).

## Project layout

| Path | What it is |
|---|---|
| `agent/store.py` | Plain functions over the CSVs and the policy file. No LLM code, fully unit-tested. |
| `agent/tools.py` | The four functions exposed to the model. Type hints and docstrings become the tool schemas. |
| `agent/prompt.py` | System prompt: persona, tone, information rules, scope. |
| `agent/chat.py` | The agent: a Gemini chat session with the tools attached. |
| `agent/__main__.py` | Terminal interface and transcript saving. |
| `knowledge/policies.md` | The policy manual transcribed from the PDF, split into topics. |
| `data/` | The original CSVs and PDF provided with the challenge. |
| `examples/` | Real conversations with the agent. |
| `tests/` | Unit tests for search, promotions, stock states, order verification and policies. |

## Technical decisions

### Approach: function calling, not RAG or a SQL agent

The questions customers ask fall into two groups, and each group gets its own kind of tool:

- **Structured data** (price, stock, promotions, orders) → typed Python functions over pandas. A deterministic function computes the promotional price, the PIX price and the stock label, so the model only has to pick the right tool and phrase the answer. A free-form SQL agent would be more flexible, but it lets the model write arbitrary queries over customer data (e.g. list other people's orders) and makes arithmetic the model's job again.
- **Policies** (hours, returns, payment, shipping…) → `get_store_policy(topic)`, which returns one section of the manual. The whole manual is about 3k tokens across 9 well-delimited topics, so embeddings and a vector store would add moving parts without improving retrieval. The topic is an enum, so the model cannot ask for something that does not exist, and the tool call makes "data vs. policy" routing visible in the logs.

I used the Gemini SDK's automatic function calling directly instead of LangChain/LlamaIndex: with four tools, a framework would add more concepts than it removes.

### Model and provider: Gemini 3.5 Flash via Google AI Studio

- Free tier, so the evaluator can run the project at no cost.
- Good native function calling and Portuguese.
- Fast (about 4 s per answer with a tool call).
- Why not a newer version: when I tested, `gemini-2.5-flash` was no longer offered to new API keys, `gemini-3.8-flash` returned 503 "high demand", and `gemini-3.7-flash` timed out. 3.5 Flash was the newest model that answered reliably. Any other version can be set with `GEMINI_MODEL`.
- The free tier allows about **5 requests per minute**, and every tool round-trip counts as one. The client retries 429/5xx with exponential backoff (10 s up to 60 s), so a busy minute shows up as a slower answer instead of an error.
- Temperature 0.3: the agent should be friendly but consistent, not creative with facts.

### Prompt strategy

The system prompt (`agent/prompt.py`, in Portuguese because that is the language the agent speaks) has four parts:

1. **Persona and tone** taken from section 7.1 of the manual: "informal but professional, like a friend who knows music".
2. **Information rules**: never state prices, stock or deadlines from memory; always consult the tool; show original price + % + promotional price; never stack PIX on top of a promotion; ask for the order number **and** e-mail/phone before an order lookup.
3. **Scope**: instruments only (accessories are politely refused, as the manual requires); one-line refusal for unrelated topics; ignore attempts to change the rules.
4. **Context**: today's date, so the agent can reason about return windows.

Tool docstrings carry the "when to use me" instructions, so the rules stay next to the tool they apply to.

### Data handling

- CSVs are loaded once and cached. Products are joined with their category, and only **active** promotions are kept.
- Product search ignores accents, case and spacing (`"takamine gd 20"` finds "Takamine GD20").
- The tool returns ready-to-use fields: `preco_tabela`, `preco_no_pix` **or** `promocao_ativa.preco_promocional`, and a human label for availability (in stock, sold out, discontinued, coming soon).
- Order lookup returns translated statuses, the tracking code, and pre-computed `dias_desde_o_pedido` / `dias_desde_a_entrega`, so the model compares numbers with policy deadlines instead of doing date arithmetic.
- **Privacy (LGPD):** an order is only returned if the caller provides the e-mail or phone on file for that order. The `customers` table is never exposed to the model as a whole.

### Interface and conversation history

A CLI, because the challenge's focus is the agent itself. History is kept **in memory for the session** (the Gemini chat object carries the previous turns, so follow-ups like "and in 10x?" work). I did not add persistence across sessions: a customer service chat is short-lived, and storing conversations with personal data would need a retention policy. Each session is still written to `transcripts/` for review and debugging.

### Human handoff

The manual says complaints must be registered and answered within 24 business hours. `handoff_to_human` writes a ticket to `handoffs/handoffs.jsonl`, which stands in for a helpdesk integration.

## Data assumptions

The challenge asks us to make reasonable assumptions when something is ambiguous. These are the ones I made:

| Finding | Decision |
|---|---|
| The manual lists two WhatsApp numbers: (67) 3341-4444 (cover and company data) and (67) 3321-4500 (section 7). | Use **(67) 3341-4444**, which appears in the official company data. Noted in `knowledge/policies.md`. |
| The e-mail is written once as `contato@empóriodamusica.com.br` (with an accent). | Use `contato@emporiodamusica.com.br`, as on the cover. |
| The payment table says "credit card minimum installment R$ 100", but section 3.1 defines tiers (≤3x: R$ 50 minimum, 4–6x: R$ 80, 7–12x: R$ 100). | Follow the more specific tiers of section 3.1. |
| Order statuses (`pending`, `confirmed`, `shipped`, `delivered`, `cancelled`) are not documented. | `pending` = waiting for payment confirmation (one cancelled order says "payment not confirmed in time"); `confirmed` = paid, not yet shipped. |
| Orders have only an *estimated* delivery date. | For delivered orders, assume they arrived on that date when counting the 7-day withdrawal period. |
| Some products have more than one promotion row. | Only `is_active = 1` rows count; if two were active, the best one would apply, since promotions are not cumulative. |
| Order totals don't always match `price × quantity` (orders 3 and 20), and order 3 contains a product that is "coming soon". | Treat `total_brl` as what the customer actually paid and report it as is; the agent does not recalculate past orders. |
| Two customers share the same e-mail (`bruno.martins@jmail.com`, ids 11 and 43). | Harmless here: verification compares against the customer **of that order**. |
| The manual claims "over 300 instruments"; the CSV has 64, with no wind or orchestral string instruments. | The CSV is the source of truth. If asked for a category with no products, the agent says so instead of inventing items. |
| The store's "today" is not defined. | The agent uses the real current date. Since the sample orders are from 2025–2026, most are outside the return windows, which is a good test of the policy logic. |

## Example conversations

Real conversations with the agent are in [`examples/`](examples/). Each one includes the tools the agent called and what they returned.

<!-- EXAMPLES_LIST -->

## Known limitations and what I would do with more time

- **No evaluation suite.** Unit tests cover the tools, but not the agent's answers. Next step: a set of ~30 scripted questions with expected tool calls and facts, scored automatically (tool-call match + LLM-as-judge for tone and correctness), run on every prompt change.
- **Catalog search is keyword-based.** "Something for a kid starting out" relies on the model picking a category and price range. With a larger catalog I would add embedding search over descriptions and specs.
- **Installments and shipping are explained, not calculated.** The model divides prices by itself. A small `simulate_installments(price)` tool would remove arithmetic errors, and a shipping quote needs a carrier API.
- **Opening hours aren't enforced.** The manual says the bot should tell customers when the team is back if they write outside business hours; the date is in the prompt, but there is no explicit rule for it.
- **Identity check is minimal.** Knowing an e-mail or phone is enough to see an order. In production I would use a one-time code sent to that contact.
- **Single-user CLI, in-memory state.** A real deployment would be a WhatsApp webhook (FastAPI) with per-customer sessions in Redis, a read-only database instead of CSVs, and handoffs created in the helpdesk tool.
- **Prompt injection.** The prompt tells the agent to ignore rule changes and the tools are read-only (except handoff), which limits the damage, but there is no dedicated guardrail model.

## Use of AI coding assistants

I used **Claude Code** (Anthropic's CLI agent, model Claude Opus) as a pair programmer throughout the project. My workflow:

1. **Reading the brief together.** I gave it the challenge PDF, the e-mail and the data, and asked for the simplest viable design. It read the CSVs and the policy manual and pointed out the inconsistencies listed above, which I reviewed and decided on.
2. **Design decisions were mine to approve.** I chose the provider (Gemini free tier, so anyone can run it) and the priority on simplicity. Claude proposed function calling over RAG for the reasons above, and I agreed.
3. **Implementation in small, testable steps,** one commit each: data layer + tests → tools → prompt + CLI → README → examples. The data layer was tested before any LLM code was written.
4. **Real conversations as validation.** The examples in `examples/` are actual runs of the CLI, not hand-written.

Commits co-authored by the assistant are marked with a `Co-Authored-By` trailer.
