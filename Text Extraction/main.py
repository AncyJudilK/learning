import streamlit as st
import easyocr
import requests
import tempfile
from PIL import Image

def extract_text_easyocr(image_path):
    """Extract text from the image using EasyOCR."""
    reader = easyocr.Reader(['en'], gpu=False)  # Set 'gpu=True' if GPU is available
    results = reader.readtext(image_path, detail=0)  # Extract text without bounding boxes
    return " ".join(results)  # Combine extracted lines into a single string

def send_to_backend(text, api_url):
    """Send the extracted text to the backend API."""
    payload = {'extracted_text': text}
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.RequestException as e:
        return None, f"Error communicating with backend: {e}"

# Streamlit App
st.title("Text Extraction using EasyOCR")

# File uploader for image input
uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg", "bmp"])
api_url = st.text_input("Backend API URL", "http://127.0.0.1:8000/receive_text")

if uploaded_file and api_url:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
        temp_file.write(uploaded_file.read())
        image_path = temp_file.name

    # Display the uploaded image
    st.image(Image.open(image_path), caption="Uploaded Image", use_column_width=True)

    # Extract text from the image using EasyOCR
    with st.spinner("Extracting text with EasyOCR..."):
        try:
            text = extract_text_easyocr(image_path)
            st.text_area("Extracted Text", text if text else "No text extracted", height=200)
        except Exception as e:
            st.error(f"Error during text extraction: {e}")
            st.stop()

    # Button to send extracted text to the backend
    if st.button("Send to Backend"):
        with st.spinner("Sending extracted text to backend..."):
            status, response = send_to_backend(text, api_url)
        if status:
            st.success(f"Backend Response: {response}")
        else:
            st.error(f"Failed to send data to backend: {response}")



