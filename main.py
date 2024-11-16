import streamlit as st
from PIL import Image
import pandas as pd

# Initial page configuration
st.set_page_config(page_title="FashionLens", layout="centered", page_icon="👗")

# Title and description
st.title("FashionLens")
st.write(
    """
    Welcome to FashionLens! Upload a photo of a garment, and our app will analyze it to provide key attributes such as
    color, style, and patterns. Discover detailed insights about your outfit in seconds!
    """
)

# Section: Upload image
st.header("🔼 Upload an image of the product")
uploaded_file = st.file_uploader("Upload an image of the product to analyze:", type=["jpg", "png", "jpeg"])

# Section: Prediction
if uploaded_file:
    # Show the uploaded image
    st.image(Image.open(uploaded_file), caption="Uploaded Image", use_column_width=True)
    
    st.write("Processing the image... Please wait.")
    
    # Example of simulated predictions
    predictions = {
        "silhouette_type": "Straight",
        "sleeve_length_type": "INVALID",
        "color": "Black",
        "style": "Casual",
        "pattern": "Plain",
    }
    
    # Prediction results
    st.subheader("🎯 Predicted Attributes:")
    st.write("Here are the predicted attributes for the uploaded image:")
    for key, value in predictions.items():
        st.write(f"**{key.replace('_', ' ').capitalize()}**: {value}")

    # Save results as CSV
    data = [{"test_id": f"88_49726492_{key}", "des_value": value} for key, value in predictions.items()]
    df = pd.DataFrame(data)
    st.download_button(
        label="📥 Download predictions as CSV",
        data=df.to_csv(index=False),
        file_name="predicted_attributes.csv",
        mime="text/csv",
    )

# Additional instructions
else:
    st.write(
        """
        Upload an image to start the analysis.
        Once uploaded, the model will predict the key attributes of the product and allow you to download them as a CSV file.
        """
    )

# Footer
st.markdown("---")
st.markdown("**Developed for the Mango Challenge** 💻👕")
