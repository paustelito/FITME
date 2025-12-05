import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.title("Gestiona tu demanda")


# --- 1. CARGA DE DATOS (Silenciosa) ---
archivo_local = "mis_rutas_para_dashboard.csv"
df = None
modo_simulacion = False

# --- 1. CARGA DE DATOS (Silenciosa) ---
archivo_local = "mis_rutas_para_dashboard.csv"
df = None
modo_simulacion = False

# Intentar cargar archivo local automáticamente
if os.path.exists(archivo_local):
    try:
        df = pd.read_csv(archivo_local)
    except:
        pass

# Si no encontró el archivo, pasa directo a SIMULACIÓN
if df is None:
    modo_simulacion = True
    rutas_default = ['Mérida - Cancún', 'Mérida - Chetumal', 'Cancún - Tulum', 'Villahermosa - Mérida', 'Campeche - Mérida']
    datos_default = []
    np.random.seed(42) 
    for r in rutas_default:
        demanda = np.random.randint(50, 300)
        variabilidad = int(demanda * np.random.uniform(0.1, 0.5))
        # Simulamos tiempos (horas)
        tiempo_ideal = np.random.uniform(3, 8)
        variabilidad_tiempo = np.random.uniform(0.5, 2.0)
        
        datos_default.append({
            'Ruta': r,
            'Demanda Promedio': demanda,
            'Variabilidad': variabilidad,
            'Tiempo Ideal (h)': round(tiempo_ideal, 1),
            'Variabilidad Tiempo (h)': round(variabilidad_tiempo, 1)
        })
    df = pd.DataFrame(datos_default)
    st.caption("Visualizando datos de ejemplo.")

# --- 2. FILTROS ---
col_filtros, col_info = st.columns([1, 2])

with col_filtros:
    opcion_servicio = st.selectbox(
        "Nivel de Servicio Objetivo:",
        options=[
            "85% - Básico", 
            "90% - Estándar", 
            "95% - Alto (Recomendado)", 
            "98% - Crítico"
        ],
        index=2
    )
    servicio_objetivo = int(opcion_servicio.split("%")[0])

with col_info:
    if servicio_objetivo >= 98:
        st.warning(" Cobertura total: Requiere inventarios y tiempos de holgura altos.")
    elif servicio_objetivo <= 85:
        st.info(" Costo bajo: Mayor riesgo en tiempos y stock.")
    else:
        st.success("Balance óptimo.")

# --- 3. LÓGICA DE NEGOCIO ---
if df is not None:
    df.columns = [c.strip() for c in df.columns]

    # Detección de Columnas
    col_ruta = next((c for c in df.columns if 'ruta' in c.lower() or 'origen' in c.lower()), df.columns[0])
    
    # Lógica de Demanda (como antes)
    col_demanda = next((c for c in df.columns if 'demanda' in c.lower()), None)
    if col_demanda:
        df['Demanda_Final'] = df[col_demanda]
    else:
        df['Demanda_Final'] = df['Demanda Promedio'] if modo_simulacion else np.random.randint(50, 300, size=len(df))

    col_var = next((c for c in df.columns if 'std' in c.lower() or 'variabilidad' in c.lower()), None)
    if col_var:
        df['Variabilidad_Final'] = df[col_var]
    else:
        df['Variabilidad_Final'] = df['Variabilidad'] if modo_simulacion else df['Demanda_Final'] * 0.2

    # --- NUEVA LÓGICA: TIEMPOS ---
    # Buscamos columnas de tiempo, si no existen las simulamos
    if 'Tiempo Ideal (h)' not in df.columns:
        if not modo_simulacion:
             # Generar tiempos aleatorios si es archivo real sin tiempos
            df['Tiempo Ideal (h)'] = np.random.uniform(4, 10, size=len(df)).round(1)
            df['Variabilidad Tiempo (h)'] = np.random.uniform(0.5, 2.5, size=len(df)).round(1)
    
    # Calculamos el Tiempo Real Estimado (Ideal + Variabilidad promedio)
    df['Tiempo Real Promedio'] = df['Tiempo Ideal (h)'] + (df['Variabilidad Tiempo (h)'] * 0.5)

    # Cálculos de Buffer (Inventario)
    factor_z = {80: 0.84, 85: 1.04, 90: 1.28, 95: 1.65, 98: 2.05, 99: 2.33}
    z_score = factor_z.get(servicio_objetivo, 1.65)

    df['Buffer Sugerido'] = (df['Variabilidad_Final'] * z_score).astype(int)
    df['Inventario Total'] = df['Demanda_Final'] + df['Buffer Sugerido']
    df['Estado'] = np.where(df['Buffer Sugerido'] > df['Demanda_Final'] * 0.4, 'Revisar', 'OK')

    # --- 4. VISUALIZACIÓN ---

    # Pestañas para separar Demanda de Tiempos
    tab1, tab2 = st.tabs(["Inventario & Buffer", "Análisis de Tiempos"])

    with tab1:
        # (El gráfico de siempre)
        k1, k2 = st.columns(2)
        k1.metric("Inventario Total Sugerido", f"{df['Inventario Total'].sum():,.0f} uds")
        k2.metric("Rutas Críticas (Stock)", len(df[df['Estado'] == 'Revisar']), delta_color="inverse")
        
        st.subheader(f"Cobertura de Stock (Nivel {servicio_objetivo}%)")
        df_grafico = df.sort_values('Buffer Sugerido', ascending=False).head(10)
        fig = px.bar(
            df_grafico,
            x=col_ruta,
            y=['Demanda_Final', 'Buffer Sugerido'],
            labels={'value': 'Unidades', col_ruta: 'Ruta', 'variable': 'Componente'},
            color_discrete_map={'Demanda_Final': '#BDC3C7', 'Buffer Sugerido': '#E74C3C'},
            height=400
        )
        fig.update_layout(legend_title_text='') 
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # --- NUEVO: GRÁFICO DE TIEMPOS ---
        t1, t2 = st.columns(2)
        avg_ideal = df['Tiempo Ideal (h)'].mean()
        avg_real = df['Tiempo Real Promedio'].mean()
        delta_tiempo = ((avg_real - avg_ideal) / avg_ideal) * 100
        
        t1.metric("Tiempo Ideal Promedio", f"{avg_ideal:.1f} h")
        t2.metric("Desviación Promedio", f"+{delta_tiempo:.1f}%", delta_color="inverse")

        st.subheader("Tiempo Ideal vs. Variabilidad Real")
        st.markdown("La barra azul es el tiempo ideal. La **línea roja** muestra el rango de variabilidad (retrasos posibles).")

        # Gráfico avanzado con barras de error
        fig_time = go.Figure()

        # Barra base (Tiempo Ideal)
        fig_time.add_trace(go.Bar(
            x=df[col_ruta],
            y=df['Tiempo Ideal (h)'],
            name='Tiempo Ideal',
            marker_color='#2E86C1'
        ))

        # Añadimos la variabilidad como barras de error hacia arriba
        fig_time.add_trace(go.Scatter(
            x=df[col_ruta],
            y=df['Tiempo Ideal (h)'] + df['Variabilidad Tiempo (h)'],
            mode='markers',
            marker=dict(symbol='line-ns-open', size=20, color='red', line=dict(width=3)),
            name='Variabilidad Máxima'
        ))

        fig_time.update_layout(
            yaxis_title="Horas de Viaje",
            xaxis_title="Ruta",
            height=450,
            showlegend=True
        )
        st.plotly_chart(fig_time, use_container_width=True)

    # C. Tabla (Común)
    with st.expander("Ver tabla de datos detallada"):
        cols_mostrar = [col_ruta, 'Demanda_Final', 'Buffer Sugerido', 'Tiempo Ideal (h)', 'Variabilidad Tiempo (h)']
        st.dataframe(df[cols_mostrar], use_container_width=True, hide_index=True)