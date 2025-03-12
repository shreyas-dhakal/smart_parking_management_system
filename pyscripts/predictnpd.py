import numpy as np
import cv2
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#Load the trained model
model = load_model('C:\\Users\\Shopnil\\Desktop\\Project\\venv\\nepalicharacter_detect.keras')
#model = load_model('C:\\Users\\Shopnil\\Desktop\\Project\\venv\\en.keras')

#Input Data
def prepare_image(file):
    img_path = 'C:\\Users\\Shopnil\\Desktop\\char\\'
    img = image.load_img(img_path + file, target_size=(64, 64), color_mode='grayscale')  # Adjust target size
    img_array = image.img_to_array(img)

    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Batch dimensions

    if img_array.shape[-1] == 1:
        img_array = np.repeat(img_array, 1, axis=-1)


    plt.imshow(img_array[0, :, :, 0], cmap='gray')  # Indexing to remove batch dimension and select single channel
    plt.axis('off')  # Hide the axis
    plt.show()

    return img_array

#actual image file
img = prepare_image('31.jpg')

#Make Predictions
predictions = model.predict(img)

predicted_class = np.argmax(predictions, axis=1)

#Interpret the Output
class_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ba', 'cha', 'pa']  #actual class names
#class_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#class_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
predicted_class_name = class_labels[predicted_class[0]]
print(f'The predicted class is: {predicted_class_name}')