import random, string
from datetime import timedelta, date

from fastapi.testclient import TestClient

from app.core.settings import settings

def get_superuser_token_headers(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }
    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    print(response.json())
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
    
def random_lower_string(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_age() -> int:
    return random.randint(1, 100)

def random_sexe():
    sexes = ["M", "F"]
    return random.choice(sexes)

def random_email(domain: str = "example.com") -> str:
    """
    Génère un email aléartoire
    """
    username = random_lower_string(6)
    return f"{username}@{domain}"

def random_phone(country_code: str = "+228") -> str:
    """
    Génère un numéro de téléphone aléartoire
    """
    number = ''.join(random.choices(string.digits, k=8))
    return f"{country_code}{number}"

def random_date(start_year: int = 2000, end_year: int = 2010) -> date:
    """
    Génère une date aléartoire
    """
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    return start_date + timedelta(days=random_days)