"""Visual system and progressive browser enhancements for the Streamlit dashboard."""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent


def asset_text(name):
    path = ROOT / "assets" / name
    if path.is_file():
        return path.read_text(encoding="utf-8")
    from bundled_assets import ASSETS
    return ASSETS[name]


def mount():
    st.html(asset_text("style.css"))
    # The embedded document belongs to this app; enhancements target its parent.
    components.html(asset_text("navigation.html"), height=0)


def introduction():
    st.html('<div id="inicio"></div><p class="eyebrow">PRISMA / LABORATÓRIO MULTIMÉDIA</p>')
    st.title("Experimenta. Cria. Descobre.")
    st.markdown('<p class="intro">Transforma versos em imagens, brinca com cores, testa o que sabes e dá forma às letras. Escolhe um dos quatro laboratórios e começa a explorar.</p>', unsafe_allow_html=True)


def footer():
    st.divider()
    st.caption("PRISMA · Projeto educativo de programação e multimédia / Python + Streamlit")


def lab_image(name):
    st.image(asset_text(f"{name}.svg"))
