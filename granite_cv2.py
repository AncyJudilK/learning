import cv2
import numpy as np
import streamlit as st

def process_image(uploaded_file):
    # Load the image
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    return image, edges

def find_contours(edges):
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def calculate_dimensions(contour, reference_length=1, reference_pixels=100):
    # Compute a bounding box
    x, y, w, h = cv2.boundingRect(contour)
    scale = reference_length / reference_pixels  # Reference scale: real-world units per pixel
    height = h * scale
    width = w * scale
    thickness = None  # Thickness may require another angle or method
    return width, height, thickness

# Streamlit app
st.title("Granite Dimension Measurement")
st.write("""
Upload an image of granite, and this application will calculate its height and width. Ensure a reference object 
(e.g., a ruler or known length) is present in the image for accurate scaling.
""")

uploaded_file = st.file_uploader("Upload Granite Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    # Process and display the image
    image, edges = process_image(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.image(edges, caption="Detected Edges", use_column_width=True)

    contours = find_contours(edges)
    if contours:
        # Assume the largest contour is the granite
        largest_contour = max(contours, key=cv2.contourArea)
        # Provide the reference length and pixel equivalent
        reference_length = st.number_input("Enter real-world reference length (e.g., 10 cm)", value=10.0)
        reference_pixels = st.number_input("Enter pixel length of the reference object", value=100)
        
        width, height, thickness = calculate_dimensions(largest_contour, reference_length, reference_pixels)
        
        st.subheader("Measured Dimensions:")
        st.write(f"Width: {width:.2f} units")
        st.write(f"Height: {height:.2f} units")
        st.write(f"Thickness: Unable to measure from this angle.")
    else:
        st.error("No contours found. Please ensure the image is clear and has a reference object.")

else:
    st.info("Please upload an image to get started.")

