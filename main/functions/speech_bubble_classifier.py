from keras.preprocessing.image import ImageDataGenerator
from speech_bubble_model import create_model
import cv2

# Define the path to your data folder
data_dir = 'processed_data'

# Define the classes
classes = ['1 - basic', '2 - double', '3 - loud', '4 - thinking', '5 - narration']

# Set the dimensions for input images
img_width, img_height = 150, 150

# Define the batch size
batch_size = 32

# Define the number of epochs
epochs = 20

# Define the percentage of data to use for validation
validation_split = 0.2

# Create data generators for training and validation
datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    validation_split=validation_split,
)

train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training',
    classes=classes
)

validation_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation',
    classes=classes
)

model = create_model(img_width, img_height, classes)

model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

model.save('speech_bubble_recognition_model.keras')
