# Return request (policy + order data)

> **Scenario:** Non-trivial case: "I regret my purchase, can I return it?". The agent asks for the order number and the e-mail before looking it up (LGPD), compares the delivery date with the 7-day withdrawal period, explains why the return is no longer possible, and covers the defect / warranty follow-up.
>
> Real run of `python -m agent` on 31/10/2026. Tool calls and their raw results are in the collapsible blocks.

Modelo: `gemini-3.5-flash-lite`

**Cliente:** Me arrependi da minha compra, posso devolver meu pedido?

<details><summary>Ferramentas consultadas</summary>

`get_store_policy(topic='trocas_e_devolucoes')`

```text
A loja segue o Código de Defesa do Consumidor (Lei nº 8.078/90).

Direito de arrependimento (compras online):
- Devolução em até 7 (sete) dias corridos **após o recebimento** do produto, sem necessidade de justificativa.
- Produto na embalagem original, sem sinais de uso, com todos os acessórios e manuais.
- Reembolso na mesma forma de pagamento original em até 10 dias úteis.
- Frete de devolução por conta da loja em caso de arrependimento.

Trocas por defeito:
- Produtos com defeito de fabricação podem ser trocados em até 30 (trinta) dias corridos **após a compra**.
- Após os 30 dias, o cliente deve acionar a garantia diretamente com o fabricante; a loja pode intermediar o processo mediante solicitação.
- Danos por mau uso, quedas, umidade excessiva ou modificações não autorizadas não são cobertos.

Trocas por preferência (cor, modelo, tamanho):
- Permitidas em até 7 dias, mediante disponibilidade do produto desejado.
- Produto em perfeito estado e na embalagem original.
- Diferenças de valor são cobradas ou reembolsadas conforme o caso.

Itens não elegíveis para troca:
- Instrumentos com personalização ou ajustes sob encomenda (setup, regulagem especial).
- Produtos de liquidação com aviso explícito de "venda final".
- Boquilhas de instrumentos de sopro, por questões de higiene.
```

</details>

**Lia:** Pode sim! Para compras feitas pela internet, você tem até 7 dias corridos após o recebimento para solicitar a devolução por arrependimento, desde que o instrumento esteja na embalagem original, sem marcas de uso e com todos os acessórios.

Para eu conferir os prazos do seu pedido e te ajudar com o processo, por favor, me informe o **número do pedido** e o **e-mail ou telefone** cadastrado na compra. 🎸

**Cliente:** Pedido 4, meu e-mail é lucas.mendes@jmail.com

<details><summary>Ferramentas consultadas</summary>

`get_order_status(order_id=4, customer_contact='lucas.mendes@jmail.com')`

```json
{
  "pedido": 4,
  "cliente": "Lucas Mendes da Silva",
  "cidade": "Campo Grande",
  "data_do_pedido": "2025-12-10",
  "status": "entregue",
  "itens": [
    {
      "produto": "Giannini GF-3D Dreadnought Sunburst",
      "quantidade": 1
    }
  ],
  "valor_total": 799.9,
  "forma_de_pagamento": "boleto bancário",
  "dias_desde_o_pedido": 325,
  "codigo_rastreamento": "BRQM7890123BR",
  "previsao_de_entrega": "2025-12-22",
  "dias_desde_a_entrega": 313
}
```

</details>

**Lia:** Lucas, vi aqui que o seu pedido foi entregue há algum tempo (em dezembro de 2025). Como o prazo de 7 dias corridos após o recebimento para arrependimento já passou, infelizmente não consigo realizar a devolução automática por aqui. 

Caso tenha ocorrido algum problema com o instrumento ou precise de outra orientação, posso te encaminhar para a nossa equipe humana analisar o seu caso, tudo bem? 🎸

**Cliente:** Poxa. E se ele estiver com defeito?

<details><summary>Ferramentas consultadas</summary>

`get_store_policy(topic='garantia')`

```text
- Garantia legal (CDC): 90 (noventa) dias contra defeitos de fabricação, contados a partir do recebimento.
- Garantia do fabricante: varia de 6 meses a 2 anos, conforme o certificado que acompanha cada produto.

Não coberto pela garantia:
- Desgaste natural de peças (trastes, cordas, feltros, palhetas de sopro).
- Danos por mau uso, queda ou exposição a condições climáticas extremas.
- Modificações ou reparos feitos por terceiros não autorizados.
- Danos estéticos que não afetem a funcionalidade do instrumento.
```

</details>

**Lia:** Se for um defeito de fabricação, a garantia legal é de 90 dias após o recebimento, e muitos fabricantes oferecem garantias adicionais. Como já passou esse período para o seu pedido, a garantia de fábrica pode ter expirado ou exigiria contato direto com o fabricante.

Quer que eu encaminhe o seu caso para a nossa equipe humana avaliar se ainda podemos te ajudar de alguma forma? 🎸
