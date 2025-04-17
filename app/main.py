"""
Modulo principal para procesar la nomina.
"""

import csv
import io
from datetime import datetime, timezone

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models import PaystubData
from app.auth import validate_credentials
from app.pdf_generator import generate_paystub_pdf
from app.email_sender import send_email_with_attachment

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/assets"), name="static")
security = HTTPBasic()

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>API de Nómina</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light text-center p-5">

        <div class="container">
            <img src="/static/logos/fastapi.png" alt="Logo FastAPI" class="img-fluid mb-4" style="max-height: 120px;">
            <h1 class="display-5">Bienvenido a la API de Nómina</h1>
            <p class="lead">Accede a la <a href="/docs" class="btn btn-primary mt-3">Documentación Interactiva</a></p>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """


@app.post("/process")
async def process_payroll(
    credentials: HTTPBasicCredentials = Depends(security),
    file: UploadFile = File(...),
    country: str = Query("do", enum=["do", "USA"]),
    company: str = Query(...)
):
    """
    Procesa los datos de nomina obtenidos desde el archivo CSV.

    Args:
        credentials (HTTPBasicCredentials): Credenciales basicas de autenticacion.
        file (UploadFile): Archivo CSV con datos de nomina.
        country (str): Codigo de pais, puede ser "do" o "USA".
        company (str): Nombre de la compañia.

    Returns:
        dict: Un diccionario con el estado y los resultados del procesamiento.
    """
    # Validar credenciales
    if not validate_credentials(credentials.username, credentials.password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Leer contenido del archivo
    contents = await file.read()
    decoded_content = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded_content))

    results = []

    for row in reader:
        try:
            data = PaystubData(**row)
            pdf_bytes = generate_paystub_pdf(data, country, company)
            send_email_with_attachment(
                country=country,
                to=data.email,
                attachment=pdf_bytes,
                filename=f"paystub_{data.email}.pdf"
            )
            results.append({
                "email": data.email,
                "sent_at": datetime.now(timezone.utc).isoformat()
            })
        except Exception as e:
            results.append({
                "email": row.get("email", "unknown"),
                "error": str(e)
            })

    return {"status": "success", "results": results}
