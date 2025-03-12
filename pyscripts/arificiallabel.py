import os

def label_full_image(image_path, class_id):
    # Extracting the name of the file without the extension
    file_name = os.path.splitext(os.path.basename(image_path))[0]

    # Path for the new label file
    label_file = os.path.join(os.path.dirname(image_path), file_name + ".txt")

    # Since the whole image is being labeled, the normalized coordinates are:
    # x_center = 0.5, y_center = 0.5, width = 1, height = 1
    label_data = f"{class_id} 0.5 0.5 1 1\n"

    # Write the label data to the file
    with open(label_file, 'w') as file:
        file.write(label_data)

def label_images_in_folder(folder_path, class_id):
    # Loop through all files in the folder
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, file)
            label_full_image(image_path, class_id)
            print(f"Labeled: {file}")

folder_path = 'C:\\Users\\Shopnil\\Desktop\\en'
class_id = 1  # Replace with your class ID
label_images_in_folder(folder_path, class_id)
