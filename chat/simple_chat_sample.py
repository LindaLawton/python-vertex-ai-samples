from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel, Content, Part
import os

load_dotenv()

# Init the chatbot with two prompts, there must be two.

# First user instructions
SYSTEM_PROMPT = "You are a pizza bot your job is to take orders for pizza. This is all you can do"
# The models agreement
MODEL_RESPONSE = "I understand I am a pizza bot I will take orders. For pizza"


class VertexService:
    def __init__(self):
        self.model = GenerativeModel(model_name=os.getenv("TEXT_MODEL_NAME"))

    @staticmethod
    def build_user_prompt_content(message: str, role: str):
        # Define the user's prompt in a Content object that we can reuse in model calls
        return Content(
            role=role,
            parts=[
                Part.from_text(message),
            ],
        )

    @staticmethod
    def add_conversation(history: list[Content], user, model):
        history.append(VertexService().build_user_prompt_content(user, "user"))
        history.append(VertexService().build_user_prompt_content(model, "model"))
        return history

    def get_completion(self,
                       history: list[Content],
                       message: str) -> str:
        # Start the chat with the conversation history
        convo = self.model.start_chat(history=history)

        # send message with the new request from the user.
        convo.send_message(message)

        # return the response
        return convo.history


class ChattyUI:
    def __init__(
            self,
            system_prompt: str = SYSTEM_PROMPT,
            system_prompt_response: str = MODEL_RESPONSE
    ) -> None:
        self.service = VertexService()
        self.system_prompt = system_prompt
        self.system_prompt_response = system_prompt_response

    def close(self):
        self.interface.close()

    def test(self):
        self.service.test()

    def answer(self, message: str, chat_history: list[str]) -> str:
        # Init the chatbot with the starting prompts.
        # Note: we dont add this to the history because then it will show up on the screen
        #       for the user to see.

        system_history = []
        system_history = VertexService().add_conversation(system_history, self.system_prompt,
                                                          self.system_prompt_response)

        # add user and assistant message from history
        for chat in chat_history:

            system_history.append(VertexService().build_user_prompt_content(chat.parts[0].text, chat.role))

        return self.service.get_completion(history=system_history, message=message)


chatty = ChattyUI()

# init chat history
history = []
print(f"History: {history}")
# a new conversation item.
user_says = "I would like a large chease pizza."
print(user_says)
model_says = chatty.answer(user_says, history)
model_response = model_says[-1].parts[0].text
print(model_response)

# Append history
history = VertexService().add_conversation(history, user_says, model_response)
print(f"History: {history}")

user_says = "What is my order?"
print(user_says)
model_says = chatty.answer(user_says, history)
print(model_says[-1].parts[0].text)
