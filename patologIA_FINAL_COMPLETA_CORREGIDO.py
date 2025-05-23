
import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from fpdf import FPDF
from datetime import datetime
import os

# Cargar modelo previamente entrenado
MODEL_PATH = "modelo_patologIA.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Leer clases desde carpetas
class_names = sorted(os.listdir("dataset_patologIA_demo"))

# Procesamiento de imagen
def procesar_imagen(imagen):
    imagen = imagen.resize((128, 128))
    img_array = np.array(imagen) / 255.0
    return np.expand_dims(img_array, axis=0)

# Función PDF
def generar_pdf(diagnostico_visual, info, respuestas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="REPORTE CLÍNICO - patologIA", ln=True)
    pdf.cell(200, 10, txt="Fecha: " + datetime.now().strftime("%d/%m/%Y %H:%M"), ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Diagnóstico visual sugerido:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=diagnostico_visual)

    if info:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="Detalles clínicos relevantes:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=info)

    if respuestas:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="Respuestas del caso:", ln=True)
        pdf.set_font("Arial", size=12)
        for k, v in respuestas.items():
            pdf.cell(0, 10, txt=f"- {k}: {v}", ln=True)

    nombre_archivo = "reporte_patologIA_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"
    pdf.output(nombre_archivo, 'F')
    return nombre_archivo

# Interfaz Streamlit
st.title("Diagnóstico visual con patologIA")

imagen = st.file_uploader("Sube una imagen clínica", type=["jpg", "jpeg", "png"])
info = st.text_area("Anota datos clínicos adicionales (opcional)")

# PREGUNTAS OPCIONALES
preguntas = [
    {"pregunta": "¿Dónde se encuentra la lesión?", "opciones": ["Labio", "Lengua", "Encía", "Paladar", "Piso de boca", "Mejilla", "Otra"]},
    {"pregunta": "¿Qué tamaño tiene la lesión?", "opciones": ["< 5 mm", "5–10 mm", "> 10 mm"]},
    {"pregunta": "¿Qué color predomina?", "opciones": ["Blanco", "Rojo", "Mixto", "Pigmentado", "Translúcido"]},
    {"pregunta": "¿Presenta dolor?", "opciones": ["Sí", "No"]},
    {"pregunta": "¿Cuánto tiempo lleva presente?", "opciones": ["< 1 semana", "1–4 semanas", "> 1 mes"]},
    {"pregunta": "¿Ha aumentado de tamaño?", "opciones": ["Sí", "No", "No lo sabe"]},
    {"pregunta": "¿El paciente fuma o consume alcohol regularmente?", "opciones": ["Sí", "No"]},
    {"pregunta": "¿La lesión sangra o supura?", "opciones": ["Sí", "No"]},
]

respuestas = {}
with st.expander("Responde el mini-formulario clínico (opcional)", expanded=False):
    for p in preguntas:
        respuesta = st.selectbox(p["pregunta"], p["opciones"], key=p["pregunta"])
        respuestas[p["pregunta"]] = respuesta


if imagen:
    img = Image.open(imagen)
    st.image(img, caption="Imagen cargada", use_column_width=True)

    if st.button("Analizar"):
        procesada = procesar_imagen(img)
        pred = model.predict(procesada)
        pred_idx = np.argmax(pred)
        diagnostico_visual = class_names[pred_idx]

        st.subheader("Diagnóstico visual sugerido:")
        st.write(diagnostico_visual)

        archivo_pdf = generar_pdf(diagnostico_visual, info, respuestas)
        st.success("Reporte generado")
        with open(archivo_pdf, "rb") as f:
            st.download_button("Descargar reporte PDF", f, file_name=archivo_pdf)
