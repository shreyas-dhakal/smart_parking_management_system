import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

train_data_dir = 'C:\\Users\\Shopnil\\Desktop\\FE\\train'
validation_data_dir = 'C:\\Users\\Shopnil\\Desktop\\FE\\valid'

def scheduler(epoch, lr):

    if epoch < 10:
        return lr
    else:
        return lr * tf.math.exp(-0.1)

callback = tf.keras.callbacks.LearningRateScheduler(scheduler)

train_datagen = ImageDataGenerator(
    rescale=1./255,   # Normalize the image pixel
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(64, 64),
    batch_size=16,
    class_mode='categorical',
    color_mode='grayscale'
)

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(64, 64),
    batch_size=16,
    class_mode='categorical',
    color_mode='grayscale'
)

model = Sequential()

# First Convolutional Block
model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 1), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

# Second Convolutional Block
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

# Third Convolutional Block
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flattening
model.add(Flatten())

# Full connection
model.add(Dense(units=256, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))  # Dropout layer

model.add(Dense(units=128, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))  # Additional Dropout layer

model.add(Dense(units=36, activation='softmax')) 

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='categorical_crossentropy', metrics=['accuracy'])

#Early Stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

model.fit(
    train_generator,
    steps_per_epoch=2304,  # Number of images in training set
    epochs=200,
    validation_data=validation_generator,
    validation_steps=578,  # Number of images in validation set
    callbacks=[callback, early_stopping]
)

model.save('enlast.keras')