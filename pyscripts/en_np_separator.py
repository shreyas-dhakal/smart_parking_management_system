from ultralytics import YOLO
import torch
from PIL import Image
import numpy as np

# Load the YOLOv8 models
model_detection = YOLO('numberplate_detector.pt')  
model_classification = YOLO('np_en_separator1.pt')  

def process_image(img_path):
    # Load the image
    img = Image.open(img_path)
    img = np.array(img)

    # Detect number plates
    results = model_detection(img)
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()

    number_plate_class_id = 0  # Class ID for number plates in detection model

    for box, class_id, confidence in zip(boxes, classes, confidences):
        if class_id == number_plate_class_id and confidence > 0.5:
            x1, y1, x2, y2 = box
            # Crop the detected number plate
            crop_img = img[int(y1):int(y2), int(x1):int(x2)]

            # Classify the cropped number plate using the second YOLOv8 model
            classification_results = model_classification(crop_img)
            category_boxes = classification_results[0].boxes.xyxy.tolist()
            category_classes = classification_results[0].boxes.cls.tolist()
            category_confidences = classification_results[0].boxes.conf.tolist()

            # Process classification results
            # Two categories: 0 and 1
            for c_box, c_class, c_confidence in zip(category_boxes, category_classes, category_confidences):
                if c_confidence > 0.5:  # Confidence threshold
                    category = 'Category NP' if c_class == 0 else 'Category EN'
                    return crop_img, category

    return None, None  # No number plate found

cropped_image, category = process_image('C:\\Users\\Shopnil\\Desktop\\Project\\numberplate_detection_dataset\\20240126214640782.jpeg')
if cropped_image is not None:
    Image.fromarray(cropped_image).show()
    print("Number plate category:", category)
else:
    print("No number plate detected.")
