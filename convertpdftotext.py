import os
import io
import tempfile
from PyPDF2 import PdfReader
from google.cloud import vision_v1p3beta1 as vision

# Set the path to your Google Cloud service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Projects\\Searchengine\\imagetotext\\healthy-catfish-350100-53f09d76f28c.json"

# Create a client for the Vision API
client = vision.ImageAnnotatorClient()

# Set the path to your PDF file
pdf_path = "C:\\Projects\\Searchengine\\imagetotext\\pdf\\filing.pdf"

# Create a temporary directory to store the converted images
temp_dir = tempfile.mkdtemp()

# Read the PDF file
with open(pdf_path, "rb") as pdf_file:
    pdf_reader = PdfReader(pdf_file)

    # Iterate over each page of the PDF
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]

        # Convert the page to an image
        image_path = os.path.join(temp_dir, f"page_{page_number}.png")
        page.to_image().save(image_path)

        # Read the image file
        with io.open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Perform text detection on the image
        image = vision.Image(content=image_data)
        response = client.document_text_detection(image=image)

        # Extract the text from the response
        text_annotations = response.full_text_annotation.text

        # Append the text to the text pad
        text_pad += text_annotations + "\n"

# Set the path to save the text file
output_file_path = "C:\\Projects\\Searchengine\\imagetotext\\output_filingdoc.txt"

# Save the text pad to a file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(text_pad)

print("Text file saved successfully.")
print(text_pad)
print("test")
