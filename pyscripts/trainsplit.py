import os
import shutil
import random

def split_dataset(folder_path, train_ratio=0.8):
    # Creating directories for the train and validation sets
    train_dir = os.path.join(folder_path, 'train')
    val_dir = os.path.join(folder_path, 'valid')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    # Get all image files
    all_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(all_files)

    # Splitting the dataset
    split_index = int(len(all_files) * train_ratio)
    train_files = all_files[:split_index]
    val_files = all_files[split_index:]

    # Function to copy files
    def copy_files(files, destination):
        for file in files:
            # Copy image
            shutil.copy2(os.path.join(folder_path, file), destination)

            # Copy corresponding label file
            base_name = os.path.splitext(file)[0]
            label_file = base_name + '.txt'
            label_path = os.path.join(folder_path, label_file)
            if os.path.exists(label_path):
                shutil.copy2(label_path, destination)

    # Copy files to the respective directories
    copy_files(train_files, train_dir)
    copy_files(val_files, val_dir)

    print(f"Dataset split into {len(train_files)} training and {len(val_files)} validation samples.")

folder_path = 'C:\\Users\\Shopnil\\Desktop\\2'
split_dataset(folder_path, train_ratio=0.8)
