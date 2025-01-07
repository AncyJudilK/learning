import qrcode
from PIL import Image

def generate_qr_code(data, filename="qrcode.png"):
    """
    Generate a QR code for the given data and save it as an image file.

    Parameters:
    data (str): The information to encode in the QR code (e.g., URL, text).
    filename (str): The name of the output image file.
    """
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code, 1 is 21x21 matrix
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in pixels
        border=4,  # Border width (minimum is 4 for a valid QR code)
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image of the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save(filename)
    print(f"QR code saved as {filename}")

# Example usage
if __name__ == "__main__":
    input_data = input("Enter the data or URL to encode in the QR code: ")
    output_filename = "my_qr_code.png"
    generate_qr_code(input_data, output_filename)
