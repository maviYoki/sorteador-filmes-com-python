# 🎬 Sorteador de Filmes - Letterboxd

Fiz esse script num surto porque eu passava 2 horas escolhendo o filme e 0 horas assistindo. Ele pega uma lista do Letterboxd e chuta um filme aleatório pra você ver.

É gambiarra com Web Scraping, então se o Letterboxd mudar o layout do site amanhã, isso aqui provavelmente vai quebrar. Aproveite enquanto funciona.

## 🚀 Como usar (se o link estiver funcionando)

Não quer baixar nada? Só entra no link que vai estar na descrição e:

- Pega o link da sua lista (ou de qualquer lista pública).

- Cola lá na caixa.

- Clica no botão e aceita o destino.

## 💻 Rodando na sua máquina (caso o link caia)

Se o link acima cair ou se você quiser ver o código:

Clona:

```
git clone https://github.com/maviYoki/sorteador-filmes-com-python
cd sorteador-filmes-com-python
```

Instala as dependências (basicamente o Streamlit e o BeautifulSoup pra raspar o site):

```
pip install -r requirements.txt 
```

Roda o servidor:

```
streamlit run app.py
```

O navegador vai abrir sozinho. Se divirta :) .
