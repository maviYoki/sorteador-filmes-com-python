import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

st.set_page_config(page_title="Sorteador Letterboxd", page_icon="🎬")

st.title("🎬 Sorteador (Modo Detalhado)")
st.write("Esse código foi feito sob medida para a estrutura da sua lista.")

url_lista = st.text_input("URL da Lista", placeholder="https://letterboxd.com/...")

if st.button("Sortear Filme"):
    if not url_lista:
        st.warning("Cole a URL primeiro.")
    else:
        try:
            # Headers para fingir ser um navegador (evita bloqueio 403)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            with st.spinner('Acessando Letterboxd...'):
                response = requests.get(url_lista, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Procuramos por <article> com a classe que aparece no seu DevTools
                filmes = soup.find_all("article", class_="list-detailed-entry")
                
                st.write(f"🔍 Encontrei {len(filmes)} filmes na lista.")
                
                if filmes:
                    # Sorteio
                    escolhido = random.choice(filmes)
                    
                    # 1. TÍTULO (Fica dentro do h2 com classe 'name')
                    elemento_titulo = escolhido.find("h2", class_="name")
                    titulo = elemento_titulo.text.strip() if elemento_titulo else "Título Desconhecido"
                    
                    # 2. IMAGEM
                    capa = "https://s.ltrbxd.com/static/img/empty-poster-70.png" # Fallback
                    div_poster = escolhido.find("div", class_="poster")
                    
                    if div_poster:
                        img_tag = div_poster.find("img")
                        if img_tag:
                            capa = img_tag.get('src')
                            
                    # 3. LINK
                    div_react = escolhido.find("div", class_="react-component")
                    link_suffix = div_react.get('data-target-link') if div_react else None
                    
                    if link_suffix:
                        link_final = "https://letterboxd.com" + link_suffix
                    else:
                        # Tenta pegar do título se falhar
                        link_tag = elemento_titulo.find("a") if elemento_titulo else None
                        link_final = "https://letterboxd.com" + link_tag['href'] if link_tag else "#"

                    # 4. SUA REVIEW (O texto que aparece embaixo)
                    review = ""
                    div_texto = escolhido.find("div", class_="body-text")
                    if div_texto:
                        review = div_texto.text.strip()

                    st.divider()
                    st.success(f"🎉 Filme Sorteado: **{titulo}**")
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(capa, use_container_width=True)
                    with col2:
                        if review:
                            st.info(f"📝 **O que você disse:**\n\n_{review}_")
                        else:
                            st.write("Sem review na lista.")
                            
                        st.link_button("Ver no Letterboxd", link_final)

                else:
                    st.error("Não encontrei os itens <article>. O Letterboxd pode ter mudado o layout ou bloqueado o acesso.")
            else:
                st.error(f"Erro {response.status_code}: O site recusou a conexão.")
                
        except Exception as e:
            st.error(f"Erro técnico: {e}")
