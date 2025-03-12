import os
import re

def update_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                contents = file.read()

            # Replace any number from 0-20 at the start of any line with '0'
            updated_contents = re.sub(r'^\b(4[0]|3[0-9]|[12][0-9]|[0-9])\b ', '0 ', contents, flags=re.MULTILINE)

            if contents != updated_contents:
                with open(file_path, 'w') as file:
                    file.write(updated_contents)
                print(f"Updated {filename}")

directory_path = 'C:\\Users\\Shopnil\\Desktop\\anamolis2.v8i.yolov8\\train\\labels'
update_files_in_directory(directory_path)
