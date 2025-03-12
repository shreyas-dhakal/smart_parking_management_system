import os

# Set the paths to the image and text file directories
image_folder = 'C:\\Users\\Shopnil\\Desktop\\numbers.v1i.yolov8\\valid\\images'  # Replace with the path to your image folder
txt_folder = 'C:\\Users\\Shopnil\\Desktop\\numbers.v1i.yolov8\\valid\\labels'      # Replace with the path to your text file folder

# List of image file extensions you want to check
image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

# Get the list of image file names without extensions
image_files = {os.path.splitext(file)[0] for file in os.listdir(image_folder) if os.path.splitext(file)[1].lower() in image_extensions}

# Get the list of text file names without extensions
txt_files = {os.path.splitext(file)[0] for file in os.listdir(txt_folder) if file.endswith('.txt')}

# Find image files without a corresponding text file
images_to_delete = image_files - txt_files

# Delete these images
for image in images_to_delete:
    for ext in image_extensions:
        image_path = os.path.join(image_folder, image + ext)
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted: {image_path}")

print("Cleanup complete.")
