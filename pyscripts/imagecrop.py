import cv2
import os
import numpy as np

# Initialize global variables
cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
window_width, window_height = 800, 600
resized_image = None
roi = None  # To store the cropped region

def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, resized_image, roi
    resized_image = param['image']

    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x, y = x, y, x, y
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False

        x1, x2 = sorted([x_start, x_end])
        y1, y2 = sorted([y_start, y_end])

        if x2 - x1 > 0 and y2 - y1 > 0:
            roi = resized_image[y1:y2, x1:x2]
            cv2.imshow("Cropped", roi)
        else:
            print("Invalid crop dimensions. Please try again.")
            roi = None

def resize_and_center_image(image, width, height):
    h, w = image.shape[:2]
    scaling_factor = min(width / w, height / h)
    new_w, new_h = int(w * scaling_factor), int(h * scaling_factor)
    resized = cv2.resize(image, (new_w, new_h))

    # Calculate border to center the image
    top_border = (height - new_h) // 2
    bottom_border = height - new_h - top_border
    left_border = (width - new_w) // 2
    right_border = width - new_w - left_border

    return cv2.copyMakeBorder(resized, top_border, bottom_border, left_border, right_border, cv2.BORDER_CONSTANT)

def process_folder(input_folder, output_folder):
    global roi

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                if image is None:
                    continue

                resized_image = resize_and_center_image(image, window_width, window_height)
                params = {'image': resized_image, 'filename': file, 'save_dir': output_folder}

                cv2.namedWindow("image")
                cv2.setMouseCallback("image", mouse_crop, params)

                while True:
                    cv2.imshow("image", resized_image)
                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("r"):
                        resized_image = resize_and_center_image(image, window_width, window_height)
                        params['image'] = resized_image
                        roi = None

                    elif key == ord("d"):  # Save and go to next image
                        if roi is not None:
                            save_path = os.path.join(output_folder, f"cropped_{file}")
                            cv2.imwrite(save_path, roi)
                            print(f"Cropped image saved as: {save_path}")
                            break
                        else:
                            print("No cropped image to save.")

                    elif key == ord("f"):  # Skip without saving
                        break

                cv2.destroyAllWindows()

input_folder = 'C:\\Users\\Shopnil\\Desktop\\1'
output_folder = 'C:\\Users\\Shopnil\\Desktop\\2'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

process_folder(input_folder, output_folder)
