"""Visual system and progressive browser enhancements for the Streamlit dashboard."""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent


def mount():
    st.html((ROOT / "assets" / "style.css").read_text(encoding="utf-8"))
    # The embedded document belongs to this app; enhancements target its parent.
    components.html((ROOT / "assets" / "navigation.html").read_text(encoding="utf-8"), height=0)


def introduction():
    st.html('<div id="inicio"></div><p class="eyebrow">PRISMA / LABORATÓRIO MULTIMÉDIA</p>')
    st.title("Experimenta. Cria. Descobre.")
    st.markdown('<p class="intro">Transforma versos em imagens, brinca com cores, testa o que sabes e dá forma às letras. Escolhe um dos quatro laboratórios e começa a explorar.</p>', unsafe_allow_html=True)


def footer():
    st.divider()
    st.caption("PRISMA · Projeto educativo de programação e multimédia / Python + Streamlit")


def lab_image(name):
    st.image(str(ROOT / "assets" / f"{name}.svg"))
