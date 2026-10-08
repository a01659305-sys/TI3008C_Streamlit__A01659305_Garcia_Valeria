import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Explorador de operación",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Carga los datos que utilizará la aplicación."""
    datos = pd.read_csv("datos_ejemplo.csv")
    datos["Fecha"] = pd.to_datetime(datos["Fecha"])
    return datos


df = cargar_datos()

st.title("Explorador de operación")
st.caption("Aplicación inicial para explorar resultados por área y región.")

# TODO OBLIGATORIO: escribe tu nombre completo.
st.write("**Desarrollado por:** Valeria García González Rubio")

st.sidebar.header("Filtros")

areas_disponibles = sorted(df["Área"].unique())
areas_seleccionadas = st.sidebar.multiselect(
    "Área",
    options=areas_disponibles,
    default=areas_disponibles,
)


# Filtro adicional por Región
regiones_disponibles = sorted(df["Región"].dropna().unique())

regiones_seleccionadas = st.sidebar.multiselect(
    "Región",
    options=regiones_disponibles,
    default=regiones_disponibles,
)

# Aplicar los filtros de Área y Región
df_filtrado = df[
    df["Área"].isin(areas_seleccionadas)
    & df["Región"].isin(regiones_seleccionadas)
].copy()



st.info(
    "Esta es la versión inicial. Selecciona una opción de la actividad y agrega "
    "una mejora funcional para el usuario."
)


# ================================================================
# ZONA DE TRABAJO
# Implementa UNA de las opciones indicadas en INSTRUCCIONES_ACTIVIDAD.md.
# Puedes reorganizar el código existente cuando sea necesario.
# ================================================================

# TODO OPCIÓN A: Tablero ejecutivo
# - Agrega al menos dos indicadores con st.metric.
# - Incorpora otro filtro.
# - Organiza dos vistas mediante st.tabs.

# TODO OPCIÓN B: Explorador de datos
# - Permite cargar un CSV con st.file_uploader.
# - Valida que el archivo tenga las columnas necesarias.
# - Permite descargar df_filtrado con st.download_button.

# TODO OPCIÓN C: Simulador
# - Solicita al menos dos valores al usuario.
# - Realiza un cálculo con esos valores.
# - Muestra un resultado y un mensaje success, warning o error.

# TODO OPCIÓN D: Reporte interactivo
# - Agrega una introducción que explique el propósito.
# - Organiza resultados y metodología en pestañas o en la barra lateral.
# - Incluye una conclusión o recomendación basada en los datos visibles.

st.subheader("Indicadores generales")

col1, col2 = st.columns(2)

total_casos = df_filtrado["Casos"].sum()

promedio_casos = (
    df_filtrado["Casos"].mean()
    if not df_filtrado.empty else 0
)

with col1:
    st.metric(
        label="Total de casos",
        value=f"{total_casos:,.0f}"
    )

with col2:
    st.metric(
        label="Promedio de casos por registro",
        value=f"{promedio_casos:,.2f}"
    )


# ==========================================
# NUEVO: PESTAÑAS
# ==========================================

tab1, tab2 = st.tabs(["📈 Resumen ejecutivo", "📋 Datos detallados"])

with tab1:
    st.subheader("Evolución de casos por fecha")

    casos_por_fecha = (
        df_filtrado.groupby("Fecha", as_index=False)["Casos"]
        .sum()
        .sort_values("Fecha")
    )

    fig = px.line(
        casos_por_fecha,
        x="Fecha",
        y="Casos",
        markers=True,
        title="Casos por fecha",
    )

    st.plotly_chart(fig, width="stretch", key="grafica_resumen")

    st.info(
        "La gráfica muestra la evolución de los casos "
        "según las áreas y regiones seleccionadas."
    )


with tab2:
    st.subheader("Datos disponibles")

    st.dataframe(
        df_filtrado,
        width="stretch",
        hide_index=True
    )

    st.write(
        f"Registros encontrados: {len(df_filtrado)}"
    )

    if df_filtrado.empty:
        st.warning(
            "No existen registros para los filtros seleccionados."
        )


