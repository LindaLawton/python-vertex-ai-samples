from dotenv import load_dotenv
import os
from google import genai
from google.genai.types import (
    Image,
    Part
)
load_dotenv()

def get_image_bytes_from_file(image_path):
    try:
        with open(image_path, "rb") as image_file:  # "rb" for read binary
            image_bytes = image_file.read()
            return image_bytes
    except FileNotFoundError:
        print(f"Error: Image file '{image_path}' not found.")
        return None  # Or raise the exception if you prefer
    except Exception as e: # Catch other potential errors (permissions, etc.)
        print(f"An error occurred: {e}")
        return None


response_schema = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "bank_name_name": {"type": "STRING"},
            "bank_address": {"type": "STRING"},
            "bank_phonenumber": {"type": "STRING"},
            "account_owner_name": {"type": "STRING"},
            "account_owner_address": {"type": "STRING"},
            "statement_period": {"type": "STRING"},
            "statement_account_number": {"type": "STRING"},
            "transactions": {"type": "ARRAY", "items": {
                                                    "type": "OBJECT",
                                                    "properties": {
                                                        "date": {"type": "STRING"},
                                                        "description": {"type": "STRING"},
                                                        "ref": {"type": "STRING"},
                                                        "withdrawals": {"type": "STRING"},
                                                        "deposits": {"type": "STRING"},
                                                        "balance": {"type": "STRING"},
                                                    },
                                                    }
                             },
        },
        "required": ["account_owner_name"],
    },
}


PROJECT_ID = os.getenv("PROJECT_ID")
print("Cloud project id is: " + PROJECT_ID)
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# Get the file data
image_path = os.path.join("..","testData", "BankStatementChequing.png")

# Read content from a local file
with open(image_path, "rb") as f:
    local_file_img_bytes = f.read()

prompt = [
        "Parse this bank statement",
        Part.from_bytes(data=local_file_img_bytes, mime_type="image/png"),
    ]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": response_schema,
    },
)

print(response.text)
# Example output:
# [
#     {
#         "ingredients": [
#             "2 1/4 cups all-purpose flour",
#             "1 teaspoon baking soda",
#             "1 teaspoon salt",
#             "1 cup (2 sticks) unsalted butter, softened",
#             "3/4 cup granulated sugar",
#             "3/4 cup packed brown sugar",
#             "1 teaspoon vanilla extract",
#             "2 large eggs",
#             "2 cups chocolate chips",
#         ],
#         "recipe_name": "Chocolate Chip Cookies",
#     }
# ]