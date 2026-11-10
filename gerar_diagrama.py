
from graphviz import Digraph

# Diagrama dimensional do Data Warehouse Pata Amiga
g = Digraph("DW_Pata_Amiga", format="png", engine="dot")

g.attr(
    rankdir="TB",
    bgcolor="white",
    nodesep="0.6",
    ranksep="1.0",
    splines="polyline"
)

g.attr("node", shape="plain", fontname="Arial")
g.attr("edge", color="#64748b", arrowsize="0.7")

def tabela(nome, colunas, cor):
    linhas = "".join(
        f'<TR><TD ALIGN="LEFT" PORT="{coluna}" '
        f'BGCOLOR="#ffffff">'
        f'<FONT FACE="Arial" POINT-SIZE="10">'
        f'{coluna}</FONT></TD></TR>'
        for coluna in colunas
    )

    rotulo = f'''<
    <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
           CELLPADDING="6" COLOR="#94a3b8">
      <TR>
        <TD BGCOLOR="{cor}">
          <FONT FACE="Arial" COLOR="white" POINT-SIZE="13">
            <B>{nome}</B>
          </FONT>
        </TD>
      </TR>
      {linhas}
    </TABLE>
    >'''

    g.node(nome, label=rotulo)


tabela("fato_pedido", [
    "sk_pedido",
    "numero_pedido",
    "sk_tempo_pedido",
    "sk_tempo_entrega",
    "sk_loja",
    "sk_categoria",
    "houve_desconto",
    "canal_pedido",
    "dt_pedido",
    "qt_itens",
    "vl_liquido",
    "dias_integracao_separacao",
    "dias_separacao_nota",
    "dias_nota_despacho",
    "dias_despacho_entrega",
    "dias_total_ate_entrega"
], "#1d4ed8")

tabela("dim_loja", [
    "sk_loja",
    "cod_loja",
    "chave_loja",
    "nome_loja",
    "cidade",
    "uf",
    "mesorregiao",
    "populacao_cidade",
    "area_venda_m2",
    "porte",
    "faixa_franquia",
    "formato_loja"
], "#0f766e")

tabela("dim_categoria", [
    "sk_categoria",
    "categoria_origem",
    "nome_categoria",
    "grupo_categoria"
], "#0f766e")

tabela("dim_tempo", [
    "sk_tempo",
    "data",
    "ano",
    "mes",
    "dia",
    "ano_mes",
    "nome_mes",
    "trimestre",
    "dia_semana",
    "fim_de_semana"
], "#0f766e")

tabela("bridge_loja_praca", [
    "cod_loja",
    "sk_praca",
    "fator_publico"
], "#7c3aed")

tabela("dim_praca", [
    "sk_praca",
    "cod_praca",
    "nome_praca",
    "regional",
    "domicilios_com_pet"
], "#7c3aed")

# Relacionamentos lógicos do modelo dimensional
g.edge("fato_pedido:sk_loja", "dim_loja:sk_loja",
       label="loja", dir="none")

g.edge("fato_pedido:sk_categoria", "dim_categoria:sk_categoria",
       label="categoria", dir="none")

g.edge("fato_pedido:sk_tempo_pedido", "dim_tempo:sk_tempo",
       label="data pedido", dir="none")

g.edge("fato_pedido:sk_tempo_entrega", "dim_tempo:sk_tempo",
       label="data entrega", dir="none",
       color="#2563eb")

# Relacionamento auxiliar por código de loja
g.edge("dim_loja:cod_loja", "bridge_loja_praca:cod_loja",
       style="dashed", dir="none")

g.edge("bridge_loja_praca:sk_praca", "dim_praca:sk_praca",
       style="dashed", dir="none")

# Exportar para PNG
g.render(
    filename="diagrama_estrela_pata_amiga",
    directory=".",
    cleanup=True
)

print("Diagrama PNG gerado com sucesso!")
