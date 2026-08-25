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

# Selector directo de distritos
st.markdown("### 🎯 Selección de Distrito para Análisis")
lista_distritos = sorted(df_inei['Distrito'].unique().tolist())
distrito_seleccionado = st.selectbox(
    "Selecciona un distrito específico de Lima Metropolitana:",
    ["Todos los distritos"] + lista_distritos
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
    
    # Filtrado inteligente por selector y texto
    if distrito_seleccionado != "Todos los distritos":
        df_filtrado = df_inei[df_inei['Distrito'] == distrito_seleccionado]
        st.success(f"🎯 Análisis filtrado exclusivamente para el distrito de: **{distrito_seleccionado}**")
    else:
        consulta_lower = consulta_personalizada.lower()
        distritos_encontrados = [d for d in df_inei['Distrito'].unique() if d.lower() in consulta_lower]
        
        if distritos_encontrados:
            df_filtrado = df_inei[df_inei['Distrito'].isin(distritos_encontrados)]
            st.success(f"🎯 Filtrado inteligente aplicado para: **{', '.join(distritos_encontrados)}**")
        else:
            df_filtrado = df_inei
            st.info("ℹ️ Mostrando el consolidado general de los distritos registrados.")

    st.markdown("#### 🔍 Diagnóstico Rápido")
    st.markdown(f"- **Indicador / Consulta Analizada:** {consulta_personalizada if consulta_personalizada else f'Evaluación integral para {distrito_seleccionado}.'}")
    st.markdown("- **Registros institucionales obtenidos:**")
    
    # Mostrar la tabla filtrada
    st.dataframe(df_filtrado, use_container_width=True)
    
    # --- GRÁFICOS ESTADÍSTICOS INTEGRADOS ---
    st.markdown("#### 📈 Visualización Gráfica de Indicadores")
    if not df_filtrado.empty:
        # Creamos una tabla pivote para graficar de forma limpia si hay valores numéricos
        try:
            df_chart = df_filtrado.pivot(index='Distrito', columns='Indicador', values='Valor')
            st.bar_chart(df_chart)
        except Exception:
            # Gráfico alternativo directo si la estructura varía
            st.bar_chart(df_filtrado.set_index('Distrito')['Valor'])
    
    st.success("✅ Análisis procesado con éxito bajo los parámetros y proyecciones del INEI.")
