import streamlit as st
import requests

# Catálogo de Livros
# Aplicação feita com Streamlit consumindo a API pública da Open Library

st.title("📚 Catálogo de Livros")

st.write("Busque livros por título, autor ou assunto usando a API pública da Open Library.")

tipo_busca = st.selectbox(
    "Escolha o tipo de busca:",
    ["Título", "Autor", "Assunto"]
)

termo = st.text_input("Digite o termo de busca:")

quantidade = st.slider(
    "Quantidade de resultados:",
    1, 20, 5
)

if st.button("Buscar"):

    if termo == "":
        st.warning("Digite algo para buscar.")

    else:
        if tipo_busca == "Título":
            parametro = "title"
        elif tipo_busca == "Autor":
            parametro = "author"
        else:
            parametro = "subject"

        url = "https://openlibrary.org/search.json"

        parametros = {
            parametro: termo,
            "limit": quantidade
        }

        try:
            resposta = requests.get(url, params=parametros)
            dados = resposta.json()

            livros = dados["docs"]

            st.subheader("Resultados encontrados")

            if len(livros) == 0:
                st.info("Nenhum livro foi encontrado.")

            for livro in livros:
                titulo = livro.get("title", "Título não informado")
                autores = livro.get("author_name", ["Autor não informado"])
                ano = livro.get("first_publish_year", "Ano não informado")
                edicoes = livro.get("edition_count", "Não informado")
                capa_id = livro.get("cover_i")

                st.markdown("---")
                st.markdown(f"### {titulo}")
                st.write(f"**Autor(es):** {', '.join(autores[:3])}")
                st.write(f"**Primeiro ano de publicação:** {ano}")
                st.write(f"**Quantidade de edições:** {edicoes}")

                if capa_id:
                    link_capa = f"https://covers.openlibrary.org/b/id/{capa_id}-M.jpg"
                    st.image(link_capa, width=120)
                else:
                    st.write("Capa não disponível.")

        except:
            st.error("Ocorreu um erro ao buscar os dados da API.")
