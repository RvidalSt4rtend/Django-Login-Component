# utils.py
from datetime import datetime
import pytz

def get_local_time():
    local_tz = pytz.timezone('America/Lima')  # Cambia esto a tu zona horaria
    return datetime.now(local_tz)
