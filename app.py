                    # 1. Título
                    elemento_titulo = filme_escolhido.find("h2", class_="name")
                    nome_filme = elemento_titulo.text.strip() if elemento_titulo else "Sem Título"

                    # 2. Imagem (Correção para encontrar a capa certa)
                    imagem_capa = ""
                    div_poster = filme_escolhido.find("div", class_="poster")
                    
                    if div_poster:
                        img_tag = div_poster.find("img")
                        if img_tag:
                            imagem_capa = img_tag.get('src') or img_tag.get('data-src')

                    # Se mesmo assim não achou ou a URL for relativa (começar com /), ajustamos
                    if imagem_capa and imagem_capa.startswith("/"):
                        imagem_capa = "https://letterboxd.com" + imagem_capa
                    
                    # Se não achou nada, usamos uma imagem genérica
                    if not imagem_capa:
                        imagem_capa = "https://s.ltrbxd.com/static/img/empty-poster-70.png"

                    # 3. Link
                    div_figure = filme_escolhido.find("div", class_="react-component")
                    if div_figure and div_figure.get('data-target-link'):
                        link_filme = "https://letterboxd.com" + div_figure['data-target-link']
                    else:
                        link_a = filme_escolhido.find("a")
                        link_filme = "https://letterboxd.com" + link_a['href'] if link_a else "#"

                    # 4. Comentário
                    comentario = ""
                    elemento_texto = filme_escolhido.find("div", class_="body-text")
                    if elemento_texto:
                        comentario = elemento_texto.text.strip()
