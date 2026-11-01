"""Read-only access to the store's data: catalog, promotions, orders and policies.

These are plain Python functions so they can be unit-tested without an LLM.
`tools.py` exposes a subset of them to the model.
"""

import json
import re
import unicodedata
from datetime import date
from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
POLICIES_FILE = ROOT / "knowledge" / "policies.md"

PIX_DISCOUNT = 0.05

STOCK_STATUS = {
    "active": "disponível",
    "discontinued": "descontinuado (fora de linha)",
    "coming_soon": "em breve (ainda não disponível para venda)",
}

# The data dictionary does not define the order statuses; meanings below are our reading
# of the data (e.g. a cancelled order notes "payment not confirmed in time").
ORDER_STATUS = {
    "pending": "aguardando confirmação do pagamento",
    "confirmed": "pagamento confirmado, em separação (ainda não enviado)",
    "shipped": "enviado (a caminho)",
    "delivered": "entregue",
    "cancelled": "cancelado",
}

PAYMENT_METHODS = {
    "pix": "PIX",
    "debit": "cartão de débito",
    "boleto": "boleto bancário",
}


def normalize(text: str) -> str:
    """Lowercase, strip accents and collapse non-alphanumerics, for forgiving matching."""
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


@lru_cache
def _tables() -> dict[str, pd.DataFrame]:
    t = {name: pd.read_csv(DATA_DIR / f"{name}.csv") for name in
         ["products", "categories", "promotions", "orders", "order_items", "customers"]}
    products = t["products"].merge(
        t["categories"][["category_id", "name"]].rename(columns={"name": "category"}),
        on="category_id", how="left",
    )
    products["search_key"] = products["name"].map(normalize)
    t["products"] = products
    t["promotions"] = t["promotions"][t["promotions"]["is_active"] == 1]
    return t


def category_names() -> list[str]:
    return _tables()["categories"]["name"].tolist()


def _format_product(row: pd.Series) -> dict:
    price = float(row["price_brl"])
    promos = _tables()["promotions"]
    promo = promos[promos["product_id"] == row["product_id"]]

    stock = int(row["stock_quantity"])
    availability = STOCK_STATUS.get(row["status"], row["status"])
    if row["status"] == "active" and stock == 0:
        availability = "esgotado no momento"

    item = {
        "id": int(row["product_id"]),
        "nome": row["name"],
        "categoria": row["category"],
        "descricao": row["description"],
        "especificacoes": json.loads(row["specs"]),
        "preco_tabela": price,
        "disponibilidade": availability,
        "unidades_em_estoque": stock,
    }
    if not promo.empty:
        # If a product ever had two active promotions we apply the best one: they are not cumulative.
        best = promo.sort_values("discount_percent", ascending=False).iloc[0]
        discount = int(best["discount_percent"])
        item["promocao_ativa"] = {
            "nome": best["description"],
            "desconto_percentual": discount,
            "preco_promocional": round(price * (1 - discount / 100), 2),
            "observacao": "desconto de PIX não se aplica sobre preço promocional",
        }
    else:
        item["preco_no_pix"] = round(price * (1 - PIX_DISCOUNT), 2)
    return item


def search_products(query: str = "", category: str = "", min_price: float = 0,
                    max_price: float = 0, limit: int = 15) -> dict:
    products = _tables()["products"]
    if category:
        wanted = normalize(category)
        products = products[products["category"].map(normalize).str.contains(wanted)]
        if products.empty:
            return {"total_encontrado": 0,
                    "dica": f"Categoria desconhecida. Use uma destas: {', '.join(category_names())}."}
    if query:
        for token in normalize(query).split():
            # "gd20" should also match "gd 20" and vice-versa
            products = products[products["search_key"].str.replace(" ", "").str.contains(token)]
    if min_price:
        products = products[products["price_brl"] >= min_price]
    if max_price:
        products = products[products["price_brl"] <= max_price]

    products = products.sort_values("price_brl")
    if products.empty and query:
        return {"total_encontrado": 0,
                "dica": "Nenhum produto com esse nome. Para buscar por tipo de instrumento "
                        "(violão, guitarra...), use o parâmetro category e deixe query vazio."}
    return {
        "total_encontrado": len(products),
        "produtos": [_format_product(r) for _, r in products.head(limit).iterrows()],
    }


def get_order(order_id: int, contact: str) -> dict:
    t = _tables()
    order = t["orders"][t["orders"]["order_id"] == order_id]
    if order.empty:
        return {"erro": f"Pedido {order_id} não encontrado."}
    order = order.iloc[0]
    customer = t["customers"][t["customers"]["customer_id"] == order["customer_id"]].iloc[0]

    # LGPD: only reveal order details to someone who knows the e-mail or phone on file.
    given_email = contact.strip().lower()
    given_phone = re.sub(r"\D", "", contact)
    phone_on_file = re.sub(r"\D", "", customer["phone"])
    phone_ok = len(given_phone) >= 8 and phone_on_file.endswith(given_phone)
    if given_email != customer["email"].lower() and not phone_ok:
        return {"erro": "O e-mail ou telefone informado não confere com o cadastro deste pedido."}

    items = t["order_items"][t["order_items"]["order_id"] == order_id].merge(
        t["products"][["product_id", "name"]], on="product_id")
    payment = order["payment_method"]
    if payment.startswith("credit_"):
        payment = f"cartão de crédito em {payment.removeprefix('credit_')}"

    result = {
        "pedido": int(order["order_id"]),
        "cliente": customer["name"],
        "cidade": customer["city"],
        "data_do_pedido": order["order_date"],
        "status": ORDER_STATUS.get(order["status"], order["status"]),
        "itens": [{"produto": r["name"], "quantidade": int(r["quantity"])} for _, r in items.iterrows()],
        "valor_total": float(order["total_brl"]),
        "forma_de_pagamento": PAYMENT_METHODS.get(payment, payment),
        "dias_desde_o_pedido": (date.today() - date.fromisoformat(order["order_date"])).days,
    }
    if pd.notna(order["tracking_code"]):
        result["codigo_rastreamento"] = order["tracking_code"]
    if pd.notna(order["estimated_delivery"]):
        result["previsao_de_entrega"] = order["estimated_delivery"]
        if order["status"] == "delivered":
            # We only have the estimated date; we assume delivery happened on it.
            delivered = date.fromisoformat(order["estimated_delivery"])
            result["dias_desde_a_entrega"] = (date.today() - delivered).days
    if pd.notna(order["notes"]):
        result["observacoes"] = order["notes"]
    return result


@lru_cache
def _policy_sections() -> dict[str, str]:
    text = POLICIES_FILE.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    sections = re.split(r"^## (\w+)\s*$", text, flags=re.M)[1:]
    return {key: body.strip() for key, body in zip(sections[::2], sections[1::2])}


def policy_topics() -> list[str]:
    return list(_policy_sections())


def get_policy(topic: str) -> str:
    sections = _policy_sections()
    if topic not in sections:
        return f"Tópico desconhecido. Tópicos disponíveis: {', '.join(sections)}."
    return sections[topic]
