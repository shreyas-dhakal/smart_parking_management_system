import cv2
import numpy as np
import os

def interpolate_points(p1, p2, fraction):
    """ Interpolate between two points """
    return p1 + fraction * (p2 - p1)

def gradual_perspective_transform(image, src_points, final_dst_points, base_folder, image_name, suffix, steps=10):
    h, w = image.shape[:2]
    original_dst_points = np.copy(src_points)

    for step in range(steps):
        fraction = step / float(steps - 1)
        # Interpolating the destination points
        dst_points = np.array([interpolate_points(original_dst_points[i], final_dst_points[i], fraction) for i in range(4)], dtype=np.float32)

        M = cv2.getPerspectiveTransform(src_points, dst_points)
        max_width = max(w, int(np.linalg.norm(dst_points[0] - dst_points[1])), int(np.linalg.norm(dst_points[2] - dst_points[3])))
        max_height = max(h, int(np.linalg.norm(dst_points[0] - dst_points[2])), int(np.linalg.norm(dst_points[1] - dst_points[3])))
        transformed = cv2.warpPerspective(image, M, (max_width, max_height), borderMode=cv2.BORDER_CONSTANT, borderValue=[255, 255, 255])
        output_path = os.path.join(base_folder, f'{image_name}_{suffix}_step_{step}.jpg')
        cv2.imwrite(output_path, transformed)

def process_folder(input_folder, steps=5):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                # Skip files that are not images
                if image is None:
                    continue

                h, w = image.shape[:2]
                src_points = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

                # Define the final destination points for horizontal perspective transformations
                final_dst_points_left = np.float32([[w*0.5, 0], [w, 0], [w*0.2, h], [w*0.8, h]])
                final_dst_points_right = np.float32([[w*0.2, 0], [w*0.8, 0], [0, h], [w, h]])

                # Process image for each type of horizontal transformation
                image_name = os.path.splitext(file)[0]
                gradual_perspective_transform(image, src_points, final_dst_points_left, root, image_name, 'left', steps)
                gradual_perspective_transform(image, src_points, final_dst_points_right, root, image_name, 'right', steps)

input_folder = 'C:\\Users\\Shopnil\\Desktop\\FEdata'

# Process all images in the folder and subfolders
process_folder(input_folder)
