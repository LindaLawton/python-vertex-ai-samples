from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel, Image, Part
import os
from typing import Optional

load_dotenv()


class VertexService:
    def __init__(self):
        self.model = GenerativeModel(model_name=os.getenv("IMAGE_MODEL_NAME"))

    @staticmethod
    def load_image_from_file(image_path: str) -> Image:
        with open(image_path, 'rb') as file:
            image_bytes = file.read()
        return Image.from_bytes(image_bytes)

    def get_completion(self, image: str, message: Optional[str] = None) -> str:
        response = self.model.generate_content(
            [Part.from_image(Image.load_from_file(image)),
             message])
        # return the response.
        return response.text


class VertexUI:
    def __init__(
            self
    ) -> None:
        self.service = VertexService()

    def single_image_answer(self, image: str, message: Optional[str] = None) -> str:
        if os.path.exists(image):
            return self.service.get_completion(image, message)
        else:
            return f"{image} does not exist."


gemini_image = VertexUI()
image_path = os.path.join("..", "testData", "image.png")
if not os.path.exists(image_path):
    print(f"'{image_path}' doesn't exist.")
else:
    answer = gemini_image.single_image_answer(image_path, "What is the weather like?")
    print(answer)
