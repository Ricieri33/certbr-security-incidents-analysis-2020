# %% limpeza
import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_csv("../data/Dados.csv", sep=";")

df = df.dropna(how="all")

df = df.loc[:, ~df.columns.str.contains("Unnamed")]

df.columns = (
     df.columns
         .str.strip()
         .str.lower()
         .str.normalize("NFKD")
         .str.encode("ascii", errors="ignore")
         .str.decode("utf-8")
)

df.rename(columns={
        "ms": "mes",
        "invaso": "invasao"
    }, inplace=True)

mapa_meses = {
        "jan": "01/20",
        "fev": "02/20",
        "mar": "03/20",
        "abr": "04/20",
        "mai": "05/20",     
        "jun": "06/20"
}

df["Mes_ref"] = df["mes"].map(mapa_meses)

ordem_meses = ["01/20", "02/20", "03/20", "04/20", "05/20", "06/20"]

df["Mes_ref"] = pd.Categorical(
    df["Mes_ref"],
    categories=ordem_meses,
    ordered=True
)
df = df.sort_values("Mes_ref")

# %% Garantir que colunas numéricas são numéricas
colunas_numericas = df.columns.difference(["mes", "Mes_ref"])

df[colunas_numericas] = df[colunas_numericas].apply(pd.to_numeric, errors="coerce")

# %% Validar consistência do total
categorias = df.columns.difference(["mes", "Mes_ref", "total"])

df["soma_calculada"] = df[categorias].sum(axis=1)

if (df["soma_calculada"] == df["total"]).all():
    print("Total consistente com a soma das categorias.")
else:
    print("Inconsistência encontrada no total.")

df.drop(columns=["soma_calculada"], inplace=True)

# %% Crescimento percentual mês a mês do total
df["crescimento_total_%"] = df["total"].pct_change() * 100

print(df[["Mes_ref", "total", "crescimento_total_%"]])

# %% Qual tipo puxou o crescimento de março?
colunas_excluir_diff = ["mes","total", "crescimento_total_%"]

df_diff = (
        df.set_index("Mes_ref")
        .drop(columns=colunas_excluir_diff)
        .diff()
)

print("Variação de fevereiro para março:")
print(df_diff.loc["03/20"].sort_values(ascending=False))

# %% Contribuição (%)
variacao_mar = df_diff.loc["03/20"]

contrib_percentual = (variacao_mar / variacao_mar.sum()) * 100

print("Contribuição percentual no crescimento de março:")
print(contrib_percentual.sort_values(ascending=False))

# %% Cálculo do total acumulado por categoria no período
colunas_excluir = ["mes", "Mes_ref", "total", "crescimento_total_%"]
categorias = df.columns.difference(colunas_excluir)

totais = df[categorias].sum()

totais_ordenados = totais.sort_values(ascending=False)

# %% Participação percentual por categoria no período
percentual = (totais/totais.sum()) *100

percentual_ordenado = (percentual.sort_values(ascending = False))

print(percentual_ordenado)
# %% Identificar o principal incidente (%)
principal = percentual_ordenado.index[0]

valor_principal = percentual_ordenado.iloc[0]

print(f"Incidente dominante: {principal} ({valor_principal:.2f}%)")

# %% Mes de pico
mes_pico = df.loc[df["total"].idxmax(), "mes"]

print(f"Mês de maior volume absoluto: {mes_pico}")

# %% Valores do mes de pico
print(df.loc[df["mes"] == mes_pico])

# %% Top3 incidentes
top3 = totais_ordenados.head(3).index

# %% Gráfico de ranking geral por tipo de incidente
plt.figure()

totais_ordenados.plot (kind="bar")
plt.title("Incidentes de Segurança por Tipo (Jan-Jun 2020)")
plt.xlabel("Tipo de Incidente")
plt.ylabel("Quantidade de registros")

plt.tight_layout()

plt.savefig("../images/ranking_incidentes.png", dpi=300) 
plt.show()  
# %% Gráfico de evolução mensal do total de incidentes
plt.figure()

plt.plot(df["Mes_ref"], df["total"], marker="o")
plt.title("Incidentes de Segurança por Mês (2020)")
plt.xlabel("Mês/Ano")
plt.ylabel("Total de incidentes")
plt.grid(True)

plt.tight_layout()

plt.savefig("../images/evolucao_mensal_total.png", dpi=300)
plt.show()
# %% Grafico top3 incidentes
plt.figure()

for col in top3:
    plt.plot(df["Mes_ref"], df[col], marker="o", label=col)

plt.title("Top 3 Incidentes - Evolução Mensal (2020)")
plt.xlabel("Mês/Ano")
plt.ylabel("Quantidade")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig("../images/top3_evolucao_mensal.png", dpi=300)
plt.show()

#%% Grafico top3 incidentes isolados
for col in top3:
    plt.figure()
    plt.plot(df["Mes_ref"], df[col], marker="o")
    plt.title(f"{col.upper()} - Evolução Mensal (2020)")
    plt.xlabel("Mês/Ano")
    plt.ylabel("Quantidade")
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(f"../images/{col}_evolucao_mensal.png", dpi=300)
    plt.show()