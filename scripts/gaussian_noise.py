import cv2
import numpy as np

def gaussian_noise(img, mean, std):
    """Adds Gaussian noise to an image."""
    row, col, ch = img.shape
    gauss = np.random.normal(mean, std, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = img + gauss
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)  # Ensure pixel values are in [0, 255]
    return noisy

try:
    img = cv2.imread('test.jpg')
    if img is None:
        raise FileNotFoundError("Image 'test.jpg' not found.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

edge_images = []
for mean in range(0, 60, 10):
    noisy_img = gaussian_noise(img.copy(), mean, 25)  # Using a fixed std for simplicity
    edges = cv2.Canny(noisy_img, 100, 200)
    edge_images.append(edges)

# Display images in separate windows
cv2.imshow('Original Image', img)
for i, edge_img in enumerate(edge_images):
    cv2.imshow(str(i), edge_img)

# Wait for user input and then close windows
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save selected image
try:
    selection = int(input("Enter the index of the image you want to save (0-{}): ".format(len(edge_images)-1)))
    if 0 <= selection < len(edge_images):
        filename = input("Enter the filename for saving (e.g., saved_image): ")
        cv2.imwrite(f"{filename}.jpg", edge_images[selection])
        print(f"Image saved as {filename}")
    else:
        print("Invalid selection.")
except ValueError:
    print("Invalid input. Please enter a number.")
except Exception as e:
    print(f"An error occurred: {e}")