# app/unidades.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Unidades — Ralentí")
st.title("Asigna tus unidades")

@st.cache_data(show_spinner=False)
def load_data():
    df_compare = pd.read_csv("../data/unidades/df_compare.csv")
    sim_df = pd.read_csv("../data/unidades/sim_df.csv")
    matriz = pd.read_csv("../data/unidades/matriz_asignacion.csv", index_col=0)
    df_full = pd.read_csv("../data/unidades/df_full.csv")
    efecto_unidad = pd.read_csv("../data/unidades/efecto_por_unidad.csv")
    matriz_explained = pd.read_csv("../data/unidades/matriz_asignacion_explained.csv")

    # Confirmar tipos de datos
    df_compare["Fecha"] = pd.to_datetime(df_compare["Fecha"], errors="coerce")
    df_full["Fecha"] = pd.to_datetime(df_full["Fecha"], errors="coerce")
    sim_df["Fecha"] = pd.to_datetime(sim_df["Fecha"], errors="coerce")

    return df_compare, sim_df, matriz, efecto_unidad, df_full, matriz_explained

df_compare, sim_df, matriz, efecto_unidad, df_full, matriz_explained = load_data()

# Filtros
with st.sidebar:
    # Montar rango de fechas
    date_source = sim_df if not sim_df.empty else df_full
    min_date = date_source['Fecha'].min()
    max_date = date_source['Fecha'].max()
    if pd.isna(min_date) or pd.isna(max_date):
        # fallback to df_full
        min_date = df_full['Fecha'].min()
        max_date = df_full['Fecha'].max()

    # Cambiar a python dates para Streamlit
    try:
        date_default = (min_date.date(), max_date.date())
    except Exception:
        date_default = (pd.to_datetime(min_date).date(), pd.to_datetime(max_date).date())
    
    st.markdown("Opciones visuales")
    show_bars = st.checkbox("Mostrar barra de reasignación", value=True)
    show_sankey = st.checkbox("Mostrar Sankey", value=False)
    top_n_flows = st.slider("Top flujos para Sankey", min_value=5, max_value=50, value=25)

# KPIs
if 'ralenti_h_sim' in df_compare.columns:
    ralenti_antes = df_compare["ralenti_h_sim"].sum()
else:
    ralenti_antes = 0.0

if 'ralenti_total_h' in df_compare.columns:
    ralenti_despues = df_compare["ralenti_total_h"].sum()
else:
    ralenti_despues = 0.0

reduccion = ralenti_antes - ralenti_despues
pct = (reduccion / ralenti_antes * 100) if ralenti_antes != 0 else 0.0

k1, k2, k3 = st.columns(3)
k1.metric("Ralentí Antes (h)", f"{ralenti_antes:,.2f}")
k2.metric("Ralentí Después (h)", f"{ralenti_despues:,.2f}")
k3.metric("Reducción Total", f"{reduccion:,.2f} h", f"{pct:.2f}%")

st.markdown("---")

# Real vs Predicción
st.subheader("📈 Ralentí Real vs Predicción")
if 'pred' not in df_full.columns:
    st.warning("No se encontró columna 'pred' en model_predictions. Mostraré solo la serie real.")
    fig_real_pred = px.line(df_full, x="Fecha", y="ralenti_total_h", labels={'ralenti_total_h':'Horas de ralentí'})
else:
    fig_real_pred = px.line(df_full, x="Fecha", y=["ralenti_total_h", "pred"],
                            labels={"value": "Horas de ralentí", "variable": "Serie"},
                            title="Comparación Real vs Predicho")
fig_real_pred.update_layout(height=360, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig_real_pred, use_container_width=True)

st.markdown("---")

# Matriz / Tabla
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("Matriz de Reasignación")
    st.write("Filas = Unidad histórica (Old). Columnas = Unidad sugerida (New). Valores = número de rutas (o horas trasladadas).")
    pivot_fallback = sim_df.groupby(['OldUnidad','NewUnidad']).size().unstack(fill_value=0)
    st.dataframe(pivot_fallback.style.format("{:,.0f}"))

with col_right:
    st.subheader("Tabla Detallada por Unidad")
    st.dataframe(
        matriz_explained,
        use_container_width=True,
        hide_index=True
    )


st.subheader("Efecto por Unidad")
# Asegurar efecto_unidad tiene datos
if isinstance(efecto_unidad, pd.DataFrame) and not efecto_unidad.empty:
    ef = efecto_unidad.copy()
else:
    # fallback
    antes_u = sim_df.groupby('OldUnidad', as_index=False)['ruta_ralenti_est_h'].sum().rename(columns={'OldUnidad':'Unidad','ruta_ralenti_est_h':'ralenti_antes'})
    despues_u = sim_df.groupby('NewUnidad', as_index=False)['ruta_ralenti_est_h'].sum().rename(columns={'NewUnidad':'Unidad','ruta_ralenti_est_h':'ralenti_despues'})
    ef = pd.merge(antes_u, despues_u, on='Unidad', how='outer').fillna(0.0)
    ef['Reduccion'] = ef['ralenti_antes'] - ef['ralenti_despues']
    ef = ef[['Unidad','Reduccion']].sort_values('Reduccion', ascending=False)

# Normalizar signos
ef_plot = ef.copy()
if 'Reduccion' not in ef_plot.columns and 'reduccion_h' in ef_plot.columns:
    ef_plot = ef_plot.rename(columns={'reduccion_h':'Reduccion'})
ef_plot = ef_plot.sort_values('Reduccion', ascending=False)
fig_efecto = px.bar(ef_plot, x='Unidad', y='Reduccion', title="Reducción de Ralentí por Unidad (h)",
                    labels={'Reduccion':'Horas reducidas'})
fig_efecto.update_layout(xaxis={'categoryorder':'total descending'}, height=360)
st.plotly_chart(fig_efecto, use_container_width=True)

st.markdown("---")

# Reasignaciones por Ruta
st.subheader("Reasignaciones por Ruta")

df_filtered = sim_df.copy()

# Asegurar tipo de dato
df_filtered['Fecha'] = pd.to_datetime(df_filtered['Fecha'], errors='coerce')

with st.expander("Agregar filtros"):
    date_range_routes = st.date_input(
        "Rango de fechas para Sankey",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date(),
        key="date_range_routes"
    )

    selected_routes = st.multiselect(
        "Filtrar rutas",
        sorted(sim_df['Ruta'].unique()),
        default=sorted(sim_df['Ruta'].unique()),
        key="routes_filter"
    )

# Aplicar filtros
start_date = pd.to_datetime(date_range_routes[0])
end_date = pd.to_datetime(date_range_routes[1])

mask = pd.Series(True, index=df_filtered.index)
if start_date is not None and end_date is not None:
    mask &= (df_filtered['Fecha'] >= start_date) & (df_filtered['Fecha'] <= end_date)
if selected_routes:
    mask &= df_filtered['Ruta'].isin(selected_routes)

df_filtered = df_filtered[mask]

if df_filtered.empty:
    st.warning("No hay datos que cumplan con los filtros seleccionados.")
else:
    # Juntar por ruta
    flow_counts = df_filtered.groupby(['Ruta', 'NewUnidad']).size().reset_index(name='count')
    flow_counts = flow_counts.sort_values('count', ascending=False)

    # Alternativa si es muy lento
    if show_bars:
        st.markdown("**Reasignación (gráfica de barras):**")
        top_routes = flow_counts.groupby('Ruta')['count'].sum().sort_values(ascending=False).head(12).index.tolist()
        stacked_df = flow_counts[flow_counts['Ruta'].isin(top_routes)]
        if not stacked_df.empty:
            fig_stack = px.bar(stacked_df, x='Ruta', y='count', color='NewUnidad', title="Top rutas: reasignaciones (apilado)")
            fig_stack.update_layout(barmode='stack', height=450)
            st.plotly_chart(fig_stack, use_container_width=True)
        else:
            st.info("No hay suficientes datos para la vista apilada.")

    # Sankey
    if show_sankey:
        st.markdown("**Sankey (Top flujos)**")
        top_n = max(5, min(200, top_n_flows))
        top_flows = flow_counts.head(top_n)

        # Agrupar
        nodes = list(pd.unique(top_flows[['Ruta','NewUnidad']].values.ravel()))
        node_idx = {n:i for i,n in enumerate(nodes)}
        sources = top_flows['Ruta'].map(node_idx).tolist()
        targets = top_flows['NewUnidad'].map(node_idx).tolist()
        values = top_flows['count'].tolist()

        # Crear Sankey
        sankey = go.Figure(data=[go.Sankey(
            node=dict(label=nodes, pad=15, thickness=15, line=dict(color="gray", width=0.5)),
            link=dict(source=sources, target=targets, value=values)
        )])
        sankey.update_layout(title=f"Ruta → Nueva Unidad (top {len(top_flows)})", height=650)
        st.plotly_chart(sankey, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Tip: usa los filtros en la barra lateral para reducir el volumen de datos y mejorar la velocidad.")