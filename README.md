## Descripción del Proyecto

`atdev_assignment` Este proyecto es una aplicación basada en FastAPI para procesar nóminas. Permite cargar un archivo CSV con información de nóminas, validar los datos, generar recibos de pago en formato PDF y enviarlos por correo electrónico.

### Archivos principales

- **`app/main.py`**: Contiene el punto de entrada principal de la aplicación y la lógica para procesar las nóminas.
- **`app/models.py`**: Define el modelo de datos `PaystubData` con validaciones.
- **`app/auth.py`**: Módulo para la validación de credenciales.
- **`app/email_sender.py`**: Módulo para enviar correos electrónicos con los recibos de nómina adjuntos.
- **`app/pdf_generator.py`**: Módulo para generar recibos de nómina en formato PDF.
- **`tests/test_main.py`**: Contiene pruebas automatizadas para validar el comportamiento de la aplicación.

## Requisitos

- Python 3.11
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/yourusername/atdev_assignment.git
```
2. Navega al directorio del proyecto:
```bash
cd atdev_assignment
```
3. Instala las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
4. Configura las variables de entorno en un archivo .env
```bash
USERS=admin,hruser
PASSWORDS=admin123,hr2025
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<TU_CORREO>
SMTP_PASSWORD=<TU_CONTRASEÑA>
FROM_EMAIL=<TU_CORREO>
LOGO_DIR=app/assets/logos
```

## Uso

1. Ejecuta la aplicación con el siguiente comando:
```bash
uvicorn app.main:app --reload
```
2. Accede a la documentación interactiva de la API en:
```bash
- Swagger UI: http://127.0.0.1/docs
- Redoc: http://127.0.0.1/redoc
```

## Docker

1. Construye y ejecuta los contenedores:
```bash
docker-compose up --build
```
2. La aplicacion estará disponible en http://localhost

