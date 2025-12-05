import streamlit as st
import base64

# Config básica de la página
st.set_page_config(
    page_title="LOGIMAYAB DATA",
    page_icon="./public/images/favicon_orange.png",
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

# Logos
def img_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = img_to_base64("public/images/logo_clear.png")

st.sidebar.markdown(
    f"""
    <div class="sidebar-logo">
        <img src="data:image/png;base64,{logo_base64}" width={200}>
    </div>
    """,
    unsafe_allow_html=True
)

pg.run()