from PIL import Image, ImageDraw
import random

def is_path_clear(img, path_width):
    """Checks if a path of given width exists from top to bottom."""
    width, height = img.size
    pixels = img.load()

    for start_x in range(width - path_width + 1):
        path = [(start_x + i, 0) for i in range(path_width)]
        visited = set()

        while path:
            current_pixel = path.pop(0)
            if current_pixel[1] == height - 1:
                return True  # Path reached the bottom

            visited.add(current_pixel)
            neighbors = [(current_pixel[0] + dx, current_pixel[1] + dy) for dx in [-1, 0, 1] for dy in [1]
                         if 0 <= current_pixel[0] + dx < width and 0 <= current_pixel[1] + dy < height]

            for neighbor in neighbors:
                if neighbor not in visited and pixels[neighbor] == (0, 0, 0):  # Check if black (empty)
                    path.append(neighbor)

    return False

def generate_pinball_table(width, height, num_shapes, filename, path_width):
    """Generates a pinball table with a guaranteed path."""
    while True:
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        shapes = ['rectangle', 'circle', 'triangle']

        for _ in range(num_shapes):
            shape_type = random.choice(shapes)
            x = random.randint(0, width - 30)
            y = random.randint(0, height - 30)
            size = random.randint(30, 60)

            if shape_type == 'rectangle':
                draw.rectangle([x, y, x + size, y + size / 2], fill='white')
            elif shape_type == 'circle':
                draw.ellipse([x, y, x + size, y + size], fill='white')
            else:
                draw.polygon([(x, y), (x + size, y), (x + size / 2, y + size)], fill='white')

        if is_path_clear(img, path_width):
            img.save(filename)
            break

# Generate 100 different pinball table configurations with a guaranteed path
for i in range(1):
    filename = f"pinball_tables/pinball_table_{i}.png"
    generate_pinball_table(200, 400, 15, filename, 30)

print("100 pinball table configurations with a guaranteed 30-pixel path generated as PNG images.")