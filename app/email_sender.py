"""
Modulo para la funcionalidad de enviar emails con la nomina en adjuntos.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app import config


def send_email_with_attachment(country: str, to: str, attachment: bytes, filename: str):
    """
    Envia un email con un adjunto.

    Args:
        country (str): Codigo de pais ('do', 'USA').
        to (str): Correo electronico del destinatario.
        attachment (bytes): Archivo adjunto.
        filename (str): Nombre del archivo adjunto.
    """
    translation = {
        "do": {
            "subject": "Comprobante de Pago",
            "body": "Adjunto encontrará su comprobante de pago."
        },
        "USA": {
            "subject": "Paystub Payment",
            "body": "Attached is your paystub."
        }
    }
    l = translation[country]
    msg = MIMEMultipart()
    msg['From'] = config.FROM_EMAIL
    msg['To'] = to
    msg['Subject'] = f"{l['subject']}"
    body = f"{l['body']}"
    msg.attach(MIMEText(body, 'plain'))
    part = MIMEApplication(attachment, Name=filename)
    part['Content-Disposition'] = f'attachment; filename="{filename}"'
    msg.attach(part)
    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(msg)
