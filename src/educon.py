import asyncio
import random
from datetime import datetime

import openai
import pytz
from aiohttp import ClientSession
from playwright.async_api import async_playwright

from config import (CHATGPT_TOKEN, EDUCON_API_URL, EDUCON_AUTH_URL,
                    EDUCON_LOGIN, EDUCON_PASSWORD, EDUCON_SESSION_PROFILE_ID,
                    TIMEZONE)


class EduconSession:
    def __init__(self) -> None:
        self._client_session = ClientSession()
        self._session_cookie_value = None
        self._session_key = None

        self.chatgpt_token = CHATGPT_TOKEN
        openai.api_key = self.chatgpt_token

        self.timezone = pytz.timezone(TIMEZONE)

    async def close(self):
        if self._client_session and not self._client_session.closed:
            await self._client_session.close()

    async def _get_educon_messages(self, user_id: int = EDUCON_SESSION_PROFILE_ID):
        params = {'sesskey': self._session_key,
                  'info': 'core_message_get_conversations'}

        headers = {'Cookie': f'MoodleSession={self._session_cookie_value}',
                   'X-Requested-With': 'XMLHttpRequest'}

        json_data = [{
                'index': 0,
                'methodname': 'core_message_get_conversations',
                'args': {
                    'userid': user_id,
                    'type': 1,
                    'limitnum': 51,
                    'limitfrom': 0,
                    'favourites': False
                }
            }]
        async with self._client_session.post(url=EDUCON_API_URL,
                                             params=params,
                                             headers=headers,
                                             json=json_data) as r:
            return await r.json()

    async def _send_educon_message(self,
                                   conversation_id: int,
                                   message: str
                                   ):
        params = {'sesskey': self._session_key,
                  'info': 'core_message_send_messages_to_conversation'}

        headers = {'Cookie': f'MoodleSession={self._session_cookie_value}',
                   'X-Requested-With': 'XMLHttpRequest'}

        json_data = [{
            'index': 0,
            'methodname': 'core_message_send_messages_to_conversation',
            'args': {
                'conversationid': conversation_id,
                'messages': [{
                    'text': message
                }]
            }
        }]
        async with self._client_session.post(url=EDUCON_API_URL,
                                             params=params,
                                             headers=headers,
                                             json=json_data) as r:
            print(f'send message status: {r.status}\nmessage:{message}')

    async def refresh_session(self):
        async with async_playwright() as connection:
            browser = await connection.chromium.launch()
            page = await browser.new_page()

            await page.goto(EDUCON_AUTH_URL)

            await page.locator('[class="btn btn-primary btn-block text-break"]').click()
            await page.locator('[id="email"]').fill(EDUCON_LOGIN)
            await page.locator('[id="password"]').fill(EDUCON_PASSWORD)
            await page.locator('[type="submit"]').click()

            cookie_value = await page.context.cookies(EDUCON_AUTH_URL)
            self._session_cookie_value = cookie_value[0]['value']

            self._session_key = await page.locator('[name="sesskey"]').get_attribute('value')

    async def start_polling(self):
        while True:
            current_hour = datetime.now(self.timezone).hour
            if current_hour in range(8):
                await asyncio.sleep(60)
                continue

            print('getting new messages...')
            messages = await self._get_educon_messages()
            error = messages[0]['error']
            if error:
                print('Auth error was occured\n')
                print(messages)
                await asyncio.sleep(60)
                await self.refresh_session()
                continue

            for conversation in messages[0]['data']['conversations']:
                user_id_from = conversation['messages'][0]['useridfrom']
                if user_id_from == EDUCON_SESSION_PROFILE_ID:
                    print('message from myself. ignoring...')
                    continue

                conversation_id = conversation['id']

                message_text = conversation['messages'][0]['text']\
                    .replace('<p>', '')\
                    .replace('</p>', '')

                request = await openai.ChatCompletion.acreate(model='gpt-3.5-turbo',
                                                              messages=[
                                                                   {'role': 'user',
                                                                    'content': message_text
                                                                    }])
                response = request.choices[0].message.content
                await self._send_educon_message(conversation_id=conversation_id,
                                                message=response)
            await asyncio.sleep(random.randint(15, 30))
