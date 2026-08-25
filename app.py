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

# Campo de entrada de consulta por parte del usuario
consulta_rapida = st.selectbox(
    "Selecciona una consulta rápida o escribe la tuya:",
    [
        "Elige una opción...",
        "Analizar la evolución del costo de la Canasta Básica Familiar en Lima Metropolitana.",
        "Comparar la Tasa de Empleo Formal entre San Luis y San Borja.",
        "Mostrar indicadores de Pobreza y Población en Miraflores.",
        "Resumen general de distritos con mayor vulnerabilidad."
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
    
    # --- FILTRADO INTELIGENTE DE DATOS ---
    consulta_lower = consulta_personalizada.lower()
    
    # Buscar distritos mencionados en el texto del usuario
    distritos_encontrados = []
    for distrito in df_inei['Distrito'].unique():
        if distrito.lower() in consulta_lower:
            distritos_encontrados.append(distrito)
    
    # Si se encontraron distritos específicos en la consulta, filtramos por ellos
    if distritos_encontrados:
        df_filtrado = df_inei[df_inei['Distrito'].isin(distritos_encontrados)]
        st.success(f"🎯 Filtrado inteligente aplicado para: **{', '.join(distritos_encontrados)}**")
    else:
        # Si no menciona un distrito específico, mostramos una muestra representativa o general
        df_filtrado = df_inei.head(10)
        st.info("ℹ️ Mostrando vista general de registros institucionales relacionados.")

    st.markdown("#### 🔍 Diagnóstico Rápido")
    st.markdown(f"- **Indicador Analizado:** {consulta_personalizada if consulta_personalizada else 'Consulta general procesada.'}")
    st.markdown("- **Datos institucionales de referencia registrados:**")
    
    # Mostrar la tabla filtrada de manera limpia
    st.dataframe(df_filtrado, use_container_width=True)
    
    st.success("✅ Análisis procesado con éxito bajo los parámetros y proyecciones del INEI.")
