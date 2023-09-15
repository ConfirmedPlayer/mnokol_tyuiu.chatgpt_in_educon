import openai

from config import CHATGPT_SYSTEM_PROMPT, CHATGPT_TOKEN


system_prompt = '''
Пользователь отправляет тебе вопрос из тестирования, и варианты ответа.
Ты должен внимательно изучить вопрос, и выбрать ответ из тех, который тебе дал пользователь.
Ты должен просто отправить ответ, точно в таком же виде, какой он был написан в варианте ответов.
Если вариантов ответа нет, ты должен просто предоставить ответ.
'''


class ChatGPT:
    def __init__(self, system_prompt: str = CHATGPT_SYSTEM_PROMPT) -> None:
        self.system_prompt = system_prompt
        openai.api_key = CHATGPT_TOKEN

    async def ask(self, message: str):
        try:
            if message.startswith('/решение_теста'):
                edited_message = message.replace('/решение_теста ', '', 1)
                request = await openai.ChatCompletion.acreate(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': edited_message}
                    ]
                )
                response = request.choices[0].message.content
                return response

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
