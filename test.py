

def translate(data, language):
    translated = GoogleTranslator(source='auto', target=language).translate(data)

    print(translated)
    return translated