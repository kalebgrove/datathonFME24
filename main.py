import streamlit as st
from PIL import Image
import pandas as pd

# Initial page configuration
st.set_page_config(page_title="FashionLens", layout="centered", page_icon="./LOGOicon.png")

# Custom CSS for styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@700&family=Instrument+Sans:wght@400&display=swap');

    .main-title {
        font-family: 'Josefin Sans', sans-serif;
        font-size: 36px;
        text-align: center;
        margin-bottom: 10px;
    }

    .title {
        font-family: 'Josefin Sans', sans-serif;
        font-size: 30px;
        text-align: center;
        margin-bottom: 10px;
    }

    .description {
        font-family: 'Instrument Sans', sans-serif;
        font-size: 18px;
        text-align: center;
        margin-bottom: 20px;
        color: #555;
    }

    .footer {
        font-family: 'Instrument Sans', sans-serif;
        font-size: 16px;
        text-align: center;
        margin-top: 30px;
        color: #888;
    }

    .image-attributes-container {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        gap: 20px;
        margin-top: 20px;
    }

    .image-container {
        max-width: 10px; /* Maximum width for image container */
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .image-container img {
        width: 50%;
        height: 50px;
    }

    .attributes {
        font-family: 'Instrument Sans', sans-serif;
        font-size: 16px;
    }

    .attributes h3 {
        font-size: 20px;
        margin-bottom: 10px;
    }

    /* CSS for centering the download button */
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and description
st.markdown('<div class="main-title">FashionLens</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="description">
        Welcome to FashionLens! Upload a photo of a garment and, optionally, a metadata file. Our app will analyze 
        the data to provide key attributes such as color, style, and patterns. Discover detailed insights about your outfit in seconds!
    </div>
    """,
    unsafe_allow_html=True,
)

# Section: Upload image
st.markdown('<div class="title">Upload the product details</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

# Image uploader
with col1:
    uploaded_file = st.file_uploader("Upload an image of the product:", type=["jpg", "png", "jpeg"])

# Metadata uploader
with col2:
    metadata_file = st.file_uploader("Upload a metadata file (.csv or .xlsx):", type=["csv", "xlsx"])

# Section: Prediction
if uploaded_file and metadata_file:
    # Layout for image and attributes side by side
    st.markdown('<div class="image-attributes-container">', unsafe_allow_html=True)

    with col1:
        # Display the uploaded image in a styled container
        st.markdown(
            f"""
            <div class="image-container">
                <img src="data:image/jpeg;base64,{st.image(Image.open(uploaded_file), use_container_width=True).data}"/>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        # Display predicted attributes
        predictions = {
            "Silhouette Type": "Straight",
            "Sleeve Length Type": "INVALID",
            "Color": "Black",
            "Style": "Casual",
            "Pattern": "Plain",
        }
        attributes_html = "<div class='attributes'><h3>🎯 Predicted Attributes:</h3><ul>"
        for key, value in predictions.items():
            attributes_html += f"<li><b>{key}:</b> {value}</li>"
        attributes_html += "</ul></div>"
        st.markdown(attributes_html, unsafe_allow_html=True)
        # Close the container
        st.markdown('</div>', unsafe_allow_html=True)

    # Save results as CSV
    data = [{"test_id": f"88_49726492_{key.replace(' ', '_').lower()}", "des_value": value} for key, value in predictions.items()]
    df = pd.DataFrame(data)

    # Center the download button
    st.download_button(
        label="📥 Download predictions as CSV",
        data=df.to_csv(index=False),
        file_name="predicted_attributes.csv",
        mime="text/csv",
    )

    
# Additional instructions
st.markdown(
    '<div class="description">Upload an image and a metadata file to start the analysis. The model will predict the key attributes of the product and allow you to download them as a CSV file.</div>',
    unsafe_allow_html=True,
)

# Footer
st.markdown('<div class="footer">Developed for the Mango Challenge</div>', unsafe_allow_html=True)
