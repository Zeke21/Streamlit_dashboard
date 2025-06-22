import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import plotly.graph_objs as go

@st.cache_data
def load_data():
    base = pd.read_csv("personal_transactions.csv")
    base["Date"] = pd.to_datetime(base["Date"])
    return base

base = load_data()
st.session_state["base_df"] = base

#base
base.info()

#st.dataframe(base)

base.groupby("Transaction Type")["Amount"].sum().reset_index()
pagamento = base.groupby("Transaction Type")["Amount"].sum().reset_index()

pagamento.set_index("Transaction Type", inplace=True)

#quantidade paga por tipo de cartao/ grafico de pizza
# Cria a lista de métodos de pagamento disponíveis
metodo_pagamento = base["Transaction Type"].value_counts().index

# Cria o seletor no sidebar
pagamentos = st.sidebar.selectbox("Método de pagamento", metodo_pagamento)

# Filtra o dataframe com base no método de pagamento selecionado
filtro_pagamento = base[base["Transaction Type"] == pagamentos]

# Conta os tipos de pagamento filtrados
tipo_pagamento = filtro_pagamento["Account Name"].value_counts().reset_index()
tipo_pagamento.columns = ["Account Name", "count"]

# Cria o gráfico de pizza com base no filtro
fig1 = px.pie(tipo_pagamento, values="count", names="Account Name", title=f"Distribuição de '{pagamentos}' por Nome do cartão")

# Exibe o gráfico
#st.plotly_chart(fig1)

#total pago por debito e por credito/ grafico de barras
pagamento.reset_index(inplace=True)
fig2 = px.bar(pagamento,
              x="Transaction Type",
              y="Amount",
              title="Tipo de Pagamento",
              text_auto=True)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

base["Account Name"].unique()
base["Category"].unique()
base["Description"].unique()

categoria = base.value_counts("Category").reset_index()

base["Year"] = base["Date"].dt.year

# Seleciona anos disponíveis em ordem crescente
data = sorted(base["Year"].unique())

# Cria o seletor no sidebar
ano = st.sidebar.selectbox("Ano", data)

# Filtra o dataframe com base no ano selecionado
filtro_data = base[base["Year"] == ano]

# Conta os tipos de pagamento filtrados
tipo_pagamento = filtro_data["Account Name"].value_counts().reset_index()
tipo_pagamento.columns = ["Account Name", "count"]

# Conta quantas transações ocorreram naquele ano
tipo_ano = filtro_data["Year"].value_counts().reset_index()
tipo_ano.columns = ["Year", "Amount"]

# Gráfico de área com os dados filtrados
fig4 = px.bar(filtro_data, x="Date", y="Amount", title="Gráfico de Área - Vendas por Ano")
st.plotly_chart(fig4)
