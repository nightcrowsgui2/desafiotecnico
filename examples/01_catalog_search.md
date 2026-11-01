# Catalog search

> **Scenario:** Customer asks for violões up to R$ 1,000 and then for a model that is sold out. The agent searches by category and price, shows table + PIX prices, flags the sold-out and discontinued items, and suggests similar available alternatives.
>
> Real run of `python -m agent` on 31/10/2026. Tool calls and their raw results are in the collapsible blocks.

Modelo: `gemini-3.5-flash-lite`

**Cliente:** Oi! Quais opções de violões disponíveis custando até R$1000?

<details><summary>Ferramentas consultadas</summary>

`search_products(category='Violões', max_price=1000)`

```json
{
  "total_encontrado": 14,
  "produtos": [
    {
      "id": 83,
      "nome": "Tagima Memphis AC-39 Nylon Natural",
      "categoria": "Violões",
      "descricao": "Violão clássico com cordas de nylon, perfeito para quem está começando. Corpo leve e confortável para longas sessões de estudo.",
      "especificacoes": {
        "top": "Linden",
        "back_sides": "Linden",
        "neck": "Nato",
        "strings": "nylon",
        "scale": "650mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 429.9,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 15,
      "preco_no_pix": 408.4
    },
    {
      "id": 85,
      "nome": "Rozini RC-104 Nylon Estudante",
      "categoria": "Violões",
      "descricao": "Violão clássico de estudo da Rozini, feito com madeiras nacionais. Acabamento caprichado e preço acessível para iniciantes.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Sapele",
        "neck": "Nato",
        "strings": "nylon",
        "scale": "650mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 459.9,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 10,
      "preco_no_pix": 436.9
    },
    {
      "id": 89,
      "nome": "Shelby SN-100 Folk Aço Preto",
      "categoria": "Violões",
      "descricao": "Violão folk aço com visual moderno em preto. Indicado para quem busca um instrumento versátil com boa relação custo-benefício.",
      "especificacoes": {
        "top": "Linden",
        "back_sides": "Linden",
        "neck": "Nato",
        "strings": "steel",
        "scale": "648mm",
        "electronics": "no",
        "color": "Preto"
      },
      "preco_tabela": 549.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 5,
      "preco_no_pix": 521.55
    },
    {
      "id": 88,
      "nome": "Giannini GF-1R Aço Folk Sunburst",
      "categoria": "Violões",
      "descricao": "Violão folk com tampo em Spruce e acabamento Sunburst clássico. Som equilibrado e visual elegante para palco e estúdio.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Sapele",
        "neck": "Nato",
        "strings": "steel",
        "scale": "648mm",
        "electronics": "no",
        "color": "Sunburst"
      },
      "preco_tabela": 579.9,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 7,
      "preco_no_pix": 550.9
    },
    {
      "id": 81,
      "nome": "Yamaha C40 Nylon Natural",
      "categoria": "Violões",
      "descricao": "Violão clássico com tampo em Spruce e fundo/laterais em Meranti. Ideal para estudantes e iniciantes, com excelente projeção sonora.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Meranti",
        "neck": "Nato",
        "strings": "nylon",
        "scale": "650mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 599.9,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 12,
      "preco_no_pix": 569.9
    },
    {
      "id": 84,
      "nome": "Giannini GN-15 Nylon Cedr Natural",
      "categoria": "Violões",
      "descricao": "Violão clássico Giannini com tampo em cedro. Sonoridade quente e encorpada, excelente custo-benefício para estudantes avançados.",
      "especificacoes": {
        "top": "Cedro",
        "back_sides": "Sapele",
        "neck": "Cedro",
        "strings": "nylon",
        "scale": "650mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 689.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 6,
      "preco_no_pix": 654.55
    },
    {
      "id": 87,
      "nome": "Yamaha F310 Aço Natural",
      "categoria": "Violões",
      "descricao": "Violão folk aço Yamaha com corpo robusto e timbre encorpado. Um dos modelos mais vendidos do mundo para iniciantes e intermediários.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Meranti",
        "neck": "Nato",
        "strings": "steel",
        "scale": "634mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 699.9,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 14,
      "preco_no_pix": 664.9
    },
    {
      "id": 86,
      "nome": "Tagima Dallas Tuner Aço Natural",
      "categoria": "Violões",
      "descricao": "Violão folk com cordas de aço e afinador integrado. Corpo confortável e som brilhante, ideal para acompanhamento vocal.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Sapele",
        "neck": "Nato",
        "strings": "steel",
        "scale": "648mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 749.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 9,
      "preco_no_pix": 711.55
    },
    {
      "id": 113,
      "nome": "Shelby SN-7C 7 Cordas Nylon Natural",
      "categoria": "Violões",
      "descricao": "Violão 7 cordas clássico com acabamento natural e braço em cedro. Boa opção para estudantes de choro que buscam qualidade acessível.",
      "especificacoes": {
        "top": "Linden",
        "back_sides": "Linden",
        "neck": "Cedro",
        "strings": "nylon",
        "scale": "650mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 749.0,
      "disponibilidade": "descontinuado (fora de linha)",
      "unidades_em_estoque": 0,
      "preco_no_pix": 711.55
    },
    {
      "id": 107,
      "nome": "Shelby SGD-195E Elétrico Aço Sunburst",
      "categoria": "Violões",
      "descricao": "Violão eletroacústico dreadnought com captação e afinador integrado. Boa opção de custo-benefício para quem precisa de amplificação.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Sapele",
        "neck": "Nato",
        "strings": "steel",
        "scale": "650mm",
        "electronics": "yes",
        "color": "Sunburst"
      },
      "preco_tabela": 799.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 6,
      "preco_no_pix": 759.05
    },
    {
      "id": 96,
      "nome": "Giannini GF-3D Dreadnought Sunburst",
      "categoria": "Violões",
      "descricao": "Violão dreadnought com corpo amplo e acabamento Sunburst. Volume alto e graves profundos, ideal para country e pop.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Sapele",
        "neck": "Nato",
        "strings": "steel",
        "scale": "650mm",
        "electronics": "no",
        "color": "Sunburst"
      },
      "preco_tabela": 799.9,
      "disponibilidade": "esgotado no momento",
      "unidades_em_estoque": 0,
      "preco_no_pix": 759.9
    },
    {
      "id": 82,
      "nome": "Yamaha C70 Nylon Natural",
      "categoria": "Violões",
      "descricao": "Violão clássico de nível intermediário com tampo em Spruce sólido. Acabamento de alta qualidade e timbre equilibrado.",
      "especificacoes": {
        "top": "Spruce Sólido",
        "back_sides": "Nato",
        "neck": "Nato",
        "strings": "nylon",
        "scale": "650mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 849.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 8,
      "preco_no_pix": 806.55
    },
    {
      "id": 91,
      "nome": "Tagima Woodstock Dreadnought Natural",
      "categoria": "Violões",
      "descricao": "Violão dreadnought com corpo amplo e som potente. Excelente para fingerpicking e strumming com projeção impressionante.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Sapele",
        "neck": "Nato",
        "strings": "steel",
        "scale": "650mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 899.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 11,
      "preco_no_pix": 854.05
    },
    {
      "id": 112,
      "nome": "Tagima TW-7 7 Cordas Aço Natural",
      "categoria": "Violões",
      "descricao": "Violão 7 cordas com cordas de aço para estilos que exigem projeção extra. Braço confortável com tensor regulável.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Sapele",
        "neck": "Nato",
        "strings": "steel",
        "scale": "650mm",
        "electronics": "no",
        "color": "Natural"
      },
      "preco_tabela": 999.0,
      "disponibilidade": "disponível",
      "unidades_em_estoque": 6,
      "preco_no_pix": 949.05
    }
  ]
}
```

</details>

**Lia:** Temos várias opções legais de violões até R$ 1.000! Vou te mostrar alguns destaques disponíveis:

*   **Tagima Memphis AC-39 Nylon Natural** (nylon) — R$ 429,90 (ou R$ 408,40 no PIX)
*   **Yamaha C40 Nylon Natural** (nylon) — R$ 599,90 (ou R$ 569,90 no PIX)
*   **Yamaha F310 Aço Natural** (aço) — R$ 699,90 (ou R$ 664,90 no PIX)
*   **Tagima Dallas Tuner Aço Natural** (aço) — R$ 749,00 (ou R$ 711,55 no PIX)
*   **Tagima Woodstock Dreadnought Natural** (aço) — R$ 899,00 (ou R$ 854,05 no PIX)

*Nota: Temos também o **Giannini GF-3D Dreadnought Sunburst** por R$ 799,90, mas ele está esgotado no momento, assim como o modelo de 7 cordas da Shelby que saiu de linha.*

Você prefere violão com cordas de nylon ou de aço? 🎸

**Cliente:** O Giannini GF-3D tem? Gostei dele

<details><summary>Ferramentas consultadas</summary>

`search_products(query='GF-3D')`

```json
{
  "total_encontrado": 1,
  "produtos": [
    {
      "id": 96,
      "nome": "Giannini GF-3D Dreadnought Sunburst",
      "categoria": "Violões",
      "descricao": "Violão dreadnought com corpo amplo e acabamento Sunburst. Volume alto e graves profundos, ideal para country e pop.",
      "especificacoes": {
        "top": "Spruce",
        "back_sides": "Sapele",
        "neck": "Nato",
        "strings": "steel",
        "scale": "650mm",
        "electronics": "no",
        "color": "Sunburst"
      },
      "preco_tabela": 799.9,
      "disponibilidade": "esgotado no momento",
      "unidades_em_estoque": 0,
      "preco_no_pix": 759.9
    }
  ]
}
```

</details>

**Lia:** Poxa, o **Giannini GF-3D Dreadnought Sunburst** (R$ 799,90 no preço de tabela ou R$ 759,90 no PIX) está esgotado no momento, infelizmente. 

Mas se você curtiu o estilo dele (violão folk/dreadnought com cordas de aço e um timbre com graves profundos), posso te sugerir o **Tagima Woodstock Dreadnought Natural** por R$ 899,00 (ou R$ 854,05 no PIX) ou o **Shelby SGD-195E Elétrico Aço Sunburst** por R$ 799,00 (ou R$ 759,05 no PIX), que também tem acabamento Sunburst! 

Quer dar uma olhada neles?

**Cliente:** Beleza, vou pensar. Valeu!

**Lia:** Imagina! Qualquer coisa é só chamar. Boa escolha e boa música para você! 🎵
