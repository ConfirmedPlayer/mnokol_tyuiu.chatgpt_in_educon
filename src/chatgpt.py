import openai

from config import CHATGPT_SYSTEM_PROMPT, CHATGPT_TOKEN


class ChatGPT:
    def __init__(self, system_prompt: str = CHATGPT_SYSTEM_PROMPT) -> None:
        self.system_prompt = system_prompt
        openai.api_key = CHATGPT_TOKEN

    async def ask(self, message: str):
        try:
            request = await openai.ChatCompletion.acreate(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': message}
                ])
            response = request.choices[0].message.content
            return response
        except openai.OpenAIError:
            return 'Произошла ошибка на стороне ChatGPT.'
