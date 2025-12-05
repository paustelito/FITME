import streamlit as st
import pandas as pd 

st.title("Conoce tus rutas") 
@st.cache_data(show_spinner=False)
def load_data():
    tabla_categorias = pd.read_csv("../data/tabla_categorias.csv")
    tabla_rutas_criticas= pd.read_csv("../data/tabla_rutas_criticas.csv")
    
    return tabla_categorias, tabla_rutas_criticas

tabla_categorias, tabla_rutas_criticas = load_data()

import matplotlib.pyplot as plt

st.subheader("Distribución de Rutas Críticas por Categoría")

# --- COLORES ---
azul_marino = "#001021"   # azul casi negro
naranja = "#ff7c43"

# Alternar colores: azul – naranja – azul – naranja…
colores = [azul_marino, naranja] * (len(tabla_rutas_criticas) // 2 + 1)
colores = colores[:len(tabla_rutas_criticas)]

# --- GRÁFICA ---
fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    tabla_rutas_criticas["Categoria_Oficial"],
    tabla_rutas_criticas["Numero_Rutas_Criticas"],
    color=colores
)

ax.set_xlabel("Categoría Oficial")
ax.set_ylabel("Número de Rutas Críticas")
ax.set_title("Distribución de Rutas Críticas por Categoría")
plt.xticks(rotation=45, ha="right")

st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    tabla_categorias

with col2:
    tabla_rutas_criticas