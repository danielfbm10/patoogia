
import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from fpdf import FPDF
from datetime import datetime
import json

# Cargar modelo visual
MODEL_PATH = "modelo_patologIA.h5"
model = tf.keras.models.load_model(MODEL_PATH)
class_names = sorted(os.listdir("dataset_patologIA_demo"))

# Cargar descripciones médicas
with open("diagnosticos_info.json", "r", encoding="utf-8") as f:
    info_diagnostico = json.load(f)

# Función para procesar imágenes
def procesar_imagen(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

# Formulario Clínico
def mostrar_formulario():
    preguntas = {
        "Localización de la lesión": ["Labio", "Lengua", "Encía", "Paladar", "Piso de boca", "Mejilla", "Otra"],
        "Tamaño de la lesión": ["< 5 mm", "5–10 mm", "> 10 mm"],
        "Color predominante": ["Blanco", "Rojo", "Mixto", "Pigmentado", "Translúcido"],
        "Dolor presente": ["Sí", "No"],
        "Tiempo de evolución": ["< 1 semana", "1–4 semanas", "> 1 mes"],
        "Crecimiento observado": ["Sí", "No", "No lo sabe"],
        "Consumo de tabaco o alcohol": ["Sí", "No"],
        "Sangrado o supuración": ["Sí", "No"]
    }
    respuestas = {}
    for pregunta, opciones in preguntas.items():
        respuestas[pregunta] = st.selectbox(pregunta, opciones)
    return respuestas

def generar_pdf(diagnostico, info, respuestas):
    nombre_archivo = f"reporte_patologIA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "REPORTE DE DIAGNOSTICO – patologIA".encode('utf-8').decode('latin1'), ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Diagnostico visual sugerido: {diagnostico}".encode('utf-8').decode('latin1'), ln=True)
    pdf.multi_cell(0, 10, f"Clasificacion: {info.get('clasificacion', '-')}".encode('utf-8').decode('latin1'))
    pdf.multi_cell(0, 10, f"Descripcion: {info.get('descripcion', '-')}".encode('utf-8').decode('latin1'))
    pdf.multi_cell(0, 10, f"Factores asociados: {', '.join(info.get('factores', []))}".encode('utf-8').decode('latin1'))
    pdf.cell(0, 10, f"Fuente: {info.get('fuente', '-')}".encode('utf-8').decode('latin1'), ln=True)

    pdf.cell(0, 10, "Respuestas clinicas:".encode('utf-8').decode('latin1'), ln=True)
    for clave, valor in respuestas.items():
        texto = f"{clave}: {valor}".encode('utf-8').decode('latin1')
        pdf.cell(0, 8, texto, ln=True)

    pdf.output(nombre_archivo)
    return nombre_archivo


    # Diagnóstico visual
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Diagnóstico visual sugerido: {diagnostico}", ln=True)
    pdf.multi_cell(0, 10, f"Clasificación: {info.get('clasificacion', '-')}")
    pdf.multi_cell(0, 10, f"Descripción: {info.get('descripcion', '-')}")
    pdf.multi_cell(0, 10, f"Factores asociados: {', '.join(info.get('factores', []))}")
    pdf.cell(0, 10, f"Fuente: {info.get('fuente', '-')}", ln=True)

    # Respuestas clínicas
    pdf.cell(0, 10, "Respuestas clínicas:", ln=True)
    for clave, valor in respuestas.items():
        pdf.cell(0, 8, f"{clave}: {valor}", ln=True)

    pdf.output(nombre_archivo)
    return nombre_archivo

# Streamlit UI
st.set_page_config(page_title="patologIA Clínica Integral", layout="centered")
st.title("🦷 patologIA: Diagnóstico Visual y Clínico")

with st.form("form_diagnostico"):
    imagen_cargada = st.file_uploader("📷 Sube imagen de la lesión (opcional)", type=["jpg", "jpeg", "png"])
    respuestas = mostrar_formulario()
    submit = st.form_submit_button("Generar diagnóstico integral")

if submit:
    diagnostico_visual = "Diagnóstico no disponible"
    if imagen_cargada:
        imagen_pil = image.load_img(imagen_cargada)
        st.image(imagen_pil, caption="Imagen analizada", use_container_width=True)
        entrada = procesar_imagen(imagen_pil)
        pred = model.predict(entrada)[0]
        diagnostico_visual = "Diagnóstico no disponible"
        st.success(f"🧠 Diagnóstico visual sugerido: {diagnostico_visual}")

    info = info_diagnostico.get(diagnostico_visual, {})
    if info:
        st.write(f"🔬 Clasificación: **{info.get('clasificacion')}**")
        st.write(f"📝 {info.get('descripcion')}")
        st.write(f"📌 Factores asociados: {', '.join(info.get('factores', []))}")
        st.write(f"📚 Fuente: {info.get('fuente')}")
    else:
        st.warning("No hay detalles disponibles para este diagnóstico visual.")

    archivo_pdf = generar_pdf(diagnostico_visual, info, respuestas)
    with open(archivo_pdf, "rb") as f:
        st.download_button("📄 Descargar reporte en PDF", f, file_name=archivo_pdf)
