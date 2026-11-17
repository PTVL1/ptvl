# Publicar o Prisma

## 1. Extrair o ZIP

Clica com o botão direito em `Prisma-GitHub.zip` e escolhe **Extrair tudo**. Publica os ficheiros extraídos, não o ZIP.

## 2. Colocar no GitHub

1. Entra em https://github.com e escolhe **New repository**.
2. Dá-lhe o nome `prisma-multimedia`. Para partilhar o código com o docente, podes escolher **Public**.
3. Cria o repositório. No repositório vazio, escolhe **uploading an existing file**; num repositório existente, usa **Add file → Upload files**.
4. Arrasta o conteúdo da pasta extraída para a área de upload, incluindo as pastas `assets` e `.streamlit`. No Explorador do Windows, ativa **Ver → Mostrar → Itens ocultos** se não vires os ficheiros que começam por ponto.
5. Confirma as alterações com **Commit changes**.

`app.py` e `requirements.txt` devem aparecer diretamente na raiz do repositório. Não os coloques numa pasta adicional chamada Prisma-GitHub. Mantém `assets` e `.streamlit` como pastas e não alteres os nomes dos ficheiros.

Estrutura principal:

```text
app.py
ui.py
calculators.py
cloud_renderer.py
typography_lab.py
requirements.txt
README.md
PUBLICAR.md
.gitignore
.streamlit/
    config.toml
assets/
    style.css
    navigation.html
    favicon.svg
    imagem.svg
    poesia.svg
    quiz.svg
    tipografia.svg
    spectrum.svg
```

O ZIP também inclui os testes e os atalhos de execução local. O ambiente `.venv` não é necessário no GitHub nem no Streamlit Cloud.

## 3. Publicar a aplicação no Streamlit Community Cloud

1. Entra em https://share.streamlit.io e associa a tua conta GitHub.
2. Escolhe **Create app** e seleciona a opção de publicar a partir do GitHub, se aparecer.
3. Seleciona o repositório `prisma-multimedia`, a branch que contém os ficheiros (normalmente `main`) e **Main file path: `app.py`**.
4. Escolhe o endereço da aplicação, se quiseres, e clica em **Deploy**.
5. Espera pela instalação das dependências e guarda o endereço terminado em `.streamlit.app`.

O GitHub guarda o código; o Streamlit Cloud executa a aplicação. GitHub Pages não executa esta aplicação Python. Depois de publicar, o endereço Streamlit funciona sem manter o teu computador ou a janela do terminal ligados.

## 4. Entregar e verificar

- Abre os quatro separadores e confirma que as imagens aparecem.
- Na largura de Imagem & cor, escreve `1920/2` e prime Enter: deve ficar `960`.
- Descarrega uma nuvem de palavras e aplica uma harmonia de cores.
- Confirma as perguntas do quiz e a comparação de tipografia.
- Partilha com o docente o endereço do repositório e o endereço público do Streamlit.

Se aparecer `ModuleNotFoundError`, confirma que todos os ficheiros `.py` e `requirements.txt` estão na raiz. Se faltarem estilos ou imagens, confirma que as pastas `assets` e `.streamlit` foram enviadas com os seus conteúdos.

Documentação oficial:
- https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
