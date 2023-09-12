from keras.preprocessing.image import ImageDataGenerator
import cv2
import os
import numpy as np

def create_data_generators(data_dir, classes, img_width, img_height, batch_size, validation_split):
    def load_and_preprocess_image(image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
        img = cv2.resize(img, (img_width, img_height))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=-1)  # Add channel dimension
        return img

    # Generate the list of image files and corresponding labels
    image_files = []
    labels = []
    for i, class_name in enumerate(classes):
        class_dir = os.path.join(data_dir, class_name)
        labels.extend([i] * len(os.listdir(class_dir)))  # Assign the label i to all images in this class
        image_files.extend([os.path.join(class_dir, f) for f in os.listdir(class_dir)])

    # Apply preprocessing to all images
    preprocessed_images = [load_and_preprocess_image(image_path) for image_path in image_files]

    # Convert labels to numpy array
    labels = np.array(labels)

    # Shuffle the data
    shuffled_indices = np.random.permutation(len(preprocessed_images))
    preprocessed_images = np.array(preprocessed_images)[shuffled_indices]
    labels = labels[shuffled_indices]

    # Create a data generator
    datagen = ImageDataGenerator(rescale=1.0/255.0, validation_split=validation_split)
    
    train_data_generator = datagen.flow(x=preprocessed_images, y=labels, batch_size=batch_size, subset='training')
    validation_data_generator = datagen.flow(x=preprocessed_images, y=labels, batch_size=batch_size, subset='validation')

    return train_data_generator, validation_data_generator
