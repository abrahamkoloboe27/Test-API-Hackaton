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
from utils_hk import *


def main():
    st.title("Testeur d'API E-Tourist")

    # Sélection de la route de l'API
    route = st.sidebar.selectbox("Choisissez une route de l'API", [
        "/audio_to_text/",
        "/texte_en_to_texte_fr/",
        "/texte_fr_to_texte_en/",
        "/texte_fr_to_texte_yo/",
        "/texte_yo_to_texte_fr/",
        "/transcribe_fongbe/",
        "/transcribe_yoruba/",
        "/describe_monument/",
        "/tts_yoruba/"
    ])
    if route == "/texte_en_to_texte_fr/" :
      texte = st.text_input("Texte en Anglais")
      if st.button('Traduire') : 
        traducteur = Translator()
        traduction = traducteur.translate(texte, src='en', dest='fr').text
        st.write(traduction)
    if route == "/texte_fr_to_texte_en/" : 
      texte = st.text_input("Texte en francais")
      if st.button('Translate') : 
        with st.spinner("Un instant...."):
          traducteur = Translator()
          traduction = traducteur.translate(texte, src='fr', dest='en').text
          st.write(traduction)
    if route == "/texte_fr_to_texte_yo/" : 
      texte = st.text_input("Texte en Yoruba")
      if st.button('Translate') : 
        with st.spinner("Un instant...."):
          traducteur = Translator()
          traduction = traducteur.translate(texte, src='fr', dest='yo').text
          st.write(traduction)
    if route == "/texte_yo_to_texte_fr/" : 
      texte = st.text_input("Texte en Yoruba")
      if st.button('Translate') : 
        with st.spinner("Un instant...."):
          traducteur = Translator()
          traduction = traducteur.translate(texte, src='yo', dest='fr').text
          st.write(traduction)

    if route == "/transcribe_fongbe" : 
      audio = st.file_uploader("Téléchargez un fichier audio ", type=["wav", "mp3"])
      if audio is not None : 
        st.audio(audio)
        with st.spinner("Un instant...."):
          text = transcribe_fongbe(audio)
          st.write(text["text"])
    if route == "/transcribe_yoruba/" : 
      audio = st.file_uploader("Téléchargez un fichier audio ", type=["wav", "mp3"])
      if audio is not None : 
        st.audio(audio)
        with st.spinner("Un instant...."):
          text = transcribe_fongbe(audio)
          st.write(text["text"])
    if route == "/describe_monument/" :
      image_file = st.sidebar.file_uploader("Téléchargez une image", type=["jpg", "jpeg", "png"])
      with st.expander("Image", False) : 
        if image_file is not None :
          st.image(image_file)
      if st.sidebar.button("Décrire"): 
        text = describe_monument(image_file)
        col_1, col_2 = st.columns(2)
        col = 1
        for language in text.keys()  :
          if col == 1 : 
            with col_1 : 
              with st.expander(f""":blue[{language}]""", False):
                st.subheader(f""":blue[{language}]""")
                st.write(text[language])
                col = 2
          else : 
            with col_2 : 
              with st.expander(f""":blue[{language}]""", False):
                st.subheader(f""":blue[{language}]""")
                st.write(text[language])
                col = 1
    if route == "/audio_to_text/" : 
      audio = st.file_uploader("Téléchargez un fichier audio ", type=["wav", "mp3"])
    if route == "/tts_yoruba/":
      texte_ecrit = st.text_input("Entrez le texte à convertir en audio en yoruba :")
      if st.button("Convertir en audio"):
        tts_yoruba(texte_ecrit)
    if route == "/audio_to_text/":
        # Téléchargement du fichier audio
        audio_file = st.file_uploader("Téléchargez le fichier audio à transcrire", type=["wav", "mp3"])

        if audio_file:
            # Transcription du fichier audio
            transcription = audio_to_text(audio_file)

            # Affichage de la transcription
            st.write("Transcription :", transcription)





if __name__ == "__main__":
    with st.sidebar : 
        st.markdown("""
        ## Auteur
        :blue[Abraham KOLOBOE]
        * Email : <abklb27@gmail.com>
        * WhatsApp : +229 91 83 84 21
        * Linkedin : [Abraham KOLOBOE](https://www.linkedin.com/in/abraham-zacharie-koloboe-data-science-ia-generative-llms-machine-learning)
                    """)
    main()
