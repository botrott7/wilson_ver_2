from config.config import API_YAN_LANDS
import aiohttp
from logibot.loggerbot import logger

async def translate_word(lang, text):
    if lang == 'ru-ru-syn':
        lang = 'ru-ru'
        syn_flag = True
    else:
        syn_flag = False

    try:
        url = f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={API_YAN_LANDS}&lang={lang}&text={text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'def' in data:
                        definitions = data['def']
                        translation_text = ""
                        synonym_text = ""
                        for definition in definitions:
                            if 'text' in definition:
                                logger.debug(f"Определение: {definition['text']}")
                            if 'tr' in definition:
                                translations = definition['tr']
                                for translation in translations:
                                    if syn_flag:
                                        if 'syn' in translation:
                                            synonyms = translation['syn']
                                            for synonym in synonyms:
                                                if 'text' in synonym:
                                                    synonym_text += f"{synonym['text']}, "
                                        if synonym_text != "":
                                            return f"Синонимы: {synonym_text}"

                                    if 'text' in translation:
                                        translation_text += translation['text'] + ", "
                                        return translation_text[:-2]

                                    else:
                                        return "Нет определений для данного слова"
                else:
                    return f"Ошибка при получении данных: {response.status}"
    except Exception as e:
        logger.exception(f"Ошибка при выполнении запроса: {str(e)}")
