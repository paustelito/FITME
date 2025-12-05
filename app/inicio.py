import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# configuración de página
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Dashboard Logística"
)

st.title("Resumen")

# cargar los datos
@st.cache_data # esto hace que la app sea rápida
def load_data():
    df_var = pd.read_csv('../data/inicio/datos_variabilidad_final.csv') 
    df_full = pd.read_csv('../data/inicio/datos_ralenti_diario.csv')
    
    # ponemos lo del formato de fechas 
    df_full['Fecha'] = pd.to_datetime(df_full['Fecha'])
    return df_var, df_full

df_var, df_full = load_data()

# métricas de Variabilidad
df_var['mean_time_safe'] = df_var['mean_time'].replace(0, np.nan)
df_var['CV'] = df_var['std_time'] / df_var['mean_time_safe']
umbral_critico = df_var['CV'].quantile(0.85)
df_var['Es_Critica'] = df_var['CV'] > umbral_critico

total_rutas = len(df_var)
rutas_criticas = df_var['Es_Critica'].sum()
kpi_pct_criticas = (rutas_criticas / total_rutas) * 100
kpi_variabilidad_promedio = df_var['CV'].mean()
kpi_buffer_promedio = df_var['buffer_recomendado'].mean()

# métricas de ralentí
proyeccion_total = df_full['ralenti_h_sim'].sum()
realidad_total = df_full['ralenti_total_h'].sum()
ahorro_horas = proyeccion_total - realidad_total
pct_reduccion = (ahorro_horas / proyeccion_total) * 100


# dashboard
st.markdown("### KEY INSIGHTS")

# key cards
st.markdown("#### Diagnóstico de Rutas y Variabilidad")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="% Rutas Críticas",
        value=f"{kpi_pct_criticas:.1f}%",
        delta=f"{rutas_criticas} rutas totales",
        delta_color="inverse" 
    )
    st.caption(f"Criterio: CV > {umbral_critico:.2f}")

with col2:
    st.metric(
        label="Variabilidad Promedio (CV)",
        value=f"{kpi_variabilidad_promedio:.2f}",
        help="Cercano a 0.5 indica alta inestabilidad."
    )

with col3:
    st.metric(
        label="Tiempo Buffer Promedio",
        value=f"{kpi_buffer_promedio:.1f} min",
        delta="Recomendado por viaje",
        delta_color="normal"
    )

st.divider() # linea para dividir

st.markdown("#### Impacto Ralentí")
col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        label="Ralentí Real",
        value=f"{realidad_total:,.0f} h",
        delta=f"-{ahorro_horas:,.0f} h vs Proyección",
        delta_color="normal" # verde porque bajar es bueno
    )

with col5:
    st.metric(
        label="Línea Base (Proyectado)",
        value=f"{proyeccion_total:,.0f} h"
    )

with col6:
    st.metric(
        label="% Reducción Global",
        value=f"{pct_reduccion:.2f}%",
        help="Ahorro logrado vs la proyección base."
    )

# gráficas

st.divider()
st.subheader("Gráficos")

tab1, tab2 = st.tabs(["Evolución del Ahorro", "Distribución de Variabilidad"])

# layout de ploty
layout_config = dict(
    paper_bgcolor='#272B40',
    plot_bgcolor='#272B40',
    font=dict(color='#F2F2F2'),
    xaxis=dict(showgrid=True, gridcolor='rgba(242, 242, 242, 0.1)'), 
    yaxis=dict(showgrid=True, gridcolor='rgba(242, 242, 242, 0.1)'),
    margin=dict(l=20, r=20, t=40, b=20)
)

with tab1:
    # GRÁFICA 1: REAL VS PROYECCIÓN 
    fig1 = go.Figure()

    # Línea Proyección 
    fig1.add_trace(go.Scatter(
        x=df_full['Fecha'], 
        y=df_full['ralenti_h_sim'],
        mode='lines',
        name='Proyección Base',
        line=dict(color='#F29F8D', dash='dash')
    ))

    # Línea Real 
    fig1.add_trace(go.Scatter(
        x=df_full['Fecha'], 
        y=df_full['ralenti_total_h'],
        mode='lines',
        name='Ralentí Real',
        line=dict(color='#F24B0F', width=3),
        fill='tonexty', 
        fillcolor='rgba(242, 75, 15, 0.2)' 
    ))

    fig1.update_layout(
        title='Desempeño Diario: Real vs. Proyección',
        **layout_config
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    # GRÁFICA 2: HISTOGRAMA DE VARIABILIDAD
    fig2 = px.histogram(
        df_var, 
        x="CV", 
        nbins=30,
        color_discrete_sequence=['#F24B0F'],
        title='Distribución de Variabilidad por Ruta'
    )

    # Línea Vertical Umbral 
    fig2.add_vline(
        x=umbral_critico, 
        line_dash="dash", 
        line_color="#F29F8D",
        annotation_text=f"Umbral: {umbral_critico:.2f}", 
        annotation_position="top right",
        annotation_font_color="#F29F8D"
    )

    fig2.update_layout(**layout_config)
    fig2.update_xaxes(title_text='Coeficiente de Variación (CV)')
    fig2.update_yaxes(title_text='Cantidad de Rutas')

    st.plotly_chart(fig2, use_container_width=True)