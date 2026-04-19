import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re

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
    # Leitura do conteúdo com errors='ignore' para evitar problemas de formatação
    html_content = uploaded_file.read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    dados_extraidos = []
    
    # Encontrar todos os links (tags <a>) no documento
    links = soup.find_all('a', href=True)
    
    for link in links:
        # Subir na árvore HTML até encontrar o bloco que contém o link (geralmente <tr> ou <p>)
        bloco_pai = link.find_parent(['tr', 'p', 'div'])
        
        if bloco_pai:
            # Juntar todo o texto fragmentado dentro desse bloco num único texto limpo
            texto_bloco = bloco_pai.get_text(separator=" ", strip=True)
            
            # Verificar se a categoria alvo está dentro desse bloco de texto
            # Usamos regex para ignorar problemas com letras maiúsculas/minúsculas ou espaços duplos
            if re.search(r'Importado\s+uso\s+Pr[oó]prio', texto_bloco, re.IGNORECASE):
                
                # Extrair o número do processo (Formato: XXXXX.XXXXXX/XXXX-XX)
                match_processo = re.search(r'\d{5}\.\d{6}/\d{4}-\d{2}', texto_bloco)
                
                if match_processo:
                    num_processo = match_processo.group(0)
                    url_sei = link['href']
                    
                    # Evitar adicionar o mesmo processo e link mais de uma vez
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
        
        # Formatação para tornar o link clicável no painel do Streamlit
        df_display = df.copy()
        df_display['Aceder'] = df_display['Link'].apply(lambda x: f"[Abrir no SEI]({x})")
        
        st.table(df_display[['Processo', 'Aceder']])

        # Botão para exportar CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descarregar CSV com os Links",
            data=csv,
            file_name='links_processos_importacao.csv',
            mime='text/csv',
        )
    else:
        st.error("Nenhum processo foi encontrado. O HTML pode não conter os dados ou estar numa formatação muito atípica.")
