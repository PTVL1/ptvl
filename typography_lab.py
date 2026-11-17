"""Interactive, local typography specimens and explained pairing suggestions."""
from html import escape
from ui import lab_image
import streamlit as st

FONTS = {
    "Arial · sem serifa": 'Arial, Helvetica, sans-serif',
    "Georgia · serifa": 'Georgia, "Times New Roman", serif',
    "Verdana · sem serifa": 'Verdana, Geneva, sans-serif',
    "Trebuchet · sem serifa": '"Trebuchet MS", Arial, sans-serif',
    "Times · serifa": '"Times New Roman", Times, serif',
    "Courier · monoespaçada": '"Courier New", Courier, monospace',
}
PAIRS = {
    "Artigo e leitura": ("Georgia · serifa", "Arial · sem serifa", "Uma serifa expressiva no título e uma sem serifa simples no corpo criam contraste sem competir."),
    "Cartaz de evento": ("Trebuchet · sem serifa", "Verdana · sem serifa", "Um título forte e um corpo com formas abertas ajudam a separar o anúncio dos detalhes."),
    "Poema e literatura": ("Times · serifa", "Georgia · serifa", "Duas serifas de tradição editorial. Distingue título e corpo pelo tamanho e pelo peso."),
    "Código e tecnologia": ("Arial · sem serifa", "Courier · monoespaçada", "O título dá hierarquia; o corpo monoespaçado evidencia o ritmo e o alinhamento dos caracteres."),
}


def specimen(title, text, settings):
    family, body_family, size, leading, tracking, wordspace, weight, italic, align, transform = settings
    css = f'font-family:{FONTS[body_family]};font-size:{size}px;line-height:{leading};letter-spacing:{tracking}px;word-spacing:{wordspace}px;font-weight:{weight};font-style:{"italic" if italic else "normal"};text-align:{align};text-transform:{transform};white-space:pre-wrap;overflow-wrap:anywhere'
    return f'<article class="type-specimen"><h3 style="font-family:{escape(FONTS[family], quote=True)}!important;font-size:{round(size*1.6)}px!important;line-height:1.15;font-weight:700">{escape(title)}</h3><div style=\'{css}\'>{escape(text)}</div></article>'


def render():
    lab_image("tipografia")
    st.header("As letras também têm personalidade")
    st.write("Compara duas composições com o mesmo texto. Muda uma variável de cada vez e observa o resultado.")
    title = st.text_input("Título da amostra", "Uma ideia ganha forma", key="type_title", max_chars=200)
    text = st.text_area("Texto para comparar", "Entre palavras e espaços, cada escolha muda a forma como lemos. Experimenta um ritmo mais calmo, um título mais forte ou uma combinação inesperada.", key="type_text", max_chars=5000)
    st.caption("Fontes locais: a aparência pode variar entre dispositivos; se uma fonte não existir, é usada uma alternativa da mesma família.")
    settings = []
    columns = st.columns(2)
    for index, col in enumerate(columns):
        key = f"type_{index}_"
        with col:
            st.subheader(f"Composição {'AB'[index]}")
            st.session_state.setdefault(key+"heading", list(FONTS)[index])
            st.session_state.setdefault(key+"body", list(FONTS)[1-index])
            heading = st.selectbox("Fonte do título", list(FONTS), key=key+"heading")
            body = st.selectbox("Fonte do texto", list(FONTS), key=key+"body")
            size = st.slider("Tamanho do texto (px)", 12, 48, 18, key=key+"size")
            leading = st.slider("Entrelinha", 1.0, 2.4, 1.6, .1, key=key+"leading")
            tracking = st.slider("Espaço entre letras (px)", -.5, 4.0, 0.0, .1, key=key+"tracking")
            wordspace = st.slider("Espaço entre palavras (px)", 0, 12, 0, key=key+"wordspace")
            weight = st.select_slider("Peso", [400, 500, 600, 700], value=400, key=key+"weight")
            italic = st.checkbox("Itálico", key=key+"italic")
            alignment = st.selectbox("Alinhamento", ["À esquerda", "Centrado", "À direita"], key=key+"align")
            upper = st.checkbox("Maiúsculas", key=key+"upper")
            settings.append((heading, body, size, leading, tracking, wordspace, weight, italic, {"À esquerda":"left", "Centrado":"center", "À direita":"right"}[alignment], "uppercase" if upper else "none"))
    st.subheader("Comparação lado a lado")
    for col, setting in zip(st.columns(2), settings):
        col.html(specimen(title, text, setting))
    st.subheader("Recomendações para o teu projeto")
    st.caption("Sugestões preparadas com apoio de IA e adaptadas por regras locais. Não são geradas por um modelo em tempo real.")
    purpose = st.selectbox("O que estás a criar?", list(PAIRS), key="type_purpose")
    heading, body, explanation = PAIRS[purpose]
    st.write(f"**Título:** {heading} · **Texto:** {body}")
    st.write(explanation)
    for index, setting in enumerate(settings):
        tips = []
        if setting[2] < 16:
            tips.append("Experimenta pelo menos 16 px para texto de leitura no ecrã.")
        if setting[3] < 1.4:
            tips.append("Aumenta a entrelinha para 1,4–1,7 e compara a facilidade de leitura.")
        if setting[4] > 1 or setting[9] == "uppercase":
            tips.append("Reserva as maiúsculas e o espaçamento largo para textos curtos.")
        if setting[0] == setting[1]:
            tips.append("A mesma fonte pode funcionar: distingue título e corpo pelo peso e tamanho.")
        if tips:
            st.info(f"Composição {'AB'[index]}: " + " ".join(tips))
    if st.button("Aplicar combinação à composição A", key="apply_type_pair"):
        st.session_state["type_pair_pending"] = (heading, body)
        st.rerun()
    html = '<!doctype html><html lang="pt"><meta charset="utf-8"><title>Estudo tipográfico Prisma</title><style>body{max-width:1100px;margin:40px auto;padding:24px;color:#243d43;background:#fffcf5}.type-specimen{padding:24px;border-bottom:1px solid #ccc}h3{margin-top:0}</style>' + ''.join(specimen(title, text, s) for s in settings) + '</html>'
    st.download_button("Guardar estudo tipográfico", html, "tipografia.html", "text/html", key="download_type")
