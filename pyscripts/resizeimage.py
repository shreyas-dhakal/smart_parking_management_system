import cv2
import os
import numpy as np
import random

def resize_image_randomly(image, min_scale=0.8, max_scale=1.0):
    """
    Resize the image by a random scale between min_scale and max_scale.
    """
    h, w = image.shape[:2]
    scale = random.uniform(min_scale, max_scale)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(image, (new_w, new_h))

def process_folder(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                if image is None:
                    continue

                resized_image = resize_image_randomly(image, 0.8, 1.0)  # Resizing by 0-20% randomly

                # Save the resized image
                # Replace original image
                cv2.imwrite(image_path, resized_image)

                # Save as a new file
                # cv2.imwrite(os.path.join(root, f'resized_{file}'), resized_image)


input_folder = 'C:\\Users\\Shopnil\\Desktop\\FEdata'

# Process all images in the folder and subfolders
process_folder(input_folder)
