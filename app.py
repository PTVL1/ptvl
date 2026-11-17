import re
import math
import random
from collections import Counter

import streamlit as st

from pathlib import Path
import importlib
import ui
from calculators import calculate, harmony, HARMONIES

# Refresh the visual module when the running app reloads after a design edit.
importlib.reload(ui)
from ui import mount, introduction, footer, lab_image

st.set_page_config(page_title="Prisma · Laboratório Multimédia", page_icon=str(Path(__file__).parent / "assets" / "favicon.svg"), layout="wide")
mount()
if st.query_params.get("pagina", "inicio") != "inicio":
    st.caption("PRISMA / 404")
    st.title("Página não encontrada")
    st.write("O endereço não corresponde a uma página deste laboratório.")
    if st.button("Voltar ao laboratório"):
        st.query_params.clear()
        st.rerun()
    st.stop()
introduction()
st.html('<div id="ferramentas"></div>')
poesia, formatos, jogo, tipografia = st.tabs(["01 · Poesia", "02 · Imagem & cor", "03 · Quiz", "04 · Tipografia"])

SINONIMOS = {"amor": ["afeto", "ternura", "paixão"], "mar": ["oceano", "imensidão", "azul"], "luz": ["claridade", "fulgor", "brilho"], "noite": ["escuridão", "sombra", "breu"], "vida": ["existência", "jornada", "caminho"], "sonho": ["devaneio", "desejo", "utopia"], "triste": ["melancólico", "saudoso", "sombrio"], "feliz": ["radiante", "contente", "jubiloso"]}
STOPWORDS = set("a o as os de da do das dos e em um uma que com por para no na nos nas é se ao à".split())


def dimension_input(container, label, default, key, maximum=32768):
    """Evaluate a dimension on Enter, retaining the last valid size on errors."""
    st.session_state.setdefault(key, str(default))
    st.session_state.setdefault(key + "_valid", default)

    def commit():
        try:
            value = calculate(st.session_state[key].strip())
            if value != int(value) or not 1 <= value <= maximum:
                raise ValueError()
            st.session_state[key + "_valid"] = int(value)
            st.session_state[key] = str(int(value))
            st.session_state.pop(key + "_error", None)
        except (ValueError, SyntaxError, ZeroDivisionError, OverflowError, RecursionError):
            st.session_state[key + "_error"] = f"Usa uma conta com resultado inteiro entre 1 e {maximum} px. Mantido o último valor válido."

    container.text_input(label, key=key, on_change=commit)
    if key + "_error" in st.session_state:
        container.error(st.session_state[key + "_error"])
    return st.session_state[key + "_valid"]

with poesia:
    lab_image("poesia")
    st.header("Dá outra dimensão às palavras")
    texto = st.text_area("Escreve ou cola um poema", "No mar encontro a luz,\nNa luz encontro um sonho.\nO sonho leva a vida,\nE a vida traz o amor.", height=180, max_chars=20000)
    palavras = re.findall(r"[^\W\d_]+", texto.lower(), re.UNICODE)
    linhas = [linha for linha in texto.splitlines() if linha.strip()]
    a, b, c = st.columns(3)
    a.metric("Palavras", len(palavras))
    b.metric("Versos", len(linhas))
    c.metric("Palavras diferentes", len(set(palavras)))
    excluir = st.checkbox("Excluir palavras comuns", value=True)
    personalizadas = st.text_area("Stopwords — palavras a excluir", placeholder="Por exemplo: mar, sonho, luz", help="Separa as palavras com espaços, vírgulas ou novas linhas.", key="stopwords", max_chars=5000)
    bloqueadas = set(re.findall(r"[^\W\d_]+", personalizadas.lower(), re.UNICODE))
    if excluir:
        bloqueadas |= STOPWORDS
    st.subheader("Personaliza a nuvem")
    dimensoes = st.columns(2)
    nuvem_largura = dimension_input(dimensoes[0], "Largura da nuvem (px)", 1200, "nuvem_largura", 2048)
    nuvem_altura = dimension_input(dimensoes[1], "Altura da nuvem (px)", 430, "nuvem_altura", 2048)
    cor = st.color_picker("Cor das palavras", "#914C51")
    fundo_ativo = st.checkbox("Adicionar fundo", value=False)
    fundo_cor, fundo_imagem = None, None
    if fundo_ativo:
        fundo_cor = st.color_picker("Cor de fundo", "#FCE5D9")
        fundo_imagem = st.file_uploader("Imagem de fundo (opcional)", type=["png", "jpg", "jpeg"], help="A imagem será recortada para preencher as dimensões da nuvem.")
    else:
        st.caption("O PNG será exportado com fundo transparente.")
    limite = st.slider("Máximo de palavras na nuvem", 5, 60, 30)
    frequencias = Counter(p for p in palavras if p not in bloqueadas)
    if frequencias:
        from cloud_renderer import render_cloud
        from PIL import Image, UnidentifiedImageError
        import hashlib

        photo = fundo_imagem.getvalue() if fundo_imagem is not None else None
        signature = (tuple(frequencias.items()), nuvem_largura, nuvem_altura, cor, limite, fundo_cor,
                     hashlib.sha256(photo).hexdigest() if photo else None)
        previous = st.session_state.get("cloud_result")
        try:
            if previous is None or previous[0] != signature:
                with st.spinner("A preparar a nuvem de palavras…"):
                    png = render_cloud(frequencias, nuvem_largura, nuvem_altura, cor, limite, fundo_cor, photo)
                st.session_state["cloud_result"] = (signature, png)
            else:
                png = previous[1]
            st.image(png, caption="O tamanho de cada palavra representa a sua frequência.")
            st.download_button("Descarregar nuvem PNG", png, "nuvem.png", "image/png")
        except MemoryError:
            st.session_state.pop("cloud_result", None)
            st.error("Não há memória disponível para gerar esta nuvem. Reduz as dimensões ou remove a imagem de fundo e tenta novamente. Os outros widgets continuam disponíveis.")
        except (ValueError, UnidentifiedImageError, OSError, Image.DecompressionBombError):
            st.error("Não foi possível gerar a nuvem. Aumenta as dimensões se as palavras não couberem ou escolhe uma imagem de fundo até 16 megapíxeis.")
        with st.expander("Ver frequências"):
            st.dataframe([{"Palavra": p, "Ocorrências": n} for p, n in frequencias.most_common()], hide_index=True)
    else:
        st.info("Introduz algumas palavras para criar a nuvem.")
    st.subheader("Inspiração poética")
    st.caption("Dicionário local criado com apoio de IA. As sugestões dependem do contexto; não existe ligação a um modelo de IA.")
    termo = st.text_input("Palavra a explorar", "luz").strip().lower()
    if termo in SINONIMOS:
        st.success(" · ".join(SINONIMOS[termo]))
    elif termo:
        st.info("Ainda não há sugestões para esta palavra. Experimenta amor, mar, luz, noite, vida, sonho, triste ou feliz.")

with formatos:
    lab_image("imagem")
    st.header("Cada imagem tem a sua medida")
    st.subheader("Resolução da imagem")
    st.caption("Escreve um valor ou uma conta na largura e na altura e prime Enter. Por exemplo: 1920/2 passa a 960.")
    a, b = st.columns(2)
    largura = dimension_input(a, "Largura (px)", 1920, "imagem_largura")
    altura = dimension_input(b, "Altura (px)", 1080, "imagem_altura")
    divisor = math.gcd(largura, altura)
    padroes = {(1280, 720): "HD", (1920, 1080): "Full HD", (3840, 2160): "4K UHD"}
    a, b, c = st.columns(3)
    a.metric("Proporção exata", f"{largura // divisor}:{altura // divisor}")
    b.metric("Resolução", padroes.get((largura, altura), "Personalizada"))
    c.metric("Megapíxeis", f"{largura * altura / 1_000_000:.2f}")
    st.caption("HD, Full HD e 4K UHD são reconhecidos pelas dimensões horizontais exatas indicadas acima.")
    st.subheader("Calculador de proporções")
    proporcao = st.selectbox("Formato pretendido", ["16:9", "4:3", "1:1", "9:16"])
    x, y = map(int, proporcao.split(":"))
    nova_largura = dimension_input(st, "Nova largura (px)", 1280, "nova_largura")
    st.info(f"Dimensões sugeridas: {nova_largura} × {round(nova_largura * y / x)} px (altura arredondada).")
    st.subheader("Constrói a tua paleta")
    st.caption("Experimenta uma harmonia de cores ou ajusta as quatro amostras manualmente.")
    base = st.color_picker("Cor de base", "#237664")
    esquema = st.selectbox("Harmonia de cores", list(HARMONIES))
    sugestoes, explicacao = harmony(base, esquema)
    st.write(explicacao)
    st.caption("Cálculo no círculo de matizes RGB/HSL. Cores neutras mantêm-se neutras; escolhe uma base saturada para explorar as harmonias.")
    amostras = st.columns(len(sugestoes))
    for coluna, hex_cor in zip(amostras, sugestoes):
        coluna.html(f'<div class="color-swatch" style="background:{hex_cor}" role="img" aria-label="Amostra {hex_cor}"></div>')
        coluna.code(hex_cor, language=None)
    st.download_button("Guardar harmonia", "\n".join(sugestoes), "harmonia.txt", "text/plain")
    if st.button("Usar harmonia na paleta"):
        for i in range(4):
            st.session_state[f"paleta_{i}"] = sugestoes[i % len(sugestoes)]
    cols = st.columns(4)
    cores = []
    for i, (col, valor) in enumerate(zip(cols, ["#21675E", "#133B46", "#C7A66B", "#F6F4EF"])):
        st.session_state.setdefault(f"paleta_{i}", valor)
        cores.append(col.color_picker(f"Cor {i + 1}", key=f"paleta_{i}"))
    st.code(" | ".join(cores), language=None)
    st.download_button("Guardar paleta", "\n".join(cores), "paleta.txt", "text/plain")

PERGUNTAS = [
    ("Qual é a resolução Full HD?", ["1280 × 720", "1920 × 1080", "3840 × 2160"], 1, "A largura é próxima de dois mil píxeis.", "Full HD corresponde a 1920 × 1080 píxeis."),
    ("Qual é a proporção de uma imagem quadrada?", ["16:9", "4:3", "1:1"], 2, "Um quadrado tem largura e altura iguais.", "Na proporção 1:1, a largura é igual à altura."),
    ("Que formato suporta transparência?", ["JPEG", "PNG", "TXT"], 1, "É um formato de imagem muito usado em logótipos.", "PNG suporta um canal de transparência."),
    ("Quantos símbolos tem a parte numérica de uma cor #RRGGBB?", ["3", "6", "8"], 1, "São dois símbolos por cada um dos três canais de cor.", "RRGGBB tem seis símbolos hexadecimais."),
    ("Em Python, o que permite repetir instruções?", ["Um ciclo for", "Uma string", "Um comentário"], 0, "Pensa numa estrutura que percorre uma lista.", "Um ciclo for repete instruções para os elementos de uma sequência."),
    ("O que significa RGB?", ["Red, Green, Blue", "Resolução Gráfica Base", "Red, Grey, Black"], 0, "São três canais de luz.", "RGB significa vermelho, verde e azul: os canais usados nos ecrãs."),
    ("Qual destas cores hexadecimais é branca?", ["#000000", "#FFFFFF", "#FF0000"], 1, "Cada canal está no seu valor máximo.", "#FFFFFF tem os três canais RGB no valor máximo."),
    ("Que harmonia usa cores opostas no círculo de matizes?", ["Análoga", "Monocromática", "Complementar"], 2, "As cores ficam separadas por meia volta.", "Uma harmonia complementar usa matizes separados por 180°."),
    ("O que acontece ao duplicar largura e altura?", ["O número de píxeis duplica", "O número de píxeis quadruplica", "O número de píxeis mantém-se"], 1, "Multiplica os dois fatores: 2 × 2.", "O total de píxeis é largura × altura; duplicar ambas quadruplica o total."),
    ("Qual é um formato de imagem vetorial?", ["JPEG", "PNG", "SVG"], 2, "Este formato descreve formas e caminhos.", "SVG descreve formas vetoriais que podem ser ampliadas sem pixelização."),
    ("O que mede a taxa de fotogramas?", ["Imagens por segundo", "Cores por píxel", "Píxeis por linha"], 0, "É normalmente indicada em fps.", "A taxa de fotogramas indica quantas imagens são apresentadas por segundo."),
    ("Que formato é usado para áudio?", ["MP3", "PNG", "SVG"], 0, "É comum em ficheiros de música.", "MP3 é um formato de áudio comprimido."),
    ("Qual é a proporção de 1080 × 1920 píxeis?", ["16:9", "9:16", "1:1"], 1, "A imagem é mais alta do que larga.", "1080:1920 simplifica-se para 9:16, um formato vertical."),
    ("Em Python, qual destas opções é uma lista?", ['"azul"', '["azul", "verde"]', '42'], 1, "Procura os parênteses retos.", "Uma lista usa parênteses retos e pode guardar vários elementos."),
    ("Qual é o resultado de (2 + 3) * 4?", ["14", "20", "24"], 1, "Resolve primeiro o que está entre parênteses.", "Primeiro 2 + 3 = 5, depois 5 × 4 = 20."),
    ("Que harmonia usa uma só matiz com variações de luminosidade?", ["Triádica", "Complementar", "Monocromática"], 2, "O nome começa por mono: um só.", "Uma paleta monocromática explora claros e escuros da mesma matiz."),
    ("Para que serve o texto alternativo numa imagem?", ["Aumentar a resolução", "Descrever a imagem a quem não a vê", "Reduzir o tamanho do ficheiro"], 1, "Pensa em leitores de ecrã.", "O texto alternativo comunica o conteúdo da imagem a quem não a consegue ver."),
    ("Qual destes é um formato de vídeo?", ["TXT", "WAV", "MP4"], 2, "Pode conter imagens em movimento e áudio.", "MP4 é um formato de contentor frequentemente usado para vídeo e áudio."),
    ("Em Python, o que representa uma string?", ["Texto", "Um ciclo", "Uma imagem vetorial"], 0, "Pode ser escrita entre aspas.", "Uma string é uma sequência de caracteres, usada para representar texto."),
    ("Qual é a resolução 4K UHD?", ["1920 × 1080", "3840 × 2160", "1280 × 720"], 1, "Tem o dobro da largura e da altura de Full HD.", "4K UHD tem 3840 × 2160 píxeis: quatro vezes o total de Full HD."),
]

@st.dialog("Iniciar um novo quiz?")
def confirmar_reinicio():
    st.write("A pontuação atual será substituída. O novo quiz terá outra ordem de perguntas.")
    esquerda, direita = st.columns(2)
    if esquerda.button("Cancelar"):
        st.rerun()
    if direita.button("Iniciar novo quiz", type="primary"):
        for chave in list(st.session_state):
            if chave in {"ordem", "indice", "pontos", "tentativas", "respondida"} or chave.startswith("resposta_"):
                del st.session_state[chave]
        st.rerun()

with jogo:
    lab_image("quiz")
    st.header("Testa o teu olhar multimédia")
    st.caption("Perguntas e dicas preparadas com apoio de IA. O feedback adapta-se ao número de tentativas através de regras Python.")
    if "ordem" not in st.session_state or len(st.session_state.ordem) != len(PERGUNTAS):
        st.session_state.ordem = random.sample(range(len(PERGUNTAS)), len(PERGUNTAS))
        st.session_state.indice = 0
        st.session_state.pontos = 0
        st.session_state.tentativas = 0
        st.session_state.respondida = False
    estado = st.session_state
    st.progress(estado.indice / len(PERGUNTAS))
    if estado.indice < len(PERGUNTAS):
        pergunta, opcoes, correta, dica, explicacao = PERGUNTAS[estado.ordem[estado.indice]]
        st.caption(f"Pergunta {estado.indice + 1} de {len(PERGUNTAS)} · {estado.pontos} pontos")
        st.subheader(pergunta)
        escolha = st.radio("Escolhe uma resposta", opcoes, index=None, key=f"resposta_{estado.indice}", disabled=estado.respondida)
        if st.button("Verificar", disabled=estado.respondida):
            if escolha is None:
                st.warning("Seleciona uma resposta primeiro.")
            elif escolha == opcoes[correta]:
                estado.pontos += max(1, 3 - estado.tentativas)
                estado.respondida = True
                st.rerun()
            else:
                estado.tentativas += 1
        if estado.respondida:
            st.success("Excelente! " + explicacao)
            if st.button("Continuar"):
                estado.indice += 1
                estado.tentativas = 0
                estado.respondida = False
                st.rerun()
        elif estado.tentativas:
            st.warning(("Boa tentativa! " if estado.tentativas == 1 else "Continua, estás a aprender! ") + dica)
            if estado.tentativas >= 2:
                st.info(explicacao)
    else:
        st.success(f"Quiz concluído! Conseguiste {estado.pontos} de {len(PERGUNTAS) * 3} pontos.")
        if st.button("Jogar novamente"):
            confirmar_reinicio()

with tipografia:
    import typography_lab
    importlib.reload(typography_lab)
    pending = st.session_state.pop("type_pair_pending", None)
    if pending:
        st.session_state["type_0_heading"], st.session_state["type_0_body"] = pending
    typography_lab.render()

footer()
