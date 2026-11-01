# Active promotion, installments and an expired campaign

> **Scenario:** Non-trivial case: the agent shows original price, discount % and promotional price; refuses to stack the PIX discount on a promotional price; computes the allowed installments (5x, because 6x would fall below the R$ 80 minimum); and states that a Black Friday promotion is not active instead of promising it.
>
> Real run of `python -m agent` on 31/10/2026. Tool calls and their raw results are in the collapsible blocks.

Modelo: `gemini-3.5-flash-lite`

**Cliente:** Quanto custa o ukulele Ohana CK-20? Se eu pagar no pix tem desconto?

<details><summary>Ferramentas consultadas</summary>

`search_products(query='Ohana CK-20', category='Ukuleles')`

```json
{
  "total_encontrado": 1,
  "produtos": [
    {
      "id": 121,
      "nome": "Ohana CK-20 Concert Natural",
      "categoria": "Ukuleles",
      "descricao": "Ukulele concert Ohana com tampo sólido em Spruce e fundo em Mogno. Tom equilibrado e sustain impressionante para a categoria.",
      "especificacoes": {
        "top": "Spruce Sólido",
        "back_sides": "Mogno",
        "neck": "Mogno",
        "strings": "nylon",
        "scale": "381mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 549.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 6,
      "promocao_ativa": {
        "nome": "Desconto Exclusivo",
        "desconto_percentual": 20,
        "preco_promocional": 439.2,
        "observacao": "desconto de PIX não se aplica sobre preço promocional"
      }
    }
  ]
}
```

</details>

**Lia:** O ukulele Ohana CK-20 (modelo Concert Natural) está com um super desconto! 

O preço de tabela dele é R$ 549,00, mas está com 20% de desconto na promoção "Desconto Exclusivo", saindo por **R$ 439,20**. 

Como ele já está com preço promocional, o desconto adicional de PIX não se acumula, ok? 

Quer conferir as opções de parcelamento ou ver mais detalhes dele? 🎶

**Cliente:** E dá pra parcelar em 6x no cartão?

<details><summary>Ferramentas consultadas</summary>

`get_installment_options(price=439.2)`

```json
{
  "valor": 439.2,
  "opcoes_sem_juros": [
    {
      "parcelas": 2,
      "valor_parcela": 219.6
    },
    {
      "parcelas": 3,
      "valor_parcela": 146.4
    },
    {
      "parcelas": 4,
      "valor_parcela": 109.8
    },
    {
      "parcelas": 5,
      "valor_parcela": 87.84
    }
  ],
  "maximo_de_parcelas": 5,
  "regra": "até 3x: parcela mínima R$ 50; 4x a 6x: R$ 80; 7x a 12x: R$ 100"
}
```

</details>

**Lia:** Para o valor promocional de R$ 439,20, conseguimos parcelar **sem juros em até 5x** (já que a 6ª parcela ficaria abaixo do valor mínimo exigido de R$ 80,00). 

Nesse caso, ficaria em 5 parcelas de R$ 87,84 sem juros no cartão de crédito! 💳

**Cliente:** Vi que tinha Black Friday no Martin D-28, ainda está valendo?

<details><summary>Ferramentas consultadas</summary>

`search_products(query='Martin D-28', category='Violões')`

```json
{
  "total_encontrado": 2,
  "produtos": [
    {
      "id": 93,
      "nome": "Martin D-28 Dreadnought Natural",
      "categoria": "Violões",
      "descricao": "Lendário violão Martin D-28 com tampo sólido em Sitka Spruce e fundo em Rosewood. Referência mundial em sonoridade e construção.",
      "especificacoes": {
        "top": "Sitka Spruce Sólido",
        "back_sides": "East Indian Rosewood",
        "neck": "Select Hardwood",
        "strings": "steel",
        "scale": "645mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 11499.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 2,
      "preco_no_pix": 10924.05
    },
    {
      "id": 108,
      "nome": "Martin D-28E Elétrico Aço Natural",
      "categoria": "Violões",
      "descricao": "O lendário Martin D-28 com captação LR Baggs Anthem. Todo o timbre clássico do D-28 com amplificação de nível profissional.",
      "especificacoes": {
        "top": "Sitka Spruce Sólido",
        "back_sides": "East Indian Rosewood",
        "neck": "Select Hardwood",
        "strings": "steel",
        "scale": "645mm",
        "electronics": "yes",
        "color": "Natural"
      },
      "preco_tabela": 12000.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 1,
      "preco_no_pix": 11400.0
    }
  ]
}
```

`get_store_policy(topic='promocoes')`

```text
Campanhas periódicas:
- Aniversário da Loja (agosto): 10% a 25% em itens selecionados.
- Black Friday (novembro): 15% a 30% em todo o catálogo.
- Volta às Aulas (fevereiro): descontos especiais em instrumentos para estudantes.
- Queima de Estoque: promoções pontuais para renovação de catálogo.
- Semana do Músico: na semana do Dia do Músico (22 de novembro).

Regras:
- Promoções **não são cumulativas**. O desconto de 5% no PIX **não se aplica** sobre preços já promocionais.
- Promoções estão sujeitas a estoque; produtos esgotados durante a promoção não geram direito a reserva de preço (rain check).
- Preços promocionais devem ser apresentados junto do preço original e do percentual de desconto.
- Se a promoção perguntada não estiver ativa no sistema, informar com transparência e apresentar o preço atual. Nunca prometer desconto que não está vigente.
```

</details>

**Lia:** Os violões Martin D-28 (tanto o modelo acústico quanto o elétrico) estão com ótimos preços em nossa loja, mas a campanha de Black Friday acontece apenas em novembro e no momento não há nenhuma promoção ativa para eles, viu? 

O **Martin D-28 Dreadnought Natural** está por R$ 11.499,00 na tabela, ou R$ 10.924,05 à vista no PIX (com 5% de desconto). 

Já o **Martin D-28E Elétrico Aço Natural** custa R$ 12.000,00 na tabela, ou R$ 11.400,00 à vista no PIX. 

Quer que eu confira as opções de parcelamento para um deles? 🎸
