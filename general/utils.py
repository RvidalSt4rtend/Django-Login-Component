# utils.py
from datetime import datetime
import pytz
from rest_framework import status
from rest_framework.exceptions import APIException

#Hora Local
def get_local_time():
    local_tz = pytz.timezone('America/Lima')  # Cambia esto a tu zona horaria
    return datetime.now(local_tz)

# Error personalizado
class SimpleValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A validation error occurred."
    default_code = "error"

    def __init__(self, detail, code=None):
        self.detail = {"error": detail}