from PIL import Image
import os

def convert_bmp_to_jpeg(folder_path):
    
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".bmp"):
            file_path = os.path.join(folder_path, filename)

            with Image.open(file_path) as img:
                rgb_img = img.convert('RGB')

                new_filename = os.path.splitext(filename)[0] + ".jpeg"

                rgb_img.save(os.path.join(folder_path, new_filename), "JPEG")

                print(f"Converted {filename} to {new_filename}")

folder_path = 'C://Users//Shopnil//Desktop//1'
convert_bmp_to_jpeg(folder_path)
