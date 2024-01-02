import os
import re

from llama_cpp import Llama
from transformers import HfAgent
from logibot.loggerbot import logger

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIRECTORY, "model-q8_0.gguf")
LLM = Llama(model_path=MODEL_PATH, n_ctx=1024)
AGENT = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoder")

REPLIC_ERROR = 'Ошибка при обработке запроса'


async def message_AI(text: str):
    '''
        Функция, которая обрабатывает вопрос пользователя с помощью искусственного интеллекта (AI).

        Аргументы:
            text (str): Вопрос пользователя.

        Возвращает:
            str: Ответ AI на вопрос пользователя.

        Выполняет следующие действия:
            1. Записывает вопрос пользователя в лог соответствующего уровня отладки.
            2. Обрабатывает вопрос с помощью модели AI и получает ответ.
            3. Записывает полученный ответ в лог соответствующего уровня отладки.
            4. Возвращает ответ AI на вопрос пользователя.

        Исключения:
            Если происходит ошибка при обработке запроса, записывает ее в лог ошибок и возвращает сообщение об ошибке.
        '''
    try:
        logger.debug(f'Получен ВОПРОС: {text}')
        output = LLM(text, max_tokens=2024,
                     echo=False)
        text = output["choices"][0]["text"].strip()
        result = re.search(r'(?<=bot\s)(.*)', text).group(1)
        logger.debug(f'Получен ОТВЕТ: {result[:100]}')
        return result
    except Exception as e:
        logger.error(f'Ошибка при обработке запроса: {e}')
        return REPLIC_ERROR
