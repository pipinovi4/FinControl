from .phone import validate_phone
from .email import validate_email
from .date import validate_date
from .inn import validate_inn_ru
from .snils import validate_snils
from .amount import validate_amount
from .document import validate_document
from .id_number import validate_id_number
from .full_name import validate_full_name
from .address import validate_address
from .income import validate_income
from .access_code import validate_access_code
from .enum import validate_enum
from .yes_no import validate_yes_no
from .date_range import validate_date_range

VALIDATOR_REGISTRY = {
    "phone": validate_phone,
    "email": validate_email,
    "date": validate_date,
    "inn_ru": validate_inn_ru,
    "snils": validate_snils,
    "amount": validate_amount,
    "document": validate_document,
    "id_number": validate_id_number,
    "full_name": validate_full_name,
    "address": validate_address,
    "income": validate_income,
    "access_code": validate_access_code,
    "enum": validate_enum,
    "yes_no": validate_yes_no,
    "date_range": validate_date_range,
}

__all__ = ["VALIDATOR_REGISTRY"]
