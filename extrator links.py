import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re
import io

# Configuração da página
st.set_page_config(page_title="Extrator de Processos Anatel", page_icon="📡")

st.title("📡 Extrator de Links - Anatel SEI")
st.markdown("""
Esta ferramenta processa o ficheiro HTML exportado e filtra apenas os processos de 
**Declaração de Conformidade - Importado uso Próprio**.
""")

# Upload do ficheiro HTML
uploaded_file = st.file_uploader("Carregue o ficheiro HTML original", type=['html'])

if uploaded_file is not None:
    # Leitura do conteúdo
    html_content = uploaded_file.read().decode("utf-8")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    dados_extraidos = []
    
    # Termo exato de filtragem conforme consta no documento
    categoria_alvo = "Declaração de Conformidade - Importado uso Próprio"
    
    # Procurar todas as ocorrências do texto da categoria
    # Usamos regex para ignorar variações de espaços ou quebras de linha no HTML
    tags_categoria = soup.find_all(string=re.compile(re.escape(categoria_alvo)))

    for tag in tags_categoria:
        # 1. Tentar encontrar o número do processo no texto próximo
        # O padrão é 00000.000000/0000-00
        match_processo = re.search(r'\d{5}\.\d{6}/\d{4}-\d{2}', tag.parent.get_text())
        
        # 2. Localizar o link (tag <a>) associado
        # Normalmente está na mesma célula ou numa célula próxima (tag pai <tr>)
        linha_pai = tag.find_parent('tr')
        link_tag = None
        
        if linha_pai:
            link_tag = linha_pai.find('a', href=True)
        
        if not link_tag:
            # Caso não esteja na mesma linha, procura o link imediatamente seguinte
            link_tag = tag.parent.find_next('a', href=True)

        if link_tag and match_processo:
            num_processo = match_processo.group(0)
            url_sei = link_tag['href']
            
            # Evitar duplicados
            if not any(d['Processo'] == num_processo for d in dados_extraidos):
                dados_extraidos.append({
                    "Processo": num_processo,
                    "Link": url_sei
                })

    if dados_extraidos:
        df = pd.DataFrame(dados_extraidos)
        
        st.success(f"Foram encontrados {len(df)} processos únicos de Importação para Uso Próprio.")
        
        # Exibição da tabela com links clicáveis
        st.write("### Lista de Processos e Links")
        
        # Formatação para tornar o link clicável no Streamlit
        df_display = df.copy()
        df_display['Aceder'] = df_display['Link'].apply(lambda x: f"[Abrir no SEI]({x})")
        
        st.table(df_display[['Processo', 'Aceder']])

        # Botão para exportar CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descarregar CSV com os Links",
            data=csv,
            file_name='links_processos_importacao.csv',
            mime='text/csv',
        )
    else:
        st.warning("Nenhum processo foi encontrado com esse critério. Verifique se o ficheiro carregado é o correto.")
