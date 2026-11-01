# Store information

> **Scenario:** Address, Sunday opening and payment methods. The agent answers only from the policy manual (`get_store_policy`), not from its own knowledge.
>
> Real run of `python -m agent` on 31/10/2026. Tool calls and their raw results are in the collapsible blocks.

Modelo: `gemini-3.5-flash-lite`

**Cliente:** Qual o endereço da loja?

<details><summary>Ferramentas consultadas</summary>

`get_store_policy(topic='sobre_a_loja')`

```text
A Empório da Música é uma loja especializada em instrumentos musicais, fundada em 2008 em Campo Grande, Mato Grosso do Sul. Com mais de 15 anos de atuação, é referência regional na venda de instrumentos para músicos iniciantes, intermediários e profissionais.

O catálogo abrange instrumentos de marcas nacionais e internacionais: guitarras, baixos, violões, baterias, teclados, instrumentos de sopro, cordas orquestrais e ukuleles.
A loja trabalha **exclusivamente com instrumentos musicais** — não comercializa acessórios como cordas, palhetas, cabos, cases, pedais ou amplificadores.

Missão: democratizar o acesso a instrumentos musicais de qualidade na região Centro-Oeste, oferecendo atendimento especializado e preços competitivos.

Dados da empresa:
- Razão social: Empório da Música Instrumentos Musicais Ltda.
- CNPJ: 12.345.678/0001-90
- Endereço: Rua 14 de Maio, 3200 — Centro, Campo Grande - MS, CEP 79202-333
- Telefone / WhatsApp: (67) 3341-4444
- E-mail: contato@emporiodamusica.com.br
- Fundação: 2008

> Nota de curadoria: o manual cita também o número (67) 3321-4500 na seção de WhatsApp e grafa o e-mail como "empóriodamusica" em um trecho. Adotamos (67) 3341-4444 e contato@emporiodamusica.com.br, que aparecem na capa e na tabela de dados oficiais da empresa.
```

</details>

**Lia:** Ficamos na Rua 14 de Maio, 3200 — Centro, aqui em Campo Grande (MS). 🎸

**Cliente:** Vocês abrem domingo? E quais formas de pagamento aceitam?

<details><summary>Ferramentas consultadas</summary>

`get_store_policy(topic='horario')`

```text
Atendimento presencial e via WhatsApp:
- Segunda a sexta-feira: 09:00 às 18:00
- Sábado: 09:00 às 13:00
- Domingo e feriados: fechado

O WhatsApp segue o mesmo horário, com respostas automáticas fora do expediente.
Em datas especiais (Black Friday, Aniversário da Loja, Natal) o horário pode ser estendido; alterações são comunicadas com antecedência nas redes sociais e no WhatsApp.
```

`get_store_policy(topic='pagamento')`

```text
Formas aceitas (compras presenciais e online):
- PIX: à vista, **5% de desconto** sobre o preço de tabela.
- Cartão de débito: à vista, todas as bandeiras.
- Cartão de crédito: até 12x sem juros.
- Boleto bancário: à vista, compensação em até 3 dias úteis.

Regras de parcelamento no cartão de crédito:
- Até 3x: sem juros, sem valor mínimo de parcela (exceto parcelas abaixo de R$ 50,00).
- De 4x a 6x: sem juros, parcela mínima de R$ 80,00.
- De 7x a 12x: sem juros, parcela mínima de R$ 100,00.
- Combinação de formas de pagamento (ex.: PIX + cartão) é permitida para compras acima de R$ 2.000,00.

> Nota de curadoria: a tabela geral do manual diz "parcela mínima de R$ 100,00" para o crédito, mas a seção 3.1 detalha faixas. Seguimos as faixas da seção 3.1, por serem mais específicas. Em até 3x, interpretamos que a parcela não pode ser inferior a R$ 50,00.
```

</details>

**Lia:** Aos domingos nós ficamos fechados, mas abrimos de segunda a sexta das 9h às 18h e aos sábados das 9h às 13h! 

Sobre o pagamento, aceitamos:
- **PIX** (com 5% de desconto);
- **Cartão de crédito** (em até 12x sem juros, respeitando o valor mínimo por parcela);
- **Cartão de débito** à vista;
- **Boleto bancário** à vista. 

Posso te ajudar a encontrar algum instrumento?
