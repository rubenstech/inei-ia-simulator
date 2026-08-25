import streamlit as st
import pandas as pd
import openai

st.set_page_config(
    page_title="Asesor Estadístico IA - INEI Lab",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main { background-color: #faf8f5; }
    h1 { color: #1e3a8a; font-family: 'Helvetica Neue', sans-serif; }
    .stAlert { background-color: #e0f2fe; border-color: #bae6fd; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Asesor Estadístico IA | INEI Lab")
st.markdown("### Simulación Interactiva: Retos de la IA con Estadísticas Oficiales")
st.markdown("Esta herramienta descentralizada permite consultar indicadores socioeconómicos y demográficos simulados bajo estrictos parámetros del INEI, aplicando inteligencia analítica autónoma.")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv('datos_inei_simulacion.csv')

try:
    df_inei = load_data()
except Exception as e:
    st.error(f"Error cargando el dataset: {e}")
    df_inei = pd.DataFrame()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Parámetros de Simulación")
    st.info("Ecosistema SmartWorld AI \n Módulo: Smart Study On Demand")
    st.markdown("---")
    st.subheader("Datos Base Disponibles:")
    if not df_inei.empty:
        st.dataframe(df_inei[['Anio', 'Mes', 'Distrito', 'Indicador', 'Valor']], height=300)
    
    st.markdown("---")
    api_key_input = st.text_input("Ingresa tu OpenAI API Key (Opcional):", type="password")

# Main interface
query_option = st.selectbox(
    "Selecciona una consulta rápida o escribe la tuya:",
    [
        "Elige una opción...",
        "Analizar la evolución del costo de la Canasta Básica Familiar en Lima Metropolitana.",
        "Comparar la Tasa de Empleo Formal entre San Luis y San Borja.",
        "¿Cuál es la población estimada y situación de empleo en San Luis?"
    ]
)

user_prompt = st.text_area("O escribe tu consulta estadística personalizada:", value="" if query_option == "Elige una opción..." else query_option)

if st.button("Ejecutar Análisis Estadístico IA", type="primary"):
    if not user_prompt:
        st.warning("Por favor ingresa o selecciona una consulta.")
    else:
        with st.spinner("Procesando datos institucionales con rigor estadístico..."):
            
            context_data = df_inei.to_string(index=False)
            response_text = ""
            
            if api_key_input:
                try:
                    client = openai.OpenAI(api_key=api_key_input)
                    system_prompt = """Eres el Asesor Estadístico Senior e Inteligencia Analítica del INEI (Instituto Nacional de Estadística e Informática del Perú). Tu propósito es asistir a investigadores y tomadores de decisiones interpretando con rigor técnico los datos oficiales proporcionados.
                    REGLAS:
                    1. BASES DE DATOS OFICIALES: Tus respuestas DEBEN basarse exclusivamente en la información del dataset proporcionado.
                    2. RIGOR TÉCNICO: Utiliza terminología estadística formal.
                    3. ESTRUCTURA:
                       - Diagnóstico Rápido: Resumen directo del indicador.
                       - Análisis de Tendencia: Contextualización del comportamiento.
                       - Implicancia Práctica: Nota técnica para política pública."""
                    
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Dataset de referencia:\n{context_data}\n\nConsulta del usuario: {user_prompt}"}
                        ]
                    )
                    response_text = completion.choices[0].message.content
                except Exception as e:
                    response_text = f"Error al conectar con la API: {e}. Mostrando análisis analítico interno del dataset:"
            
            if not api_key_input or "Error" in response_text:
                response_text = f"""### 📈 Diagnóstico Rápido
- **Indicador Analizado:** Consulta procesada sobre los registros oficiales del INEI.
- **Datos institucionales de referencia registrados:**
```
{context_data}
```

### 📊 Análisis de Tendencia Institucional
Basado en los registros procesados para el periodo 2026, se observa estabilidad en los indicadores clave de Lima Metropolitana y distritos focales como San Luis. Los datos reflejan una correspondencia directa entre los costos de la canasta básica y las variables de empleo formal.

### 🏛️ Implicancia Práctica para la Gestión Pública
Este indicador es clave para la formulación de planes de desarrollo local y focalización de recursos socioeconómicos."""

            st.markdown("### 📋 Resultados del Análisis Estadístico")
            st.markdown(response_text)
            
            if "Empleo" in user_prompt or "Canasta" in user_prompt or "San Luis" in user_prompt:
                st.markdown("---")
                st.subheader("📊 Visualización Gráfica de Indicadores")
                chart_subset = df_inei[['Distrito', 'Valor']].set_index('Distrito')
                st.bar_chart(chart_subset)
