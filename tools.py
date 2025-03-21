import os
from dotenv import load_dotenv
from openai import OpenAI

# Carga las variables desde el archivo .env
load_dotenv()

# Obtiene la clave desde la variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Asegúrate de que no sea None (opcional)
if not api_key:
    raise ValueError("Falta la variable de entorno OPENAI_API_KEY")

openai_client = OpenAI(api_key=api_key)

def traducir_texto(texto_original):
    prompt = f"Traduce el siguiente texto al inglés:\n\n'{texto_original}'"

    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un traductor experto del español al inglés."},
            {"role": "user", "content": prompt}
        ]
    )

    resultado = completion.choices[0].message.content.strip()
    return resultado

def generar_audio_openai(texto, archivo_audio, voz="nova"):
 # 📂 Asegurar que el archivo siempre esté en "static/audio/"
    if not archivo_audio.startswith("static/audio/"):
        archivo_audio = f"static/audio/{archivo_audio}"

    response = openai_client.audio.speech.create(
        model="tts-1-hd",
        voice=voz,
        input=texto
    )

    response.stream_to_file(archivo_audio)

    # 🔍 Debug: Imprimir la ruta donde se guarda el archivo
    print(f"🔊 Archivo de audio guardado en: {archivo_audio}")

    return archivo_audio  # Devuelve la ruta correcta
