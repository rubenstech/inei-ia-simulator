import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Asesor Estadístico IA | INEI Lab",
    page_icon="📊",
    layout="wide"
)

# Título y presentación
st.markdown("""
    <div style='display: flex; align-items: center;'>
        <h1>📊 Asesor Estadístico IA | INEI Lab</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("Simulación Interactiva: Retos de la IA con Estadísticas Oficiales")
st.markdown(
    "Esta herramienta descentralizada permite consultar indicadores socioeconómicos y demográficos simulados bajo estrictos "
    "parámetros del INEI, aplicando inteligencia analítica autónoma."
)

# Barra lateral para parámetros e inventario de datos
st.sidebar.markdown("### ⚙️ Parámetros de Simulación")
st.sidebar.info("Ecosistema SmartWorld AI\nMódulo: Smart Study On Demand")

# Carga de datos oficiales simulados (con caché para velocidad)
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_inei_simulacion.csv")

df_inei = cargar_datos()

st.sidebar.markdown("### 📋 Datos Base Disponibles:")
st.sidebar.dataframe(df_inei.head(15), height=300)

# --- NUEVO: SELECTOR MÚLTIPLE PARA COMPARACIÓN DE DISTRITOS ---
st.markdown("### 🎯 Comparativa Multi-Distrito")
lista_distritos = sorted([d for d in df_inei['Distrito'].unique() if d != "Lima (Promedio)"])

distritos_seleccionados = st.multiselect(
    "Selecciona dos o más distritos para comparar:",
    options=lista_distritos,
    default=["San Luis", "San Borja", "Miraflores"]  # Selección inicial por defecto para que luzca lleno al cargar
)

consulta_rapida = st.selectbox(
    "O selecciona una consulta rápida:",
    [
        "Elige una opción...",
        "Analizar la evolución del costo de la Canasta Básica Familiar en Lima Metropolitana.",
        "Comparar indicadores demográficos y de pobreza oficial.",
        "Mostrar resumen de vulnerabilidad y empleo."
    ]
)

consulta_personalizada = st.text_area(
    "O escribe tu consulta estadística personalizada:",
    value=consulta_rapida if consulta_rapida != "Elige una opción..." else ""
)

api_key = st.sidebar.text_input("Ingresa tu OpenAI API Key (Opcional):", type="password")

# Botón de ejecución
if st.button("Ejecutar Análisis Estadístico IA"):
    st.markdown("---")
    st.markdown("### 📋 Resultados del Análisis Estadístico")
    
    # Filtrar según los distritos seleccionados en el multiselect
    if distritos_seleccionados:
        df_filtrado = df_inei[df_inei['Distrito'].isin(distritos_seleccionados)]
        st.success(f"🎯 Comparativa activa para los distritos: **{', '.join(distritos_seleccionados)}**")
    else:
        # Si no elige ninguno, toma por defecto un par o todo el general
        df_filtrado = df_inei[df_inei['Distrito'].isin(["San Luis", "San Borja"])]
        st.warning("⚠️ No seleccionaste ningún distrito. Mostrando comparación predeterminada (San Luis y San Borja).")

    st.markdown("#### 🔍 Diagnóstico Rápido")
    st.markdown(f"- **Indicador / Consulta Analizada:** {consulta_personalizada if consulta_personalizada else 'Evaluación comparativa multi-distrito.'}")
    st.markdown("- **Registros institucionales obtenidos:**")
    
    # Mostrar la tabla filtrada
    st.dataframe(df_filtrado, use_container_width=True)
    
    # --- GRÁFICOS COMPARATIVOS AVANZADOS ---
    st.markdown("#### 📈 Visualización Comparativa de Indicadores")
    if not df_filtrado.empty:
        try:
            # Transformamos los datos en una tabla cruzada (pivote) para que el gráfico de barras compare perfectamente por indicador
            df_pivot = df_filtrado.pivot(index='Distrito', columns='Indicador', values='Valor')
            st.bar_chart(df_pivot)
        except Exception:
            st.bar_chart(df_filtrado.set_index('Distrito')['Valor'])
    
    st.success("✅ Análisis procesado con éxito bajo los parámetros y proyecciones del INEI.")
