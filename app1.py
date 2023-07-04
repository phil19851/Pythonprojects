import os
import io
from google.cloud import vision

# Set the path to the folder containing the images
folder_path = "C:\\Projects\\Searchengine\\imagetotext\\images"

# Set the path to your Google Cloud service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Projects\\Searchengine\\imagetotext\\healthy-catfish-350100-53f09d76f28c.json"

# Create a client for the Vision API
client = vision.ImageAnnotatorClient()

# Create an empty text pad to store the converted text from all images
text_pad = ""

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Load the image into memory
        with io.open(file_path, "rb") as image_file:
            file_content = image_file.read()

        # Perform text detection on the image
        image = vision.Image(content=file_content)
        response = client.document_text_detection(image=image)

        # Extract the text from the response
        text_annotations = response.full_text_annotation.text

        # Append the text to the text pad
        text_pad += text_annotations + "\n"

# Print the text pad containing the converted text from all images
print(text_pad)
# Set the path to save the text file
output_file_path = "C:\\Projects\\Searchengine\\imagetotext\\output_ds160.txt"

# Save the text pad to a file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(text_pad)

print("Text file saved successfully.")

