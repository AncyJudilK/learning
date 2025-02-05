import os
import streamlit as st
from google.cloud import vision
import pandas as pd
from PIL import Image

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

def extract_text_from_image(image_path):
    # Initialize Google Vision client
    client = vision.ImageAnnotatorClient()

    # Load the image
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Extract all detected text
    if texts:
        extracted_text = texts[0].description
    else:
        extracted_text = "No text detected."

    return extracted_text

def save_to_excel(text, filename="output.xlsx"):
    # Create a DataFrame and save to Excel
    df = pd.DataFrame({"Extracted Text": [text]})
    df.to_excel(filename, index=False)
    return filename

def main():
    st.title("Handwritten Text Recognition with Google Cloud Vision")
    st.write("Upload an image containing handwritten text, and the app will extract the text and save it to an Excel file.")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Extract text
        extracted_text = extract_text_from_image("temp_image.jpg")
        st.write("Extracted Text:")
        st.write(extracted_text)

        # Save to Excel
        excel_filename = save_to_excel(extracted_text)
        st.success(f"Text saved to {excel_filename}")

        # Provide download link for the Excel file
        with open(excel_filename, "rb") as file:
            btn = st.download_button(
                label="Download Excel File",
                data=file,
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
