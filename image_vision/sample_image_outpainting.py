import os

import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel
from dotenv import load_dotenv

from image_vision.outpainting_helper import MaskSettings, pad_image_with_mask, create_mask_image

load_dotenv()


#vertexai.init(project=PROJECT_ID, location="us-central1")

def out_paint_image(input_file, mask_file, output_file, prompt):

    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    base_img = Image.load_from_file(location=input_file)
    mask_img = Image.load_from_file(location=mask_file)

    images = model.edit_image(
        base_image=base_img,
        mask=mask_img,
        prompt=prompt,
        edit_mode="outpainting",
    )

    images[0].save(location=output_file, include_generation_parameters=False)

    # Optional. View the edited image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes



# Example usage:
if __name__ == "__main__":
    input_image_path = os.path.join("..", "testData", "outpainting_output-image.png")
    pad_image = "output_file.jpg"  # Replace with your desired output image path.
    pad_image_mask = pad_image.replace(".jpg", "_mask.jpg")
    image_bigger = pad_image.replace(".jpg", "_biger.jpg")

    # Create a BorderSettings object
    my_mask_settings = MaskSettings(top=1000, bottom=1000, left=1000, right=1000)

    # Example: 10 pixels on all sides, black border
    pad_image_with_mask(input_image_path, pad_image, my_mask_settings)

    # Create a 200x150 black rectangle with 50 pixel white borders on all sides.
    create_mask_image(input_image_path, pad_image_mask, my_mask_settings)

    out_paint_image(pad_image, pad_image_mask, image_bigger, "")