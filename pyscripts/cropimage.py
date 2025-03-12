import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCropper:
    def __init__(self, root, image_files):
        self.root = root
        self.image_files = image_files
        self.index = 0
        self.save_directory = None
        
        #Canvas
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.select_area)
        self.canvas.bind("<B1-Motion>", self.extend_area)
        self.canvas.bind("<ButtonRelease-1>", self.perform_crop)
        
        # Load the first image
        self.load_image()

    def load_image(self):
        if self.index < len(self.image_files):
            filepath = self.image_files[self.index]
            self.image = Image.open(filepath)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        else:
            self.root.destroy()

    def select_area(self, event):
        # Record the starting position
        self.x_start, self.y_start = event.x, event.y
        self.crop_rectangle = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_start, self.y_start, outline='red')

    def extend_area(self, event):
        # Update the crop rectangle
        self.canvas.coords(self.crop_rectangle, self.x_start, self.y_start, event.x, event.y)

    def perform_crop(self, event):
        # Get the coordinates
        x1, y1, x2, y2 = self.canvas.coords(self.crop_rectangle)
        
        # Crop the image and display it
        cropped_image = self.image.crop((x1, y1, x2, y2))
        tk_cropped_image = ImageTk.PhotoImage(cropped_image)
        self.canvas.create_image(event.x, event.y, image=tk_cropped_image, anchor=tk.NW)
        
        # Save the cropped image
        if not self.save_directory:
            self.save_directory = filedialog.askdirectory(title="Select Folder to Save Cropped Images")
        
        if self.save_directory:
            base_filename = os.path.basename(self.image_files[self.index])
            name, ext = os.path.splitext(base_filename)
            cropped_filename = os.path.join(self.save_directory, f"{name}_cropped{ext}")
            cropped_image.save(cropped_filename)
            print(f"Cropped image saved as {cropped_filename}")

        # Move to the next image
        self.index += 1
        self.canvas.delete("all")  # Clear canvas
        self.load_image()  # Load  next image

# main window
root = tk.Tk()
root.title("Batch Image Cropper")

folderpath = filedialog.askdirectory(title="Select Folder containing Images")
if folderpath:
    image_files = [os.path.join(folderpath, f) for f in os.listdir(folderpath) if f.endswith(('.jpg', '.jpeg', '.png'))]
    cropper = ImageCropper(root, image_files)

root.mainloop()