from dotenv import load_dotenv
import os
from vertexai.vision_models._vision_models import ImageGenerationModel
load_dotenv()


def create_image(prompt: str, save_to_path: str):

    generation_model = ImageGenerationModel.from_pretrained(os.getenv("IMAGE_GEN_MODEL"))
    response = generation_model.generate_images(
        prompt=prompt,
        negative_prompt="people",
        aspect_ratio="1:1",
        number_of_images=1,
        seed=123456789,
        add_watermark=False,
        safety_filter_level="block_few",
        person_generation="allow_adult"
    )
    print(len(response.images))
    image = response.images[0]
    image.save(save_to_path)


create_image("I quiet sea view, with sail boats in the distance and a island", "sea.png")
