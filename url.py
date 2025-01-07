# import streamlit as st
# import time

# st.title("My Heart 💖")

# # Container to hold the running text
# placeholder = st.empty()

# # Text to display
# text = "I love you 💖"

# # Running text effect
# for _ in range(1):  # Run the animation once
#     for i in range(len(text) + 1):
#         placeholder.text(text[:i])  # Display the substring
#         time.sleep(0.2)  # Pause for animation

# # Create a downloadable text file
# file_content = "I love you 💖"
# file_name = "I_love_you.txt"

# # Download button
# st.download_button(
#     label="Download 'I Love You' Text",
#     data=file_content,
#     file_name=file_name,
#     mime="text/plain",
# )




import streamlit as st

# Set page layout
st.set_page_config(page_title="Coffee Menu", layout="wide")

# Function to set the background image
def set_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover; /* Ensure the image covers the entire background */
            background-position: center;
            color: white; /* White text for contrast */
            font-family: 'Arial', sans-serif;
        }}
        h1, h2 {{
            color: #F5DEB3; /* Lighter brown for headings */
        }}
        .total {{
            font-size: 20px;
            font-weight: bold;
            color: #F5DEB3;
        }}
        .menu-item {{
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #F5DEB3;
            border-radius: 5px;
            background-color: rgba(160, 82, 45, 0.8); /* Semi-transparent brown */
        }}
        .menu-item:hover {{
            background-color: rgba(210, 105, 30, 0.9);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Set background image URL directly
background_image_url = 'https://img.lovepik.com/photo/48008/6757.jpg_wh860.jpg'  # Replace with your desired image URL
set_background_image(background_image_url)

# Main Title
st.title("Coffee Menu ☕")

# Subtitle for the Classic section
st.subheader("Classic")

# Coffee menu options and prices
menu = {
    "Latte": 4.75,
    "Flat White": 4.50,
    "Americano": 3.25,
    "Pour Over": 3.50,
    "Cappuccino": 4.50,
    "Espresso": 3.25,
    "Mocha": 5.75,
}

# Initialize a session state for total
if "total" not in st.session_state:
    st.session_state["total"] = 0.0

# Display menu items
for coffee, price in menu.items():
    col1, col2 = st.columns([3, 1])  # Layout for menu items
    with col1:
        st.markdown(f"<div class='menu-item'>{coffee}</div>", unsafe_allow_html=True)
    with col2:
        if st.button(f"Add ${price:.2f}", key=coffee):
            st.session_state["total"] += price

# Display total amount
st.markdown(
    f"<div class='total'>Total: ${st.session_state['total']:.2f}</div>",
    unsafe_allow_html=True,
)

# Footer text
st.markdown("<br><br>Enjoy your coffee! ☕💖", unsafe_allow_html=True)
