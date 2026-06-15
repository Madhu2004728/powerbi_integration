import requests
from ...core.config import settings

AUTH_URL = (
    f"https://login.microsoftonline.com/"
    f"{settings.POWERBI_TENANT_ID}/oauth2/v2.0/token"
)

def get_access_token():

    payload = {
        "grant_type": "client_credentials",
        "client_id": settings.POWERBI_CLIENT_ID,
        "client_secret": settings.POWERBI_CLIENT_SECRET,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }

    response = requests.post(
        AUTH_URL,
        data=payload
    )

    response.raise_for_status()

    return response.json()["access_token"]