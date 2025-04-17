from datetime import date
from pydantic import BaseModel, EmailStr, field_validator, model_validator

class PaystubData(BaseModel):
    """
    Modelo de datos para la nómina de empleados.
    Este modelo incluye validaciones para asegurar la consistencia de los datos.
    """
    full_name: str
    email: EmailStr
    position: str
    health_discount_amount: float
    social_discount_amount: float
    taxes_discount_amount: float
    other_discount_amount: float
    gross_salary: float
    gross_payment: float
    net_payment: float
    period: date

    # Validador de campo individual: net_payment no puede ser negativo
    @field_validator("net_payment")
    def net_payment_must_be_positive(cls, v):
        """
        Valida que el pago neto no sea negativo.
        """
        if v < 0:
            raise ValueError("El pago neto no puede ser negativo")
        return v

    # Validador de modelo: para validar que el net_payment sea consistente con los descuentos
    @model_validator(mode='before')
    def check_net_payment_consistency(cls, values):
        """
        Valida que el pago neto sea consistente con los descuentos aplicados.
        """
        expected_net = (
            float(values.get("gross_payment", 0))
            - float(values.get("health_discount_amount", 0))
            - float(values.get("social_discount_amount", 0))
            - float(values.get("taxes_discount_amount", 0))
            - float(values.get("other_discount_amount", 0))
        )
        net = float(values.get("net_payment", 0))
        if net is not None and abs(expected_net - net) > 1:
            raise ValueError("El pago neto no coincide con el total de descuentos")
        return values

    def calculate_total_discounts(self) -> float:
        """
        Calcula el total de descuentos en la nomina.
        """
        return (
            self.health_discount_amount +
            self.social_discount_amount +
            self.taxes_discount_amount +
            self.other_discount_amount
        )
