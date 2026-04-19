import streamlit as st
import pandas as pd

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Processos Anatel",
    page_icon="📡",
    layout="wide"
)

# 2. Título e descrição da aplicação
st.title("📡 Painel de Processos Anatel")
st.markdown("Este painel exibe os processos extraídos do sistema SEI referentes à categoria **Declaração de Conformidade - Importado uso Próprio**.")

# 3. Dados extraídos (Lista dos 64 processos únicos)
processos_uso_proprio = [
    "53500.017392/2026-19", "53500.019353/2026-56", "53500.019417/2026-19", "53500.019436/2026-45",
    "53500.019576/2026-13", "53500.020060/2026-11", "53500.020213/2026-21", "53500.020448/2026-12",
    "53500.020539/2026-58", "53500.020185/2026-41", "53500.021492/2026-40", "53500.021571/2026-51",
    "53500.021599/2026-98", "53500.021691/2026-58", "53500.021709/2026-11", "53500.021737/2026-39",
    "53500.021754/2026-76", "53500.021764/2026-10", "53500.021772/2026-58", "53500.021778/2026-25",
    "53500.021829/2026-19", "53500.021832/2026-32", "53500.021905/2026-96", "53500.021911/2026-43",
    "53500.022041/2026-20", "53500.022055/2026-43", "53500.022093/2026-04", "53500.022103/2026-01",
    "53500.022127/2026-52", "53500.022192/2026-88", "53500.022227/2026-89", "53500.022247/2026-50",
    "53500.022283/2026-13", "53500.022291/2026-60", "53500.022312/2026-47", "53500.022476/2026-74",
    "53500.022523/2026-80", "53500.022602/2026-91", "53500.022716/2026-31", "53500.022720/2026-07",
    "53500.022721/2026-43", "53500.022736/2026-10", "53500.022749/2026-81", "53500.022751/2026-50",
    "53500.022882/2026-37", "53500.022909/2026-91", "53500.023051/2026-82", "53500.023352/2026-14",
    "53500.023511/2026-72", "53500.023536/2026-76", "53500.023775/2026-26", "53500.023781/2026-83",
    "53500.023785/2026-61", "53500.023790/2026-74", "53500.023797/2026-96", "53500.023816/2026-84",
    "53500.024519/2026-56", "53500.024782/2026-45", "53500.025487/2026-14", "53500.025587/2026-32",
    "53500.025641/2026-40", "53500.025642/2026-94", "53500.025653/2026-74", "53500.025755/2026-90"
]

# Criar um DataFrame com os dados
df = pd.DataFrame(processos_uso_proprio, columns=["Número do Processo SEI"])
df["Categoria"] = "Importado para Uso Próprio"
df["Status"] = "Em Análise / Exigência" # Adicionada coluna extra para contexto

# 4. Barra lateral interativa para pesquisa
st.sidebar.header("🔍 Pesquisa")
termo_busca = st.sidebar.text_input("Procurar por número (ex: 025641):", "")

# Lógica de filtragem
if termo_busca:
    df_filtrado = df[df["Número do Processo SEI"].str.contains(termo_busca, case=False)]
else:
    df_filtrado = df

# 5. Apresentação das Métricas
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total de Processos Exibidos", value=len(df_filtrado))
with col2:
    st.metric(label="Total Original", value=len(df))

# 6. Tabela de Dados Interativa
st.write("### Detalhes dos Processos")
st.dataframe(
    df_filtrado, 
    use_container_width=True, 
    hide_index=True
)

# 7. Botão para exportar dados para CSV
st.write("---")
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descarregar Tabela em CSV",
    data=csv,
    file_name='processos_uso_proprio_anatel.csv',
    mime='text/csv',
)