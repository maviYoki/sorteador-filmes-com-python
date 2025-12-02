import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

# Configurações iniciais da página
st.set_page_config(
    page_title="Sorteador Letterboxd", 
    page_icon="🎬",
    layout="centered"
)

# Títulos e textos
st.title("🎬 Sorteador de Filmes")
st.write("Cole o link da sua lista do Letterboxd abaixo e deixe o destino escolher seu próximo filme.")

# Campo de entrada
url_lista = st.text_input("Link da Lista", placeholder="https://letterboxd.com/seu_usuario/list/sua-lista/")

# Botão de ação
if st.button("Sortear Filme"):
    if not url_lista:
        st.warning("Por favor, cole a URL da lista antes de sortear.")
    else:
        try:
            # Headers para simular um navegador real e evitar bloqueios
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            with st.spinner('Lendo a lista de filmes...'):
                response = requests.get(url_lista, headers=headers)
            
            # Verifica se o site respondeu com sucesso (200 OK)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Tenta buscar pelo modo "Detalhado" (articles) que é o layout da sua lista
                filmes = soup.find_all("article", class_="list-detailed-entry")
                
                # Se não encontrar, tenta o modo "Grade" (fallback)
                if not filmes:
                    filmes = soup.find_all("li", class_="poster-container")
                
                # Se encontrou filmes, faz o sorteio
                if filmes:
                    escolhido = random.choice(filmes)
                    
                    # --- 1. Extração do Título ---
                    elemento_titulo = escolhido.find("h2", class_="name")
                    if elemento_titulo:
                        titulo = elemento_titulo.text.strip()
                    else:
                        # Tenta pegar do atributo alt da imagem se não tiver h2
                        img = escolhido.find("img")
                        titulo = img.get('alt', 'Filme Misterioso') if img else "Sem Título"

                    # --- 2. Extração da Imagem (Blindada) ---
                    capa = "https://s.ltrbxd.com/static/img/empty-poster-70.png" # Imagem padrão
                    
                    # Procura a tag de imagem dentro do item
                    img_tag = escolhido.find("img")
                    if img_tag:
                        # O Letterboxd usa lazy loading, então a imagem real pode estar em atributos diferentes
                        # Prioridade: srcset (melhor qualidade) > data-src > src
                        if img_tag.get('srcset'):
                            capa = img_tag.get('srcset').split(" ")[0] # Pega a primeira url do srcset
                        elif img_tag.get('data-src'):
                            capa = img_tag.get('data-src')
                        else:
                            capa = img_tag.get('src')
                    
                    # Garante que a URL da imagem seja absoluta
                    if capa and not capa.startswith("http"):
                        capa = "https://letterboxd.com" + capa

                    # --- 3. Extração do Link ---
                    div_react = escolhido.find("div", class_="react-component")
                    link_suffix = div_react.get('data-target-link') if div_react else None
                    
                    if link_suffix:
                        link_final = "https://letterboxd.com" + link_suffix
                    else:
                        link_tag = escolhido.find("a")
                        link_final = "https://letterboxd.com" + link_tag['href'] if link_tag else "#"

                    # --- 4. Extração da Review/Comentário ---
                    review = ""
                    div_texto = escolhido.find("div", class_="body-text")
                    if div_texto:
                        review = div_texto.text.strip()

                    # --- Exibição do Resultado ---
                    st.divider()
                    st.success(f"🎉 O filme escolhido foi: **{titulo}**")
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(capa, use_container_width=True)
                    
                    with col2:
                        if review:
                            st.info(f"📝 **Sua nota:**\n\n_{review}_")
                        else:
                            st.write("_Nenhum comentário disponível para este filme._")
                            
                        st.link_button("Ver no Letterboxd", link_final)

                else:
                    st.error("Não encontrei filmes nesta página. Verifique se a lista é pública ou se o link está correto.")
            else:
                st.error(f"Erro ao conectar com o Letterboxd. Código: {response.status_code}")
                
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
