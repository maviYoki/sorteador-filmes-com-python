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
            # Headers otimizados para evitar bloqueios e simular um PC real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            with st.spinner('Lendo a lista de filmes...'):
                response = requests.get(url_lista, headers=headers)
            
            # Verifica se o site respondeu com sucesso (200 OK)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Busca pelo modo "Detalhado" (articles) baseado no seu HTML
                filmes = soup.find_all("article", class_="list-detailed-entry")
                
                # Fallback para modo Grade se não achar articles
                if not filmes:
                    filmes = soup.find_all("li", class_="poster-container")
                
                if filmes:
                    escolhido = random.choice(filmes)
                    
                    # --- 1. Extração do Título ---
                    elemento_titulo = escolhido.find("h2", class_="name")
                    if elemento_titulo:
                        titulo = elemento_titulo.text.strip()
                    else:
                        img_alt = escolhido.find("img")
                        titulo = img_alt.get('alt', 'Filme Misterioso') if img_alt else "Sem Título"

                    # --- 2. Extração da Imagem (Blindada) ---
                    capa = None
                    
                    # TENTATIVA 1: Busca direta pelo seletor CSS da imagem do poster
                    # Procura img dentro de div.poster ou div.film-poster
                    img_tag = escolhido.select_one(".poster img, .film-poster img")
                    
                    if img_tag:
                        # Prioridade: srcset > data-src > src
                        if img_tag.get('srcset'):
                            capa = img_tag.get('srcset').split(" ")[0]
                        elif img_tag.get('data-src'):
                            capa = img_tag.get('data-src')
                        elif img_tag.get('src'):
                            capa = img_tag.get('src')
                            
                    # TENTATIVA 2: Se falhar, busca no atributo do container React (Backup)
                    if not capa:
                        div_react = escolhido.find("div", class_="react-component")
                        if div_react and div_react.get('data-poster-url'):
                            capa = div_react.get('data-poster-url')
                    
                    # TENTATIVA 3: Varredura final por qualquer imagem válida
                    if not capa:
                        imgs = escolhido.find_all("img")
                        for img in imgs:
                            src_cand = img.get('src', '')
                            # Pega se tiver 'resized' ou 'film-poster' na url e não for placeholder vazio
                            if ('resized' in src_cand or 'poster' in src_cand) and 'empty' not in src_cand:
                                capa = src_cand
                                break

                    # Tratamento final da URL
                    if capa:
                        if not capa.startswith("http"):
                            # Se for link relativo, adiciona o domínio
                            capa = "https://letterboxd.com" + capa
                    else:
                        capa = "https://s.ltrbxd.com/static/img/empty-poster-70.png"

                    # --- 3. Extração do Link ---
                    div_react = escolhido.find("div", class_="react-component")
                    link_suffix = div_react.get('data-target-link') if div_react else None
                    
                    if link_suffix:
                        link_final = "https://letterboxd.com" + link_suffix
                    else:
                        link_tag = escolhido.find("a")
                        link_final = "https://letterboxd.com" + link_tag['href'] if link_tag else "#"

                    # --- 4. Extração da Review ---
                    review = ""
                    div_texto = escolhido.find("div", class_="body-text")
                    if div_texto:
                        review = div_texto.text.strip()

                    # --- Exibição ---
                    st.divider()
                    st.success(f"🎉 O filme escolhido foi: **{titulo}**")
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # use_column_width ajusta melhor em mobile/telas pequenas
                        st.image(capa, use_container_width=True)
                    
                    with col2:
                        if review:
                            st.info(f"📝 **Sua nota:**\n\n_{review}_")
                        else:
                            st.write("_Nenhum comentário disponível para este filme._")
                            
                        st.link_button("Ver no Letterboxd", link_final)

                else:
                    st.error("Não encontrei filmes. Verifique se a lista é pública.")
            else:
                st.error(f"Erro ao conectar: {response.status_code}")
                
        except Exception as e:
            st.error(f"Ocorreu um erro técnico: {e}")
