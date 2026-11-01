"""Functions the LLM can call. Gemini builds each tool schema from the signature and docstring."""

import functools
import json
from datetime import datetime

from agent import store

HANDOFF_FILE = store.ROOT / "handoffs" / "handoffs.jsonl"

# Every tool call of the current turn, so the CLI can show and save what the agent looked up.
call_log: list[dict] = []


def _logged(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
        except Exception as e:
            call_log.append({"tool": fn.__name__, "args": kwargs, "result": f"ERRO: {e!r}"})
            raise
        call_log.append({"tool": fn.__name__, "args": kwargs, "result": result})
        return result
    return wrapper


@_logged
def search_products(query: str = "", category: str = "",
                    min_price: float = 0, max_price: float = 0) -> dict:
    """Search the store catalog. Always use this before stating any price, stock or promotion.

    Args:
        query: Words that appear in the product NAME: brand, model or finish
            (e.g. "Takamine GD20", "Yamaha", "Sunburst"). Product names do not contain the
            instrument type, so leave it empty when the customer asks for a type.
        category: The instrument type. Use it whenever the customer mentions a kind of
            instrument. One of: Guitarras, Baixos, Baterias e Percussão, Teclados e Pianos,
            Violões, Instrumentos de Sopro (Madeiras), Instrumentos de Sopro (Metais),
            Cordas Orquestrais, Ukuleles. Leave empty for any category.
        min_price: Minimum table price in BRL (0 = no minimum).
        max_price: Maximum table price in BRL (0 = no maximum).

    Returns up to 15 products sorted by price, with table price, PIX price or active promotion,
    and availability. `total_encontrado` tells how many matched in total.
    """
    return store.search_products(query, category, min_price, max_price)


@_logged
def get_order_status(order_id: int, customer_contact: str) -> dict:
    """Look up an order. Ask the customer for BOTH the order number and the e-mail or phone
    used in the purchase before calling; never guess them.

    Args:
        order_id: The order number.
        customer_contact: E-mail or phone number registered in the order.
    """
    return store.get_order(order_id, customer_contact)


@_logged
def get_store_policy(topic: str) -> str:
    """Read the official store policy on a topic. Use it for any question about the store itself:
    address and contacts (sobre_a_loja), opening hours, payment and installments, returns and
    exchanges, shipping, promotion rules, warranty, complaints, and personal data (privacidade).

    Args:
        topic: One of: sobre_a_loja, horario, pagamento, trocas_e_devolucoes, frete_e_entrega,
            promocoes, garantia, reclamacoes, privacidade.
    """
    return store.get_policy(topic)


@_logged
def handoff_to_human(reason: str, summary: str, customer_contact: str = "") -> str:
    """Forward the conversation to the human team. Use it for complaints, return/exchange requests
    the customer wants to start, or anything you cannot resolve with the other tools.

    Args:
        reason: Short category, e.g. "reclamação", "solicitação de devolução", "dúvida sem resposta".
        summary: One or two sentences with what the customer needs, in Portuguese.
        customer_contact: Customer name, e-mail or phone, if they provided it.
    """
    HANDOFF_FILE.parent.mkdir(exist_ok=True)
    ticket = {"created_at": datetime.now().isoformat(timespec="seconds"), "reason": reason,
              "summary": summary, "customer_contact": customer_contact}
    with HANDOFF_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ticket, ensure_ascii=False) + "\n")
    return "Encaminhado à equipe. Prazo de retorno: até 24 horas úteis."


ALL_TOOLS = [search_products, get_order_status, get_store_policy, handoff_to_human]
