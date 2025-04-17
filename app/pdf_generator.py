"""
Modulo para generar recibos de nomina en PDF.
"""

import os
from fpdf import FPDF
from app import config

def generate_paystub_pdf(data, country: str, company: str) -> bytes:
    """
    Genera un recibo de nomina en PDF basado en la informacion proporcionada.

    Args:
        data: Objeto que contiene los detalles de la nomina.
        country (str): Codigo del pais ('do', 'USA').
        company (str): Nombre de la compañia.

    Returns:
        bytes: El archivo pdf generado.
    """
    labels = {
        "do": {
            "Name": "Nombre",
            "Position": "Cargo",
            "Period": "Perido",
            "Gross Salary": "Salario Bruto",
            "Gross Payment": "Pago Bruto",
            "Net Payment": "Pago Neto",
            "Health": "SFS",
            "Social": "AFP",
            "Taxes": "ISR",
            "Others": "Otros",
            "Total Discounts": "Total Descuentos",
            "Title": "Comprobante de Pago"
        },
        "USA": {
            "Name": "Name",
            "Position": "Position",
            "Period": "Period",
            "Gross Salary": "Gross Salary",
            "Gross Payment": "Gross Payment",
            "Net Payment": "Net Payment",
            "Health": "Health Insurance",
            "Social": "Social Security",
            "Taxes": "Taxes",
            "Others": "Others",
            "Total Discounts": "Total Discounts",
            "Title": "Paystub Payment"
        }
    }
    l = labels[country]
    pdf = FPDF()
    pdf.add_page()
    logo_path = os.path.join(config.LOGO_DIR, f"{company.lower()}.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(config.LOGO_DIR, "fastapi.png")
    pdf.image(logo_path, x=10, y=8, w=33)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=l["Title"], ln=True, align='C')
    pdf.ln(20)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"{l['Name']}: {data.full_name}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Position']}: {data.position}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Period']}: {data.period}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Gross Salary']}: {data.gross_salary}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Gross Payment']}: {data.gross_payment}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Net Payment']}: {data.net_payment}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Health']}: {data.health_discount_amount}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Social']}: {data.social_discount_amount}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Taxes']}: {data.taxes_discount_amount}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Others']}: {data.other_discount_amount}", ln=True)
    pdf.cell(200, 10, txt=f"{l['Total Discounts']}: {data.calculate_total_discounts()}", ln=True)
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output
