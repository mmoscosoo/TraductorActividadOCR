import streamlit as st
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
import os

st.set_page_config(page_title="OCR y Texto a Voz", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #101010;
        color: #FFFFFF;
    }

    h1 {
        color: #FF6347 !important;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 2.5em;
    }

    .stButton > button, .stCameraInput, .stRadio > div {
        background-color: #FF6347 !important;
        color: white !important;
        border-radius: 8px;
        border: 1px solid #FF6347;
        font-weight: bold;
    }

    .stSidebar {
        background-color: #1C1C1C !important;
    }

    .stSidebar div, .stSidebar label, .stSidebar span {
        color: white !important;
    }

    .css-1offfwp, .css-1aumxhk {
        color: white !important;
    }

    .stMarkdown {
        font-family: 'Arial', sans-serif;
        font-size: 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("OCR y Conversión de Texto a Voz")

st.markdown("Captura una imagen con texto y conviértelo automáticamente en audio. ¡Es muy fácil!")


img_file_buffer = st.camera_input("Toma una foto para leer el texto")


with st.sidebar:
    apply_filter = st.radio("¿Aplicar filtro?", ('Sí', 'No'))

if img_file_buffer is not None:
  
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)


    if apply_filter == 'Sí':
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

  
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    st.image(img_rgb, caption="Imagen procesada", use_column_width=True)

 
    extracted_text = pytesseract.image_to_string(img_rgb)
    st.subheader("Texto detectado:")
    st.write(extracted_text)

   
    if extracted_text.strip() != "":
        tts = gTTS(extracted_text, lang='es')
        audio_path = "audio_detectado.mp3"
        tts.save(audio_path)

        st.subheader("Escuchar el texto:")
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        audio_file.close()
        os.remove(audio_path)
    else:
        st.warning("No se detectó texto en la imagen. Intenta con una imagen más clara.")
