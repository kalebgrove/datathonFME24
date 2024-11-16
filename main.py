import streamlit as st
from PIL import Image
import pandas as pd

# Configuración inicial de la página
st.set_page_config(page_title="Fashion Attribute Analysis", layout="centered", page_icon="👗")

# Título y descripción
st.title("👗 Fashion Attribute Analysis & Classification")
st.write(
    """
    Bienvenido a la herramienta de análisis y clasificación de atributos de diseño de productos.
    Este prototipo utiliza Machine Learning para analizar imágenes de ropa y metadatos, 
    prediciendo atributos relevantes para agilizar el proceso de registro y diseño.
    """
)

# Sección: Subir imagen
st.header("🔼 Subir imagen del producto")
uploaded_file = st.file_uploader("Carga una imagen del producto para analizar:", type=["jpg", "png", "jpeg"])

# Sección: Predicción
if uploaded_file:
    # Mostrar imagen cargada
    st.image(Image.open(uploaded_file), caption="Imagen cargada", use_column_width=True)
    
    st.write("Procesando la imagen... Por favor, espera.")
    
    # Ejemplo de predicciones simuladas
    predictions = {
        "silhouette_type": "Recto",
        "sleeve_length_type": "INVALID",
        "color": "Negro",
        "style": "Casual",
        "pattern": "Liso",
    }
    
    # Resultados de predicción
    st.subheader("🎯 Predicciones de atributos:")
    st.write("Estas son las predicciones de atributos para la imagen cargada:")
    for key, value in predictions.items():
        st.write(f"**{key.replace('_', ' ').capitalize()}**: {value}")

    # Guardar los resultados en formato CSV
    data = [{"test_id": f"88_49726492_{key}", "des_value": value} for key, value in predictions.items()]
    df = pd.DataFrame(data)
    st.download_button(
        label="📥 Descargar predicciones como CSV",
        data=df.to_csv(index=False),
        file_name="predicciones_atributos.csv",
        mime="text/csv",
    )

# Instrucciones adicionales
else:
    st.write(
        """
        Sube una imagen para iniciar el análisis.
        Una vez cargada, el modelo predecirá los atributos clave del producto y te permitirá descargarlos como un archivo CSV.
        """
    )

# Footer
st.markdown("---")
st.markdown("**Desarrollado para el Mango Challenge** 💻👕")
