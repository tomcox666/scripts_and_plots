import cv2
import os  # <--- import os module to handle file paths
import sys

# Add the following function to check for file existence
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    
prototxt_path = 'deploy.prototxt'
caffemodel_path = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
cfv
# Check if the required files exist
check_file_exists(prototxt_path)  # <--- Check for prototxt file
check_file_exists(caffemodel_path)  #<--- Check for caffemodel file

net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

image_path = 'input_image.jpg'
image = cv2.imread(image_path)

if image is None:  
  print("Error: Could not read image. Check the file path.")
  sys.exit(1)
   
(h, w) = image.shape[:2] 

blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=True, crop=False)
   
net.setInput(blob)
detections = net.forward()
   
confidence_threshold = 0.5

for i in range(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]  # <--- changed the index from 3 to 2 to get the confidence score
    
    if confidence > confidence_threshold:
        box = detections[0, 0, i, 3:7] * [w, h, w, h]
        (x1, y1, x2, y2) = box.astype("int")
   
        x1, y1, x2, y2 = max(0, x1), max(0, y1), min(w, x2), min(h, y2)  # <--- Fixed the order of max and min
        roi = image[y1:y2, x1:x2]
        blurred_roi = cv2.medianBlur(roi, 15)  # <--- Using a larger kernel size (31 was too large)
        image[y1:y2, x1:x2] = blurred_roi
   
cv2.imshow("Blurred Faces", image)
cv2.waitKey(0)
cv2.destroyAllWindows()