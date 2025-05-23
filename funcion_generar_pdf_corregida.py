
from fpdf import FPDF
from datetime import datetime

def 
from fpdf import FPDF
from datetime import datetime

def generar_pdf(diagnostico_visual, info, respuestas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Encabezado
    pdf.cell(200, 10, txt="REPORTE CLÍNICO - patologIA", ln=True)
    pdf.cell(200, 10, txt="Fecha: " + datetime.now().strftime("%d/%m/%Y %H:%M"), ln=True)

    # Diagnóstico visual
    pdf.ln(10)
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Diagnóstico visual sugerido:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=diagnostico_visual)

    # Información adicional
    if info:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="Detalles clínicos relevantes:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=info)

    # Respuestas del formulario
    if respuestas:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="Respuestas del caso:", ln=True)
        pdf.set_font("Arial", size=12)
        for k, v in respuestas.items():
            pdf.cell(0, 10, txt=f"- {k}: {v}", ln=True)

    # Guardar archivo
    nombre_archivo = "reporte_patologIA_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"
    pdf.output(nombre_archivo, 'F')
    return nombre_archivo
