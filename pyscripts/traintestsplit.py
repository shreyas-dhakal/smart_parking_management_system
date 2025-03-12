import os
import shutil
import random

# Set the path to your dataset
dataset_path = 'C:\\Users\\Shopnil\\Desktop\\Project\\nepali_character_dataset'

# Define the ratio for splitting
train_ratio = 0.8

# Create train and validation directories
train_path = os.path.join(dataset_path, 'train')
validation_path = os.path.join(dataset_path, 'validation')

os.makedirs(train_path, exist_ok=True)
os.makedirs(validation_path, exist_ok=True)

# Process each folder in the dataset
for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)
    
    if os.path.isdir(folder_path):
        # List all images in the folder
        images = [img for img in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, img))]

        # Shuffle the images
        random.shuffle(images)

        # Split the images into train and validation sets
        split_index = int(train_ratio * len(images))
        train_images = images[:split_index]
        validation_images = images[split_index:]

        # Create corresponding folders in train and validation directories
        train_folder_path = os.path.join(train_path, folder)
        validation_folder_path = os.path.join(validation_path, folder)

        os.makedirs(train_folder_path, exist_ok=True)
        os.makedirs(validation_folder_path, exist_ok=True)

        # Move images to their respective folders
        for img in train_images:
            shutil.move(os.path.join(folder_path, img), train_folder_path)

        for img in validation_images:
            shutil.move(os.path.join(folder_path, img), validation_folder_path)

print("Train and validation sets have been created.")
