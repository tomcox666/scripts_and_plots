import cv2
import sys

# Correct paths for Caffe model and Prototxt
prototxt_path = 'deploy.prototxt'  # Path to the downloaded Prototxt file
caffemodel_path = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'  # Path to the Caffe model

# Load the pre-trained model for face detection
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

# Load the image (ensure the path is correct)
image_path = 'input_image.jpg'  # Change this to your image's path
image = cv2.imread(image_path)

if image is None:
    print("Error: Could not read image. Check the file path.")
    sys.exit(1)

# Image dimensions
(h, w) = image.shape[:2]

# Create a blob from the image for face detection
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=True, crop=False)

# Set the blob to the network and perform face detection
net.setInput(blob)
detections = net.forward()

# Threshold for face detection confidence
confidence_threshold = 0.5

# Loop over detected faces and blur them
for i in range(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]

    if confidence > confidence_threshold:
        # Extract the box for the detected face
        box = detections[0, 0, i, 3:7] * [w, h, w, h]
        (x1, y1, x2, y2) = box.astype("int")

        # Ensure the coordinates are within the image boundaries
        x1, y1, x2, y2 = max(x1, 0), max(y1, 0), min(x2, w), min(y2, h)

        # Apply median blur for a strong effect
        roi = image[y1:y2, x1:x2]
        blurred_roi = cv2.medianBlur(roi, 31)  # Adjust the blur strength
        image[y1:y2, x1:x2] = blurred_roi

# Save the output image
cv2.imwrite('blurred_faces.jpg', image)

# Display the result for visual debugging
cv2.imshow("Blurred Faces", image)
cv2.waitKey(0)  # Wait for any key press
cv2.destroyAllWindows()  # Properly close the OpenCV window
