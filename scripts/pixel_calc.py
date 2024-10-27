from PIL import Image
import colorsys

def analyze_colors(image_path):
  """
  Analyzes the significant colors (blue, white, yellow) in an image.

  Args:
    image_path: Path to the image file.

  Returns:
    A dictionary containing the count of blue, white, and yellow pixels.
  """

  try:
    img = Image.open(image_path).convert("RGB")
  except FileNotFoundError:
    print(f"Image not found at: {image_path}")
    return None

  width, height = img.size
  blue_count = 0
  white_count = 0
  yellow_count = 0

  for x in range(width):
    for y in range(height):
      r, g, b = img.getpixel((x, y))
      h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

      # Define color thresholds (adjust as needed)
      if b > r + 50 and b > g + 50:  # Mostly blue
        blue_count += 1
      elif r > 200 and g > 200 and b > 200:  # Mostly white
        white_count += 1
      if 50/360 <= h <= 70/360 and s >= 0.4 and v >= 0.4:
        yellow_count += 1

  total_pixels = width * height
  blue_percent = (blue_count / total_pixels) * 100
  white_percent = (white_count / total_pixels) * 100
  yellow_percent = (yellow_count / total_pixels) * 100

  return {
      "blue": blue_count,
      "white": white_count,
      "yellow": yellow_count,
      "blue_percent": blue_percent,
      "white_percent": white_percent,
      "yellow_percent": yellow_percent
  }


if __name__ == "__main__":
  image_path = "grey2.jpg"  # Replace with your image path
  results = analyze_colors(image_path)

  if results:
    print("Color Analysis:")
    print(f"  Blue Pixels: {results['blue']} ({results['blue_percent']:.2f}%)")
    print(f"  White Pixels: {results['white']} ({results['white_percent']:.2f}%)")
    print(f"  Yellow Pixels: {results['yellow']} ({results['yellow_percent']:.2f}%)")