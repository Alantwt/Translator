import openai
import os
import speech_recognition as sr
from gtts import gTTS
import warnings
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv")
from playsound import playsound


openai.api_key = "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"

# Settings
recod = sr.Recognizer()
mic = sr.Microphone()
lang_dic = {
    "español":"es",
    "ingles":"en",
    "frances":"fr"
}

def main():

    while True:
        
        text_lang = user_input()
        translate_text = translate(text_lang[0],text_lang[1])
        speaker(translate_text,text_lang[1])

        input("Press any kay to continue....\n")
        os.system("cls" if os.name == "nt" else "clear")



def user_input() -> tuple:
    opc = input("\nTraduccion por default(a ingles)?, Y/N\n")
    if opc == "N" or opc == "n":
        while True:
            lang_translate = input("A que idioma quieres traducirlo?: ")
            if lang_translate in lang_dic.keys():
                break
            else: print("idioma no soportado")
    else: 
        lang_translate = "ingles"

    while True:
        print("Te escucho...\n")
        with mic as source:
            audio = recod.listen(source)
        try:    
            text = recod.recognize_google(audio,show_all=False,language="es-ES")
            return (text,lang_translate)
        except sr.UnknownValueError:
            print("No se pudo reconocer el audio.")


def translate(ask:str="none", lang:str="español") -> str:

    print(ask)
    if ask == "none":
        return "no se recibio ningun parametro"
    else:
        ask = f"Solo escribe la traduccion a {lang} de: " + ask
        response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=ask,
                n=1,
                max_tokens=2048
            )
        return response.choices[0].text



def speaker(text:str="none",lang:str="ingles"):
    if text == "none":
        return
    else:
        print("Esto esta traducido al idioma: " + lang)
        speech = gTTS(text=text,lang=lang_dic[lang],slow=False)
        speech.save("..\Translator\data\\texto.mp3")
        playsound("..\Translator\data\\texto.mp3")


if __name__ == "__main__":
    main()