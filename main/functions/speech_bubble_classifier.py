from keras.preprocessing import image
from keras.models import load_model
import numpy as np
from functions.log import log, color, bold
import os

# Load the trained model
model = None
number = 4

# Define the class labels
class_labels = ['🟦 basic', '🔄 double', '🔊 loud', '💭 thinking', '📖 narration']

def set_model(value): 
    global model, number
    number = value
    # Define the path to the folder containing the models
    models_folder = "models/trained_models"

    # Get a list of files in the folder
    model_files = os.listdir(models_folder)
    model_files = [file for file in model_files]
    model = load_model(f'models/trained_models/{model_files[value]}')

def classify_images():
    global model
    if (model == None):
        set_model(4)

    models_folder = "output/extracted_bubbles"
    model_files = os.listdir(models_folder)

    log(bold("🚀🚀🚀 STARTED CLASSIFYING SPEECH BUBBLES 🚀🚀🚀"), True)
    for file in model_files:
        # Load and preprocess the image
        img = image.load_img(f"output/extracted_bubbles/{file}", target_size=(256, 256))
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

        log(bold(f'The image {os.path.splitext(file)[0]} is classified as: {color("#5ab54e",predicted_class_label)}'), True)
        log(f"", True)
    
    log(bold("🏁🏁🏁 CLASSIFYING ENDED 🏁🏁🏁"), True)

def classify_image(file, name):
    global model, number
    if (model == None):
        set_model(number)
    
    log(bold(f"Using model {number}"), True)
    # Load and preprocess the image
    img = image.load_img(file, target_size=(256, 256))
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

    log(bold(f'The image {name} is classified as: {color("#5ab54e",predicted_class_label)}'), True)
    log(f"", True)
    return predicted_class_label