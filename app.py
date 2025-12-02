import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

# Configuração da página para ficar bonitinha na aba do navegador
st.set_page_config(page_title="Sorteador Letterboxd", page_icon="🎬")

# Cabeçalho
st.title("🎬 Sorteador de Filmes")
st.write("Não sabe o que assistir? Cola o link da sua lista do Letterboxd aí embaixo que eu escolho pra você.")

# Entrada de dados
url_lista = st.text_input("URL da Lista (pública)", placeholder="https://letterboxd.com/seu_user/list/sua-lista/")

if st.button("Sortear Filme"):
    if not url_lista:
        st.warning("Opa, esqueceu de colar o link!")
    else:
        try:
            # Fingimos ser um navegador real para o site não bloquear a gente
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url_lista, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # --- LÓGICA DE BUSCA ---
                # Tenta primeiro o modo "Detalhado" (que você usa)
                filmes = soup.find_all("article", class_="list-detailed-entry")
                
                # Se não achar, tenta o modo "Grade" (padrão do site)
                if not filmes:
                    filmes = soup.find_all("li", class_="poster-container")

                if filmes:
                    # O Sorteio
                    total_filmes = len(filmes)
                    numero_sorteado = random.randint(0, total_filmes - 1)
                    filme_escolhido = filmes[numero_sorteado]
                    
                    # --- EXTRAÇÃO DOS DADOS ---
                    
                    # 1. Título
                    elemento_titulo = filme_escolhido.find("h2", class_="name")
                    if elemento_titulo:
                        nome_filme = elemento_titulo.text.strip()
                    else:
                        # Fallback para o modo grade, onde o titulo fica na imagem
                        img_alt = filme_escolhido.find("img")
                        nome_filme = img_alt['alt'] if img_alt else "Filme Misterioso"

                    # 2. Imagem (Agora vai!)
                    imagem_capa = ""
                    # Procura a div especifica do poster para não pegar avatar de usuário errado
                    div_poster = filme_escolhido.find("div", class_="poster")
                    if div_poster:
                        img_tag = div_poster.find("img")
                        if img_tag:
                            imagem_capa = img_tag.get('src')
                    
                    # Se falhar, tenta pegar direto do article (modo grade)
                    if not imagem_capa:
                        img_tag = filme_escolhido.find("img")
                        if img_tag:
                            imagem_capa = img_tag.get('src')

                    # 3. Link do filme
                    div_figure = filme_escolhido.find("div", class_="react-component")
                    if div_figure and div_figure.get('data-target-link'):
                        link_filme = "https://letterboxd.com" + div_figure['data-target-link']
                    else:
                        link_tag = filme_escolhido.find("a")
                        link_filme = "https://letterboxd.com" + link_tag['href'] if link_tag else "#"

                    # 4. Seu comentário (se existir)
                    comentario = ""
                    elemento_texto = filme_escolhido.find("div", class_="body-text")
                    if elemento_texto:
                        comentario = elemento_texto.text.strip()

                    # --- MOSTRAR NA TELA ---
                    st.divider()
                    st.success(f"🎲 O dado rolou e caiu no número: **{numero_sorteado + 1}**")
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        if imagem_capa:
                            st.image(imagem_capa, use_container_width=True)
                        else:
                            st.text("🚫 Sem capa")
                    
                    with col2:
                        st.header(nome_filme)
                        if comentario:
                            st.info(f"📝 **Sua nota:** \"{comentario}\"")
                        else:
                            st.write("_Sem comentários nesta lista._")
                            
                        st.link_button("Ver no Letterboxd", link_filme)
                    
                else:
                    st.error("Não achei nenhum filme! Certeza que a lista é pública?")
            else:
                st.error(f"Erro ao acessar o Letterboxd (Status: {response.status_code})")
        except Exception as e:
            st.error(f"Deu ruim no código: {e}")
