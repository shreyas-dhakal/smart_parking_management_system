import os
import shutil
from tkinter import Tk, Label, PhotoImage, mainloop
from PIL import Image, ImageTk

source_folder = 'C:\\Users\\Shopnil\\Desktop\\DATASETCROPPED'
main_destination_folder = 'C:\\Users\\Shopnil\\Desktop\\SORTED'

sub_folders = {
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H',
    'i': 'I',
    'j': 'J',
    'k': 'K',
    'l': 'L',
    'm': 'M',
    'n': 'N',
    'o': 'O',
    'p': 'P',
    'q': 'Q',
    'r': 'R',
    's': 'S',
    't': 'T',
    'u': 'U',
    'v': 'V',
    'w': 'W',
    'x': 'X',
    'y': 'Y',
    'z': 'Z',
    '/': 'trash', #for unwanted images trash
}

destination_folders = {}
for key, sub_folder in sub_folders.items():
    full_path = os.path.join(main_destination_folder, sub_folder)
    destination_folders[key] = full_path
    if not os.path.exists(full_path):
        os.makedirs(full_path)

def handle_keypress(event):
    key = event.char
    if key in destination_folders:
        destination = destination_folders[key]
        shutil.move(current_image_path, os.path.join(destination, current_image_name))
        root.quit()

root = Tk()
root.title("Image Sorter")
image_label = Label(root)
image_label.pack()

for current_image_name in os.listdir(source_folder):
    current_image_path = os.path.join(source_folder, current_image_name)
    if not os.path.isfile(current_image_path):
        continue

    img = Image.open(current_image_path)
    img.thumbnail((800, 800), Image.Resampling.LANCZOS) 
    photo = ImageTk.PhotoImage(img)

    image_label.config(image=photo)
    image_label.image = photo

    root.bind('<Key>', handle_keypress)
    mainloop()

print("Image sorting complete.")
