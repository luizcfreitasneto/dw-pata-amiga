# dw-pata-amiga
Data Warehouse Pata Amiga - PostgreSQL, ETL, modelagem dimensional e analises SQL

# Data Warehouse Pata Amiga

## 1. Apresentação do projeto

Este projeto foi desenvolvido como parte do Mini-Projeto Avaliativo do Módulo 2 da formação em Análise de Dados do SC TEC.

O estudo de caso utiliza dados de uma rede fictícia de pet shops, denominada Pata Amiga, com unidades em diferentes municípios de Santa Catarina.

O objetivo é construir um Data Warehouse utilizando PostgreSQL, aplicando técnicas de ETL, tratamento de dados, modelagem dimensional e consultas SQL para apoiar a tomada de decisões de negócio.

## 2. Objetivos

- Organizar e integrar dados de pedidos, lojas e praças de atendimento.
- Identificar e tratar inconsistências presentes nos dados de origem.
- Construir um modelo dimensional para análise dos pedidos.
- Implementar dimensões e tabela fato no PostgreSQL.
- Analisar indicadores de faturamento, logística, descontos, categorias e distribuição regional.
- Responder às cinco perguntas de negócio propostas no estudo de caso.
- Identificar limitações dos dados e apresentar recomendações fundamentadas nos resultados.

## 3. Tecnologias utilizadas

- **PostgreSQL 18:** armazenamento e processamento dos dados.
- **pgAdmin 4:** execução e validação dos scripts SQL.
- **SQL:** transformação, integração, modelagem e análise dos dados.
- **Visual Studio Code:** organização dos arquivos e documentação.
- **Git e GitHub:** versionamento e publicação do projeto.
- **Markdown:** elaboração da documentação técnica.

## 4. Diagnóstico dos dados de origem

O projeto utiliza três arquivos CSV como fontes de dados:

- `stg_pedido.csv`: informações dos pedidos realizados pela rede.
- `stg_loja.csv`: informações cadastrais das lojas.
- `stg_loja_praca.csv`: relacionamento entre lojas e praças de atendimento.

### 4.1. Quantidade de registros

Após o processamento e a validação dos dados, foram identificados:

| Indicador | Quantidade |
|---|---:|
| Pedidos na origem | 4.044 |
| Pedidos carregados na tabela fato | 4.044 |
| Pedidos distintos | 4.044 |
| Lojas na dimensão, incluindo registro padrão | 33 |
| Categorias na dimensão | 38 |
| Registros na dimensão tempo, incluindo registro padrão | 236 |

A conferência confirmou que todos os 4.044 pedidos foram carregados na tabela fato, sem duplicidade de número de pedido.

### 4.2. Qualidade dos dados

Durante o tratamento dos dados, foram identificadas as seguintes limitações:

| Problema identificado | Pedidos afetados | Percentual |
|---|---:|---:|
| Loja não identificada | 3 | 0,07% |
| Data de entrega ausente | 1.953 | 48,29% |
| Quantidade de itens ausente | 257 | 6,36% |
| Valor líquido ausente | 121 | 2,99% |

Essas situações foram preservadas e tratadas de forma controlada durante o ETL.

A ausência da data de entrega não permite concluir, isoladamente, que o pedido sofreu atraso ou deixou de ser entregue.

### 4.3. Tratamentos realizados

O processo de ETL contemplou:

- Padronização de diferentes formatos de datas.
- Conversão de valores monetários para formatos numéricos.
- Normalização de nomes e identificadores de lojas.
- Padronização de categorias de produtos.
- Tratamento de valores ausentes.
- Padronização dos canais de venda e indicadores de desconto.
- Validação dos relacionamentos entre dimensões e tabela fato.
- Preservação dos pedidos com informações incompletas, utilizando registros padrão quando necessário.

Os tratamentos permitiram estruturar os dados para análise, mantendo a rastreabilidade das limitações encontradas.


## 5. Modelagem dimensional

O Data Warehouse Pata Amiga foi estruturado utilizando modelagem dimensional, com uma tabela fato central e dimensões para contextualizar os indicadores de negócio.

A modelagem permite analisar os pedidos por loja, categoria, período e região de atendimento.

### 5.1. Tabela fato

**`fato_pedido`**

É a tabela central do modelo, com granularidade de um registro por pedido.

Contém as chaves de relacionamento com as dimensões e os indicadores utilizados nas análises.

Principais informações:

- Número do pedido.
- Loja responsável.
- Categoria do pedido.
- Data do pedido e data de entrega.
- Canal de venda.
- Indicador de desconto.
- Quantidade de itens.
- Valor líquido do pedido.
- Intervalos entre as etapas logísticas.
- Tempo total até a entrega.

Foram carregados **4.044 pedidos**, sem duplicidade de número de pedido.

### 5.2. Dimensões

| Dimensão | Finalidade |
|---|---|
| `dim_loja` | Informações cadastrais, porte, município e classificação da loja. |
| `dim_categoria` | Padronização e classificação das categorias de produtos e serviços. |
| `dim_tempo` | Análises por data, mês, ano e demais atributos de calendário. |
| `dim_praca` | Identificação das praças e regiões de atendimento. |

A tabela `bridge_loja_praca` representa o relacionamento entre lojas e praças, permitindo distribuir os indicadores regionais com fatores de ponderação e evitando a duplicação indevida do faturamento.

### 5.3. Integridade e tratamento de valores ausentes

A modelagem utiliza chaves substitutas (*surrogate keys*) para relacionar a tabela fato às dimensões.

Foram utilizados registros padrão para representar informações não identificadas, preservando os pedidos na base analítica.

A validação final confirmou:

- 4.044 pedidos carregados.
- 4.044 números de pedido distintos.
- Nenhuma chave estrangeira nula na tabela fato.
- 33 registros na dimensão loja, incluindo o registro padrão.
- 38 registros na dimensão categoria.
- 236 registros na dimensão tempo, incluindo o registro padrão.

### 5.4. Organização dos scripts

| Arquivo | Finalidade |
|---|---|
| `00-conferencia.sql` | Consultas de conferência e diagnóstico. |
| `01-carga-staging.sql` | Preparação e carga dos dados de origem. |
| `02-dimensoes-prontas.sql` | Estruturas e dados de apoio das dimensões. |
| `03-dimensoes.sql` | Construção e preparação das dimensões analíticas. |
| `04-fato.sql` | Transform

## 6. Respostas às perguntas de negócio

### 6.1. Pergunta 1 — Onde está o gargalo logístico?

**Objetivo:** identificar as etapas do processo de entrega que apresentam maiores tempos médios, comparando o desempenho das lojas por porte.

#### Resultados

| Porte da loja | Pedidos | Integração → Separação | Separação → Nota | Nota → Despacho | Despacho → Entrega | Tempo total |
|---|---:|---:|---:|---:|---:|---:|
| Pequena | 615 | 3,02 | 0,69 | 8,53 | 2,86 | 15,27 |
| Média | 1.663 | 1,98 | 0,62 | 3,34 | 2,03 | 8,06 |
| Grande | 1.763 | 1,96 | 0,64 | 3,32 | 2,01 | 8,04 |
| Não informado | 3 | 2,00 | 0,00 | 4,00 | 3,00 | 8,50 |

*Tempos expressos em dias, calculados a partir dos registros com informações disponíveis para cada indicador.*

#### Principais conclusões

O principal gargalo logístico identificado está no intervalo entre a emissão da nota fiscal e o despacho do pedido.

Nas lojas pequenas, essa etapa apresenta média de **8,53 dias**, significativamente superior às médias das lojas médias (3,34 dias) e grandes (3,32 dias).

O tempo total médio das lojas pequenas é de **15,27 dias**, enquanto lojas médias e grandes apresentam aproximadamente 8 dias.

#### Recomendações

- Investigar os processos de faturamento e expedição das lojas pequenas.
- Verificar possíveis limitações operacionais, de equipe e de integração entre sistemas.
- Monitorar o intervalo entre nota fiscal e despacho como indicador de desempenho.
- Priorizar ações corretivas nas lojas com maiores tempos médios.

#### Limitações da análise

As médias consideram somente os pedidos com datas suficientes para calcular os respectivos intervalos.

Como existem pedidos sem data de entrega, os resultados não devem ser interpretados como representativos de todas as entregas realizadas.

Os dados identificam diferenças de desempenho, mas não permitem determinar isoladamente a causa operacional dos atrasos.


### 6.2. Pergunta 2 — Quais categorias geram mais faturamento?

**Objetivo:** identificar as categorias de produtos e serviços com maior participação na receita da rede Pata Amiga.

#### Resultados

| Categoria | Pedidos | Faturamento (R$) | Participação |
|---|---:|---:|---:|
| Ração | 1.387 | 1.076.202,55 | 60,01% |
| Medicamento | 667 | 305.904,03 | 17,06% |
| Petisco | 759 | 128.590,16 | 7,17% |
| Serviço | 269 | 94.001,37 | 5,24% |
| Higiene | 507 | 92.314,45 | 5,15% |
| Acessório | 263 | 64.661,39 | 3,61% |
| Brinquedo | 192 | 31.634,56 | 1,76% |
| **Total** | **4.044** | **1.793.308,51** | **100%** |

#### Principais conclusões

A categoria **Ração** é a principal responsável pelo faturamento da rede, representando **60,01% da receita analisada**.

A segunda categoria mais relevante é Medicamento, com 17,06%.

Juntas, Ração e Medicamento representam aproximadamente **77,07% do faturamento**.

Essa concentração indica que o desempenho financeiro da rede depende significativamente dessas duas categorias.

#### Recomendações

- Priorizar a disponibilidade e o controle de estoque de rações e medicamentos.
- Investigar oportunidades de vendas complementares com petiscos, higiene e acessórios.
- Monitorar a concentração do faturamento para reduzir riscos comerciais.
- Avaliar estratégias específicas para categorias com menor participação.

#### Limitações da análise

O faturamento considera os valores líquidos disponíveis na base.

Existem **121 pedidos sem valor líquido**, que não contribuem para a soma do faturamento.

A participação percentual representa a receita registrada nos dados analisados, não necessariamente o faturamento contábil completo da empresa.


### 6.3. Pergunta 3 — Os descontos estão associados a tickets médios maiores?

**Objetivo:** comparar o ticket médio dos pedidos com e sem desconto, considerando os diferentes canais de venda da rede Pata Amiga.

#### Resultados

| Canal de venda | Ticket médio sem desconto (R$) | Ticket médio com desconto (R$) |
|---|---:|---:|
| Aplicativo (App) | 167,63 | 488,04 |
| Loja física | 197,55 | 494,04 |
| Site | 189,68 | 501,92 |
| Telefone | 195,23 | 514,02 |
| WhatsApp | 179,26 | 514,33 |

Os valores representam a média do valor líquido dos pedidos com informações disponíveis.

#### Principais conclusões

Em todos os cinco canais identificados, os pedidos classificados como realizados com desconto apresentaram ticket médio superior ao dos pedidos sem desconto.

O WhatsApp apresentou o maior ticket médio entre os pedidos com desconto (R$ 514,33), seguido pelo Telefone (R$ 514,02).

O resultado sugere uma associação entre a utilização de descontos e pedidos de maior valor.

Entretanto, **essa associação não demonstra que os descontos causaram o aumento do ticket médio**.

Outros fatores podem explicar as diferenças, como o perfil dos clientes, a quantidade de produtos, o tipo de mercadoria e as regras das promoções.

#### Recomendações

- Investigar o perfil dos pedidos com e sem desconto.
- Avaliar a margem de lucro, e não apenas o faturamento.
- Comparar pedidos semelhantes para reduzir distorções.
- Monitorar o desempenho das promoções por canal.
- Realizar testes controlados antes de concluir que os descontos aumentam as vendas.

#### Limitações da análise

A base não permite determinar isoladamente o efeito causal dos descontos sobre o comportamento de compra.

Também existem pedidos sem informação de desconto, canal de venda ou valor líquido.

A análise utiliza os valores líquidos registrados, sem informações suficientes para calcular a margem de contribuição ou o retorno financeiro efetivo das promoções.


### 6.4. Pergunta 4 — Quais praças concentram o faturamento da rede?

**Objetivo:** identificar as regiões de atendimento com maior participação no faturamento da Pata Amiga.

#### Resultados

| Praça de atendimento | Faturamento (R$) | Participação |
|---|---:|---:|
| Vale do Itajaí | 633.746,09 | 35,34% |
| Grande Florianópolis | 283.546,75 | 15,81% |
| Norte Industrial | 175.431,90 | 9,78% |
| Litoral Sul | 137.051,20 | 7,64% |
| Litoral Norte | 128.872,75 | 7,19% |
| Extremo Oeste | 98.359,18 | 5,48% |
| Carbonífera | 88.707,42 | 4,95% |
| Serra Catarinense | 80.477,64 | 4,49% |
| Meio-Oeste | 58.955,63 | 3,29% |
| Foz do Itajaí | 46.749,72 | 2,61% |
| Planalto Norte | 31.100,84 | 1,73% |
| Planalto Serrano | 29.323,10 | 1,64% |

#### Principais conclusões

O Vale do Itajaí concentra a maior parcela do faturamento regional, representando **35,34% da receita total analisada**.

A Grande Florianópolis aparece na segunda posição, com 15,81%.

Juntas, essas duas praças representam aproximadamente **51,15% do faturamento da rede**.

Os resultados indicam uma concentração relevante da receita nessas regiões.

#### Recomendações

- Priorizar o acompanhamento comercial e operacional das praças com maior participação.
- Investigar oportunidades de crescimento nas regiões com menor faturamento.
- Comparar faturamento, quantidade de lojas e população atendida antes de definir investimentos.
- Monitorar a concentração regional da receita para avaliar riscos comerciais.

#### Cuidados metodológicos

O relacionamento entre lojas e praças foi realizado por meio da tabela `bridge_loja_praca`, utilizando fatores de ponderação para evitar a contagem integral do mesmo faturamento em múltiplas praças.

Os percentuais foram calculados em relação ao faturamento total analisado.

Os pedidos sem loja identificada podem não ser atribuídos a uma praça, e diferenças residuais também podem ocorrer por arredondamento.

O faturamento regional, isoladamente, não permite concluir quais regiões apresentam maior rentabilidade ou potencial de expansão.


### 6.5. Pergunta 5 — Expansão da rede e desempenho das franquias

**Objetivo:** avaliar indicadores que possam apoiar decisões de expansão da rede Pata Amiga, comparar o faturamento por faixa de franquia e identificar limitações dos dados.

#### 6.5.1. Indicadores para expansão

Foi calculada a quantidade de itens vendidos por mil habitantes, utilizando os dados de vendas das lojas e a população dos municípios.

| Município | Itens por mil habitantes | Tempo médio de entrega (dias) |
|---|---:|---:|
| Rio dos Cedros | 41,87 | 14,31 |
| Presidente Getúlio | 34,84 | 14,26 |
| Ibirama | 32,07 | 15,50 |
| Itapoá | 25,94 | 15,53 |
| Santo Amaro da Imperatriz | 23,71 | 16,00 |
| Taió | 19,37 | 14,63 |
| Timbó | 17,86 | 7,77 |
| Gaspar | 16,72 | 8,10 |
| Otacílio Costa | 15,86 | 15,72 |
| Ituporanga | 13,75 | 16,63 |

**Conclusão:** Rio dos Cedros apresentou o maior indicador de itens vendidos por mil habitantes (41,87), seguido por Presidente Getúlio (34,84) e Ibirama (32,07).

Entretanto, esse indicador utiliza as vendas históricas das lojas em relação à população municipal. Portanto, não mede diretamente a demanda potencial por uma nova unidade.

**Recomendação:** utilizar os resultados como ponto de partida para estudos de mercado, considerando concorrência, renda, densidade populacional, cobertura logística, custos e demanda ainda não atendida.

#### 6.5.2. Faturamento por faixa de franquia

| Faixa de franquia | Pedidos | Faturamento (R$) |
|---|---:|---:|
| Ouro | 2.316 | 1.011.264,38 |
| Diamante | 818 | 382.209,74 |
| Prata | 719 | 314.812,03 |
| Bronze | 188 | 84.036,06 |
| Não informado | 3 | 986,30 |
| **Total** | **4.044** | **1.793.308,51** |

A faixa **Ouro** apresentou o maior faturamento, seguida por Diamante e Prata.

Essa análise utiliza a classificação de franquia disponível no cadastro das lojas.

**Limitação importante:** não existe histórico suficiente para confirmar se cada loja já pertencia à mesma faixa no momento em que os pedidos foram realizados.

Portanto, os resultados não devem ser interpretados como faturamento histórico por faixa vigente na data de cada venda.

#### 6.5.3. Limitações dos dados

A análise identificou as seguintes situações:

| Limitação | Pedidos | Percentual |
|---|---:|---:|
| Loja não identificada | 3 | 0,07% |
| Data de entrega ausente | 1.953 | 48,29% |
| Quantidade de itens ausente | 257 | 6,36% |
| Valor líquido ausente | 121 | 2,99% |

Essas limitações afetam diferentes indicadores:

- A ausência de datas de entrega reduz a cobertura das análises logísticas.
- A ausência de quantidade de itens pode afetar indicadores de volume de vendas.
- A ausência de valor líquido limita a apuração do faturamento.
- Pedidos sem loja identificada não podem ser atribuídos com segurança a uma unidade ou praça.

#### Recomendações finais

1. Melhorar o preenchimento e a validação dos dados na origem.
2. Priorizar a investigação dos gargalos logísticos nas lojas pequenas.
3. Monitorar a concentração do faturamento nas categorias Ração e Medicamento.
4. Avaliar a rentabilidade das campanhas de desconto antes de ampliá-las.
5. Utilizar indicadores demográficos e comerciais complementares antes de decidir pela abertura de novas lojas.
6. Implantar histórico das alterações cadastrais das franquias para permitir análises temporais mais precisas.

Os resultados fornecem subsídios para decisões gerenciais, mas devem ser interpretados considerando a qualidade, a cobertura e as limitações dos dados disponíveis.