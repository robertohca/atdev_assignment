import pytest
from httpx import AsyncClient
from app.main import app

# Test: Caso exitoso con una fila válida
@pytest.mark.asyncio
async def test_process_payroll_success(monkeypatch):
    csv_content = """full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period
Roberto Camejo,fastapiassignment@gmail.com,Software Engineer,50,30,100,20,5000,4800,4600,2025-04-30
"""

    monkeypatch.setattr("app.main.validate_credentials", lambda u, p: True)
    monkeypatch.setattr("app.main.generate_paystub_pdf", lambda data, country, company: b"PDF_BYTES")
    monkeypatch.setattr("app.main.send_email_with_attachment", lambda **kwargs: None)

    # Usa solo base_url sin app en AsyncClient
    async with AsyncClient(base_url="http://web") as ac:
        response = await ac.post(
            "/process?credentials=admin%2Badmin123&country=do&company=MiEmpresa",
            files={"file": ("payroll.csv", csv_content, "text/csv")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["results"][0]["email"] == "fastapiassignment@gmail.com"


# Test: Credenciales inválidas
@pytest.mark.asyncio
async def test_process_payroll_invalid_credentials(monkeypatch):
    monkeypatch.setattr("app.main.validate_credentials", lambda u, p: False)

    csv_content = """full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period
Roberto Camejo,fastapiassignment@gmail.com,Software Engineer,50,30,100,20,5000,4800,4600,2025-04-30
"""

    async with AsyncClient(base_url="http://web") as ac:
        response = await ac.post(
            "/process?credentials=wrong%2Bwrong&country=do&company=MiEmpresa",
            files={"file": ("payroll.csv", csv_content, "text/csv")}
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


# Test: CSV con campos faltantes (net_payment faltante)
@pytest.mark.asyncio
async def test_process_payroll_invalid_csv(monkeypatch):
    monkeypatch.setattr("app.main.validate_credentials", lambda u, p: True)
    monkeypatch.setattr("app.main.generate_paystub_pdf", lambda data, country, company: b"PDF_BYTES")
    monkeypatch.setattr("app.main.send_email_with_attachment", lambda **kwargs: None)

    # Falta columna net_payment
    csv_content = """full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,period
Carlos Gómez,fastapiassignment@gmail.com,QA Engineer,30,20,80,15,3500,3400,2025-04-30
"""

    async with AsyncClient(base_url="http://web") as ac:
        response = await ac.post(
            "/process?credentials=admin%2Badmin123&country=do&company=MiEmpresa",
            files={"file": ("bad.csv", csv_content, "text/csv")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "error" in data["results"][0]
    assert data["results"][0]["email"] == "fastapiassignment@gmail.com"


# Test: CSV con una fila buena y dos con errores
@pytest.mark.asyncio
async def test_process_payroll_partial_success(monkeypatch):
    csv_content = """full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period
Roberto Camejo,fastapiassignment@gmail.com,Software Engineer,50,30,100,20,5000,4800,4600,2025-04-30
Ana Pérez,fastapiassignment[fa]gmail.com,Designer,40,25,90,10,4000,3900,3800,2025-04-30
Carlos Gómez,fastapiassignment@gmail.com,QA Engineer,30,20,80,15,3500,3400,,2025-04-30
"""

    monkeypatch.setattr("app.main.validate_credentials", lambda u, p: True)
    monkeypatch.setattr("app.main.generate_paystub_pdf", lambda data, country, company: b"PDF_BYTES")
    monkeypatch.setattr("app.main.send_email_with_attachment", lambda **kwargs: None)

    async with AsyncClient(base_url="http://web") as ac:
        response = await ac.post(
            "/process?credentials=admin%2Badmin123&country=do&company=MiEmpresa",
            files={"file": ("mixed.csv", csv_content, "text/csv")}
        )

    assert response.status_code == 200
    data = response.json()
    results = data["results"]

    assert data["status"] == "success"
    assert len(results) == 3

    # Primer resultado debe ser correcto
    assert "email" in results[0]
    assert "error" not in results[0]

    # Segundo: email inválido
    assert "error" in results[1]
    assert results[1]["email"] == "fastapiassignment[fa]gmail.com"

    # Tercero: campo faltante
    assert "error" in results[2]
    assert results[2]["email"] == "fastapiassignment@gmail.com"
