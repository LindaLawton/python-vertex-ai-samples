import os.path

from PIL import Image


class MaskSettings:
    """
    A class to store border settings.
    """

    def __init__(self, top=10, bottom=10, left=10, right=10):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right


def pad_image_with_mask(image_path, output_path, mask_settings):
    """
    Expands an image with custom border sizes for each side.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the output image file.
        :param mask_settings:
    """
    try:
        color = "black"  # mask always black
        original_image = Image.open(image_path)
        original_width, original_height = original_image.size

        new_width = original_width + mask_settings.left + mask_settings.right
        new_height = original_height + mask_settings.top + mask_settings.bottom

        new_image = Image.new("RGB", (new_width, new_height), color)

        paste_x = mask_settings.left
        paste_y = mask_settings.top

        new_image.paste(original_image, (paste_x, paste_y))

        new_image.save(output_path)

        print(f"Image expanded and saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_mask_image(image_path, output_path, mask_settings):
    """
    Creates a new image with a black center and white borders.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the output image file.
        :param mask_settings:
    """
    try:
        original_image = Image.open(image_path)
        original_width, original_height = original_image.size

        new_width = original_width + mask_settings.left + mask_settings.right
        new_height = original_height + mask_settings.top + mask_settings.bottom

        new_image = Image.new("RGB", (new_width, new_height), "white")

        paste_x = mask_settings.left
        paste_y = mask_settings.top

        black_center = Image.new("RGB", (original_width, original_height), "black")

        new_image.paste(black_center, (paste_x, paste_y))

        new_image.save(output_path)

        print(f"Image with white border and black center saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage:
if __name__ == "__main__":
    input_image_path = os.path.join("..", "testData", "outpainting_output-image.png")
    output_image_path = "output_file.jpg"  # Replace with your desired output image path.

    # Create a BorderSettings object
    my_mask_settings = MaskSettings(top=20, bottom=30, left=40, right=50)

    # Example: 10 pixels on all sides, black border
    pad_image_with_mask(input_image_path, output_image_path, my_mask_settings)

    # Create a 200x150 black rectangle with 50 pixel white borders on all sides.
    create_mask_image(input_image_path, output_image_path.replace(".jpg", "_mask.jpg"), my_mask_settings)
