from config.config import API_YAN_LANDS
import requests

def translate_word(lang, text):
    url = f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={API_YAN_LANDS}&lang={lang}&text={text}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if 'def' in data:
            definitions = data['def']

            for definition in definitions:
                if 'text' in definition:
                    print(f"Определение: {definition['text']}")

                if 'tr' in definition:
                    translations = definition['tr']
                    translation_text = ""

                    for translation in translations:
                        if 'text' in translation:
                            translation_text += translation['text'] + ", "

                    if translation_text != "":
                        return f"Переводы: {translation_text[:-2]}"  # удалить последнюю запятую и пробел

                if 'tr' in definition:
                    translations = definition['tr']
                    synonym_text = ""

                    for translation in translations:
                        if 'syn' in translation:
                            synonyms = translation['syn']

                            for synonym in synonyms:
                                if 'text' in synonym:
                                    synonym_text += f"{synonym['text']}, "

                    if synonym_text != "":
                        return f"Синонимы: {synonym_text}"

        else:
            return "Нет определений для данного слова"

    else:
        return "Ошибка при получении данных:", response.status_code
