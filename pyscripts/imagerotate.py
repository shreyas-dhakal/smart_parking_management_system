import cv2
import os
import numpy as np

def rotate_image(image, angle):
    h, w = image.shape[:2]
    center = (w / 2, h / 2)

    # Calculate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Calculate the size of the new image
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to consider the translation
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # Rotate the image with white background
    return cv2.warpAffine(image, M, (new_w, new_h), borderMode=cv2.BORDER_CONSTANT, borderValue=[255, 255, 255])

def process_image_rotation(image, base_folder, image_name, steps=10):
    for step in range(steps):
        # Update here to limit rotation to 0-10 degrees
        angle = (step / float(steps - 1)) * 10
        rotated_left = rotate_image(image, -angle)
        rotated_right = rotate_image(image, angle)

        cv2.imwrite(os.path.join(base_folder, f'{image_name}_left_{angle:.0f}.jpg'), rotated_left)
        cv2.imwrite(os.path.join(base_folder, f'{image_name}_right_{angle:.0f}.jpg'), rotated_right)

def process_folder(input_folder, steps=5):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                # Skip files that are not images
                if image is None:
                    continue

                # Process image
                image_name = os.path.splitext(file)[0]
                process_image_rotation(image, root, image_name, steps)

input_folder = 'C:\\Users\\Shopnil\\Desktop\\FEdata'

# Process all images in the folder and subfolders
process_folder(input_folder)
