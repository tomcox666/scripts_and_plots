import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
import os

# Define the categories (car manufacturers)
categories = ['Toyota', 'Ford', 'Honda', 'Nissan', 'Volkswagen']

# Load the trained model
model = keras.models.load_model('car_classifier.h5')
dataset_path = os.path.expanduser('~/mini_scripts/image_classification/images')

# Load a new image for testing
new_image_path = os.path.join(dataset_path, 'test_images/test_image_1.jpg')
new_image = Image.open(new_image_path)
new_image = new_image.resize((224, 224))  # Resize the image to 224x224
new_image = np.array(new_image) / 255.0  # Normalize the image pixels to [0, 1]
new_image = np.expand_dims(new_image, axis=0)  # Add a batch dimension

# Predict the manufacturer of the new image
prediction = model.predict(new_image)
prediction_class = np.argmax(prediction)
print(f'Predicted manufacturer: {categories[prediction_class]}')