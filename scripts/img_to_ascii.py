from PIL import Image
import os

def image_to_ascii(image_path, max_chars=40000):
    """
    Converts an image to ASCII art using a limited number of characters.

    Args:
        image_path: Path to the input image file.
        max_chars: Maximum number of ASCII characters to use in the output.

    Returns:
        A string representing the ASCII art version of the image, or an error message.
    """
    if not os.path.exists(image_path):
        return "Error: Image file not found."

    try:
        img = Image.open(image_path).convert('L')  # Convert to grayscale
    except Exception as e:
        return f"Error opening image: {e}"

    width, height = img.size
    aspect_ratio = height / width
    new_width = int((max_chars / aspect_ratio)**0.5)
    new_height = int(new_width * aspect_ratio)

    if new_width > width or new_height > height:
        print("Warning: Image is smaller than the specified maximum character limit. Using original image size.")
        new_width = width
        new_height = height

    img = img.resize((new_width, new_height))

    pixels = img.getdata()
    chars = " .:-=+*#%@"[::-1]  # Characters ordered by density (from light to dark)
    n_chars = len(chars)
    ascii_image = "".join(chars[pixel * n_chars // 256] for pixel in pixels)

    ascii_lines = [ascii_image[i:i + new_width] for i in range(0, len(ascii_image), new_width)]
    return "\n".join(ascii_lines)

# Example usage:
image_path = 'mondeo_2.jpg'

# Create a dummy image file for testing (if it doesn't exist)
if not os.path.exists(image_path):
    try:
        with open(image_path, 'wb') as f:
            f.write(b'This is a dummy file to prevent FileNotFoundError.')
        print(f"Dummy image file '{image_path}' created for testing.")
    except Exception as e:
        print(f"Error creating dummy image file: {e}")
        exit()

ascii_art = image_to_ascii(image_path)

if ascii_art.startswith("Error"):
    print(ascii_art)
else:
    print(ascii_art)

# Optional: Delete the dummy image file after testing
delete_dummy = input("Delete the dummy image file? (y/n): ").lower()
if delete_dummy == 'y' and os.path.exists(image_path):
    try:
        os.remove(image_path)
        print(f"Dummy image file '{image_path}' deleted.")
    except Exception as e:
        print(f"Error deleting dummy file: {e}")