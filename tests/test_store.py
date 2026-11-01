from agent import store


def test_search_by_name_is_accent_and_spacing_insensitive():
    for query in ["Takamine GD20", "takamine gd 20", "TAKAMINE GD-20"]:
        result = store.search_products(query=query)
        assert [p["nome"] for p in result["produtos"]] == ["Takamine GD20 Dreadnought Natural"]


def test_search_by_category_and_price_is_sorted_and_bounded():
    result = store.search_products(category="violoes", max_price=1000)
    prices = [p["preco_tabela"] for p in result["produtos"]]
    assert prices == sorted(prices)
    assert all(p <= 1000 for p in prices)
    assert all(p["categoria"] == "Violões" for p in result["produtos"])


def test_active_promotion_replaces_pix_discount():
    product = store.search_products(query="Ohana CK-20")["produtos"][0]
    assert product["promocao_ativa"]["desconto_percentual"] == 20
    assert product["promocao_ativa"]["preco_promocional"] == 439.2
    assert "preco_no_pix" not in product


def test_inactive_promotion_is_ignored_and_pix_price_is_offered():
    product = store.search_products(query="Takamine GD20")["produtos"][0]
    assert "promocao_ativa" not in product
    assert product["preco_no_pix"] == round(2199 * 0.95, 2)


def test_stock_states():
    assert store.search_products(query="Giannini GF-3D")["produtos"][0]["disponibilidade"] == "esgotado no momento"
    assert "descontinuado" in store.search_products(query="Shelby SN-7C")["produtos"][0]["disponibilidade"]
    assert "em breve" in store.search_products(query="KA-ABP-CTG")["produtos"][0]["disponibilidade"]


def test_order_requires_matching_contact():
    assert "erro" in store.get_order(8, "someone@else.com")
    assert "erro" in store.get_order(999, "x")


def test_order_lookup_by_email_or_phone():
    by_email = store.get_order(8, "AnaCarol.Ferreira@coldmail.com")
    by_phone = store.get_order(8, "67 99654-7821")
    assert by_email == by_phone
    assert by_email["status"] == "enviado (a caminho)"
    assert by_email["codigo_rastreamento"] == "BRJL5544332BR"
    assert by_email["forma_de_pagamento"] == "cartão de débito"


def test_delivered_order_exposes_days_since_delivery():
    order = store.get_order(4, "lucas.mendes@jmail.com")
    assert order["dias_desde_a_entrega"] > 0
    assert order["forma_de_pagamento"] == "boleto bancário"


def test_policies_are_split_by_topic():
    assert "horario" in store.policy_topics()
    assert "09:00 às 13:00" in store.get_policy("horario")
    assert "Tópico desconhecido" in store.get_policy("nope")


def test_tool_docstrings_list_every_valid_option():
    # The valid values live in the docstrings (the SDK cannot convert Literal args), so keep them in sync.
    from agent import tools
    assert all(c in tools.search_products.__doc__ for c in store.category_names())
    assert all(t in tools.get_store_policy.__doc__ for t in store.policy_topics())


def test_unknown_category_lists_the_valid_ones():
    assert "Violões" in store.search_products(category="Pianos de cauda")["dica"]


def test_search_with_no_match_explains_how_to_search_by_type():
    result = store.search_products(query="violão")
    assert result["total_encontrado"] == 0
    assert "category" in result["dica"]


def test_tools_accept_arguments_the_way_the_gemini_sdk_passes_them():
    # The SDK converts the model's JSON args using the type hints before calling the tool;
    # an Optional[Literal] hint used to break here even though direct calls worked.
    from google.genai._extra_utils import invoke_function_from_dict_args
    from agent import tools
    result = invoke_function_from_dict_args({"category": "Violões", "max_price": 1000}, tools.search_products)
    assert result["total_encontrado"] > 0
    assert invoke_function_from_dict_args({"topic": "horario"}, tools.get_store_policy)


def test_installments_respect_minimum_per_tier():
    # R$ 439,20: 6x would be R$ 73,20, below the R$ 80 minimum for 4x-6x
    options = store.installment_options(439.2)
    assert [o["parcelas"] for o in options["opcoes_sem_juros"]] == [2, 3, 4, 5]
    assert options["maximo_de_parcelas"] == 5
    assert store.installment_options(2199)["maximo_de_parcelas"] == 12
    assert store.installment_options(90)["opcoes_sem_juros"] == []
