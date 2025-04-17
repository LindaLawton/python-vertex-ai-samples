import base64
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel, Part
from dotenv import load_dotenv
import os

load_dotenv()

TEXT_MODEL_NAME = os.getenv("TEXT_MODEL_NAME")
PROJECT_ID = os.getenv("PROJECT_ID")
vertexai.init(project=PROJECT_ID, location="us-central1")
model = GenerativeModel(TEXT_MODEL_NAME)



prompt = """
You are a highly skilled teacher danish history teacher.  
Your task is to create a quiz for your students.
Your task is to create concise questions and their answers to ensure your students have learned 
 the less on on the page given.
Please examine the given document and create a question and answer.
"""

with open(os.path.join("..", "testData",  "page_10.pdf"), "rb") as f:
    pdf = base64.b64encode(f.read()).decode("utf-8")

pdf_file = Part.from_data(
                mime_type="application/pdf",
                data=pdf)



response = model.generate_content(
        contents=[pdf_file, prompt],
    )


print(response.text)
# Example response:
# Here is a summary of the document in 300 words.
#
# The paper introduces the Transformer, a novel neural network architecture for
# sequence transduction tasks like machine translation. Unlike existing models that rely on recurrent or
# convolutional layers, the Transformer is based entirely on attention mechanisms.
# ...