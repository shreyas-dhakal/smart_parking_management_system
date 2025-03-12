import os
import cv2

def extract_images_from_videos(folder_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is a video file
        if file_path.endswith(('.mp4', '.avi', '.mkv')):
            # Read the video file
            cap = cv2.VideoCapture(file_path)

            if not cap.isOpened():
                print(f"Error opening video file: {file_path}")
                continue

            # Get the first frame from the video
            ret, frame = cap.read()

            if not ret:
                print(f"Error reading frame from video file: {file_path}")
                continue

            # Save the extracted frame as an image
            output_filename = os.path.splitext(filename)[0] + '.jpg'
            output_path = os.path.join(output_folder, output_filename)
            cv2.imwrite(output_path, frame)

            cap.release()

            print(f"Image extracted from video: {file_path} --> {output_path}")

if __name__ == "__main__":
    input_folder = "C://Users//Shopnil//Desktop//fyp_dataset_vid"
    output_folder = "C://Users//Shopnil//Desktop//fyp_dataset_img"

    extract_images_from_videos(input_folder, output_folder)