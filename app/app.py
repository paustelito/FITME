import streamlit as st

# Config básica de la página
st.set_page_config(
    page_title="MAYAB-METRICS",
    page_icon="./public/images/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de estilos CSS
def load_css():
    with open("public/styles/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Páginas del sidebar
inicio = st.Page("inicio.py", title="Resumen")
rutas = st.Page("rutas.py", title="Rutas")
unidades = st.Page("unidades.py", title="Unidades")
demanda = st.Page("demanda.py", title="Demanda")

# Navegación entre páginas
pg = st.navigation([
    inicio,
    rutas,
    unidades,
    demanda,
])

pg.run()