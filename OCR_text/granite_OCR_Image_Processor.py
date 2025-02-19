import streamlit as st
import os
import logging
from paddleocr import PaddleOCR
from PIL import Image
import pandas as pd
from datetime import datetime

BACKEND_EXCEL_FILE = "extracted_final_number.xlsx"

def save_to_excel(data, file_name):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    data_with_meta = [[file_name, current_date, current_time, text] for text in data]
    columns = ["File Name", "Date", "Time", "Extracted Text"]

    if os.path.exists(BACKEND_EXCEL_FILE):
        df_existing = pd.read_excel(BACKEND_EXCEL_FILE, engine='openpyxl')
        df_new = pd.DataFrame(data_with_meta, columns=columns)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = pd.DataFrame(data_with_meta, columns=columns)

    df_combined.to_excel(BACKEND_EXCEL_FILE, index=False, engine='openpyxl')

 
def setup_logger():
    """Sets up the logger for debugging."""
    logging.basicConfig(
        filename="ocr_app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
 
def save_uploaded_file(uploaded_file):
    """Saves the uploaded file temporarily and returns its path."""
    temp_path = "temp_image.jpg"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path
 
def perform_ocr(image_path):
    """Performs OCR on the given image and returns extracted text."""
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(image_path, cls=True)
    extracted_text = [line[1][0] for line in result[0]]
    return extracted_text
 
def display_results(extracted_text):
    """Displays OCR results in Streamlit UI."""
    st.subheader("Extracted Text")
    if extracted_text:
        for text in extracted_text:
            st.write(f"**Text:** {text}")
    else:
        st.write("No text detected. Please try another image.")
 
def main():
    setup_logger()
    st.set_page_config(page_title="OCR Text Extractor ", page_icon="📝", layout="centered")
    st.title("📝 OCR Text Extractor")
    uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"], help="Supported formats: JPG, JPEG, PNG")
    if uploaded_file is not None:
        image_path = save_uploaded_file(uploaded_file)
        image = Image.open(uploaded_file)
        st.image(image, caption='📷 Uploaded Image', use_container_width=True, output_format="JPEG")
        st.markdown("---")
        logging.info("Image uploaded successfully.")
        extracted_text = perform_ocr(image_path)
        display_results(extracted_text)

        if extracted_text:
            save_to_excel(extracted_text, uploaded_file.name)
            st.success("Text saved to backend Excel sheet successfully!")
            with open(BACKEND_EXCEL_FILE, "rb") as f:
                st.download_button("📥 Download Extracted Data", data=f, file_name="extracted_text.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.info("No text detected. Try another image.")
        os.remove(image_path)
        logging.info("Temporary image file removed.")
    else:
        st.error("Please upload an image to proceed.")

if __name__ == "__main__":
    main()
