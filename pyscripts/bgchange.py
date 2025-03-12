import cv2
import numpy as np
import os
import random

def adjust_background_grayscale(image):
    # Check if the image is grayscale; convert to BGR if it is
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Define the range for white color
    lower_white = np.array([200, 200, 200], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)

    # Create a mask to isolate white background
    mask = cv2.inRange(image, lower_white, upper_white)

    # Random gray value
    random_gray = random.randint(180, 220)

    # Change white (255) to random gray value in the mask
    image[mask == 255] = [random_gray, random_gray, random_gray]

    # Optionally convert back to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image

def process_folder(input_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                # Skip files that are not images
                if image is None:
                    continue

                # Adjust the background grayscale
                adjusted_image = adjust_background_grayscale(image)

                # Save the adjusted image
                cv2.imwrite(os.path.join(root, f'adjusted_{file}'), adjusted_image)

input_folder = 'C:\\Users\\Shopnil\\Desktop\\FEdata'

# Process all images in the folder and subfolders
process_folder(input_folder)
