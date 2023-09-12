import tensorflow as tf
from keras.preprocessing import image
import numpy as np
from functions.log import log, color, bold

# Load the trained model
model = tf.keras.models.load_model('speech_bubble_recognition_model.keras')

# Define the class labels
class_labels = ['🟦 basic', '🔄 double', '🔊 loud', '📢 announcement', '💭 thinking', '📖 narration']

def classify_image(image_path):
    # Load and preprocess the image
    img = image.load_img(image_path, target_size=(256, 256))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalize the image data

    # Make predictions
    predictions = model.predict(img)

    # Get the predicted class index
    predicted_class_index = np.argmax(predictions)

    # Get the corresponding class label
    predicted_class_label = class_labels[predicted_class_index]

    # Get the percentage likelihood for each class
    class_percentages = predictions[0] * 100.0

    # Find the index of the class with the highest percentage likelihood
    highest_percentage_index = np.argmax(class_percentages)

    # Print the results
    log(bold(" - Class Probabilities - "), True)
    for i, label in enumerate(class_labels):
        if highest_percentage_index != i:
            log(f"{label}: {color('#b32f25',f'{class_percentages[i]:.2f}%')}", True)
        else:
            log(f"{label}: {color('#5ab54e',f'{class_percentages[i]:.2f}%')}", True)

    log(bold(f'The image is classified as: {color("#5ab54e",predicted_class_label)}'), True)
    log(f"", True)