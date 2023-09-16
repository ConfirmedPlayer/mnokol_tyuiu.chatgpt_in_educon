import openai

from config import CHATGPT_SYSTEM_PROMPT, CHATGPT_TOKEN
import json


system_prompt = '''
Пользователь отправляет тебе вопрос из тестирования, и варианты ответа.
Ты должен внимательно изучить вопрос, и выбрать ответ из тех, который тебе дал пользователь.
Твой выбор должен быть максимально точным. Внимательно подумай перед тем как выбирать ответ.
Ты должен просто отправить ответ, точно в таком же виде, какой он был написан в варианте ответов.
'''


chatgpt_question_prompt = '''
{question}


'''


class ChatGPT:
    def __init__(self, system_prompt: str = CHATGPT_SYSTEM_PROMPT) -> None:
        self.system_prompt = system_prompt
        openai.api_key = CHATGPT_TOKEN

    async def ask(self, message: str):
        try:
            if message.startswith('/решение_теста'):
                edited_message = message.replace('/решение_теста ', '', 1)

                jsonified_message = json.loads(edited_message)

                question = jsonified_message['question']
                answers = jsonified_message['answers']
                final_prompt = chatgpt_question_prompt.format(question=question)

                for answer in answers:
                    final_prompt += answer + '\n'
                print(f'\nfinal prompt is: {final_prompt}\n')

                request = await openai.ChatCompletion.acreate(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': final_prompt}
                    ]
                )
                response = request.choices[0].message.content

                jsonified_message['answer'] = response
                jsonified_message['solved'] = True

                new_json = json.dumps(jsonified_message, ensure_ascii=False)
                return new_json

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
