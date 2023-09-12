import os
import cv2

# Define the paths for the original and processed data directories
original_data_dir = 'data'
processed_data_dir = 'processed_data'

# Create the processed data directory
os.makedirs(processed_data_dir, exist_ok=True)

# Get the list of subfolders in the original data directory
subfolders = os.listdir(original_data_dir)

# Loop through each subfolder
for subfolder in subfolders:
    # Define the paths for the original and processed subfolders
    original_subfolder_path = os.path.join(original_data_dir, subfolder)
    processed_subfolder_path = os.path.join(processed_data_dir, subfolder)
    
    # Create the processed subfolder
    os.makedirs(processed_subfolder_path, exist_ok=True)
    
    # Get the list of image files in the original subfolder
    image_files = os.listdir(original_subfolder_path)
    
    # Loop through each image file
    for image_file in image_files:
        # Define the paths for the original and processed images
        original_image_path = os.path.join(original_subfolder_path, image_file)
        processed_image_path = os.path.join(processed_subfolder_path, image_file)
        
        # Load the image with transparency (including alpha channel)
        img = cv2.imread(original_image_path, cv2.IMREAD_UNCHANGED)
        
        # Extract the alpha channel (transparency)
        alpha_channel = img[:, :, 3]
        
        # Set transparent pixels to white
        img[alpha_channel == 0] = [255, 255, 255, 255]

        img_gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)
        
        # Save the processed image
        cv2.imwrite(processed_image_path, img_gray)

print("Images converted and saved in 'processed_data' directory.")
