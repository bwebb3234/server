from stegano import lsb
import tkinter as tk
from tkinter import filedialog

def encode_message(input_image_path, message, output_image_path):
    secret_image = lsb.hide(input_image_path, message)
    secret_image.save(output_image_path)
    print(f"Message encoded and saved to {output_image_path}")

def decode_message(image_path):
    secret = lsb.reveal(image_path)
    print(f"Hidden message: {secret}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt user to select the input image file
    print("Please select the input image (PNG preferred):")
    input_image = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if not input_image:
        print("No input image selected. Exiting.")
        exit()

    # Prompt user for the message to hide
    user_message = input("Enter the message to hide in the image: ")

    # Prompt user to select the output file path
    print("Please select the output image path (it will save the encoded image):")
    output_image = filedialog.asksaveasfilename(
        title="Save Encoded Image",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )
    if not output_image:
        print("No output file path selected. Exiting.")
        exit()

    # Encode the message
    encode_message(input_image, user_message, output_image)

    # Optionally, you could call decode_message(output_image) here to test decoding