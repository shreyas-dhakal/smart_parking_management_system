from ultralytics import YOLO
import cv2
import os

# Load your YOLOv8 model
model = YOLO('en_segmentation.pt')

# Directory containing images
image_folder = "C:\\Users\\Shopnil\\Desktop\\shreyas_cropped"

# Directory to save cropped number plates
output_folder = "C:\\Users\\Shopnil\\Desktop\\extract_shreyas"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Assuming the class ID for number plates
number_plate_class_id = 0  # Replace with the correct class ID

# Iterate over each image
for img_name in os.listdir(image_folder):
    img_path = os.path.join(image_folder, img_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Failed to read image {img_name}")
        continue

    # Run YOLOv8 model
    results = model(img)
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()

    found_number_plate_count = 0

    # Process detections
    for box, class_id, confidence in zip(boxes, classes, confidences):
        if class_id == number_plate_class_id and confidence > 0.5:
            found_number_plate_count += 1
            x1, y1, x2, y2 = box
            crop_img = img[int(y1):int(y2), int(x1):int(x2)]

            # Modify the output filename for each cropped image
            output_filename = f"{os.path.splitext(img_name)[0]}_plate_{found_number_plate_count}{os.path.splitext(img_name)[1]}"
            output_path = os.path.join(output_folder, output_filename)
            cv2.imwrite(output_path, crop_img)
            print(f"Saved cropped image to {output_path}")

    if found_number_plate_count == 0:
        print(f"No number plate found in image {img_name}")

print("Extraction completed.")
