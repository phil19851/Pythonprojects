#!/usr/bin/env python
# coding: utf-8

# In[27]:


import os, io
import pandas as pd
from google.cloud import vision
from google.cloud import vision_v1
# os.chdir("C:\\Projects\\Searchengine\\imagetotext\\")

# In[28]:


os.chdir("C:\\Projects\\Searchengine\\imagetotext\\images\\")


# In[29]:


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Projects\\Searchengine\\imagetotext\\healthy-catfish-350100-53f09d76f28c.json"


# In[30]:


client = vision.ImageAnnotatorClient()


# In[31]:


folder_path=os.getcwd()
image_path = "image_1.png"
file_path = os.path.join(folder_path,image_path)


# In[32]:


# load image into memory
with io.open(file_path,"rb") as image_file:
    file_content = image_file.read()

# perform text detection from the image
image_detail = vision.Image(content=file_content)
response = client.document_text_detection(image=image_detail)

# print text from the dcoment
doctext = response.full_text_annotation.text
print(doctext)


# In[ ]:




