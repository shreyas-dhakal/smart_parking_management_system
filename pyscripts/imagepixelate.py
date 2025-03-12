import cv2
import os

def pixelate_image(image, pixelation_level):
    # Get the dimensions of the image
    height, width = image.shape[:2]

    # Resize down using the pixelation level
    # The greater the level, the more pixelated it will be
    small_image = cv2.resize(image, (width // pixelation_level, height // pixelation_level), interpolation=cv2.INTER_LINEAR)

    # Resize back to original size
    pixelated_image = cv2.resize(small_image, (width, height), interpolation=cv2.INTER_NEAREST)

    return pixelated_image

def process_folder(input_folder, pixelation_levels):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                # Skip files that are not images
                if image is None:
                    print(f"Could not open or find the image {image_path}. Skipping...")
                    continue

                for level in pixelation_levels:
                    # Pixelate image
                    pixelated_image = pixelate_image(image, level)

                    # Construct the output filename and save the pixelated image
                    base, extension = os.path.splitext(file)
                    output_filename = f"{base}_pixelated_{level}{extension}"
                    output_path = os.path.join(root, output_filename)
                    cv2.imwrite(output_path, pixelated_image)

input_folder = 'C:\\Users\\Shopnil\\Desktop\\FEdata' 

# Pixelate all images in the folder and subfolders with pixelation levels 4 and 5
process_folder(input_folder, pixelation_levels=[3, 4])
