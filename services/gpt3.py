
import openai 
import config

class GPT:
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY

    def generate_response(self, text_input):
        # Generate a response using ChatGPT
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": config.GPT3_SYSTEM_MESSAGE},
                {"role": "user", "content": text_input}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
