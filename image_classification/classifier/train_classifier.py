import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras

# Define the categories (car manufacturers)
categories = ['Toyota', 'Ford']

# Load the dataset (images of cars)
dataset_path = os.path.expanduser('~/mini_scripts/image_classification/images')
images = []
labels = []
for category in categories:
    category_path = os.path.join(dataset_path, category)
    print(f"Loading images for category: {category}")
    for image_file in os.listdir(category_path):
        image_path = os.path.join(category_path, image_file)
        # Load and preprocess the image
        image = Image.open(image_path).resize((224, 224))
        image = np.array(image) / 255.0  # Normalize the image pixels to [0, 1]
        images.append(image)
        labels.append(categories.index(category))

# Convert lists to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Define the neural network model
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(len(categories), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
epochs = 20
print(f"Training the model for {epochs} epochs...")
model.fit(x_train, y_train, epochs=epochs, validation_data=(x_test, y_test))

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {test_acc:.2f}%')

# Save the trained model
model.save('car_classifier.h5')
print("Model saved successfully.")