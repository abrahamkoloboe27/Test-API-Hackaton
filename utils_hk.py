import streamlit as st
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import PlainTextResponse
import speech_recognition as sr
import audioread
import wave
import os 
import tempfile
from googletrans import Translator
import requests
import base64
from IPython.display import Audio


@st.cache_resource
def tts_yoruba(texte_ecrit):
    payload = {
        "inputs": texte_ecrit,
    }
    audio_bytes = query(payload)
    #audio = Audio(audio_bytes)
    # Convertir les données audio en format base64 pour Streamlit
    #audio_data = base64.b64encode(audio_bytes)
    audio_format = ".wav"

    # Afficher l'audio dans Streamlit
    st.audio(audio_bytes, format=audio_format)

@st.cache_resource
def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-yor"
    headers = {"Authorization": "Bearer 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"}

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

@st.cache_resource
def convert_to_wav(audio_file_path, audio_to_transcript):
    with audioread.audio_open(audio_file_path) as source:
        with wave.open(audio_to_transcript, 'w') as destination:
            destination.setnchannels(source.channels)
            destination.setframerate(source.samplerate)
            destination.setsampwidth(2)

            for buffer in source:
                destination.writeframes(buffer)

@st.cache_resource
def audio_to_text(audio_to_transcript):
    r = sr.Recognizer()
    
    with sr.AudioFile(audio_to_transcript) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio, language='fr-FR')
        return text
    except sr.UnknownValueError:
        return "Google Web Speech API n'a pas pu comprendre l'audio"
    except sr.RequestError as e:
        return f"Impossible d'obtenir les résultats de Google Web Speech API; {e}"

@st.cache_resource
def encode_image(image_file):
  return base64.b64encode(image_file.read()).decode('utf-8')
    
@st.cache_resource
def describe_monument(image_file) : 
    api_key = "sk-proj-juI5OZRrhDiiJbszYjqfT3BlbkFJ4jtzTopdB5cJYdTMUhmm"
    try:
        context = "Tu es un guide touristique du Bénin. Je vais te montrer des images de monuments béninois, et tu dois me dire à quel monument cela correspond de facon claire et consise. Evite les expressions comme 'il semblerait'. Aussi , focalise toi uniquement sur le monument et son histoire. Pour tout ce qui est du décor autour evite d'en parler. De facon brève et consise explique l'histoire du monument. Enfin; si cela possible, raconte une petite anecdote sur l'histoire du monument. "
        base64_image = encode_image(image_file)
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": context + "Identifie ce monument et raconte moi son histoire"
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 500
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        texte_francais = response.json()['choices'][0]['message']['content']

        ## On traduit maintenant 

        translator = Translator()

        # Traduction en anglais
        texte_anglais = translator.translate(texte_francais, src='fr', dest='en').text

        # Traduction en espagnol
        texte_espagnol = translator.translate(texte_francais, src='fr', dest='es').text

        # Traduction en yoruba
        texte_yoruba = translator.translate(texte_francais, src='fr', dest='yo').text

        return {
                    'Francais': texte_francais,
                    'Anglais': texte_anglais,
                    'Espagnol': texte_espagnol,
                    'Yoruba': texte_yoruba
                }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")

@st.cache_resource
def transcribe_yoruba(audio):

  try:
    API_URL = "https://api-inference.huggingface.co/models/neoform-ai/whisper-medium-yoruba"
    headers = {"Authorization": "Bearer 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"}

    response = requests.post(API_URL, headers=headers, data=audio)
    return response.json()
    
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")

@st.cache_resource
def transcribe_fongbe(audio):

  try:
    API_URL = "https://api-inference.huggingface.co/models/chrisjay/fonxlsr"
    headers = {"Authorization": "Bearer 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"}

    
    response = requests.post(API_URL, headers=headers, data=audio)
    return response.json()
    
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")
