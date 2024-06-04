# app/external_api.py
import httpx
import app.static.constants as app_constants


class ExternalApi:

    @staticmethod
    async def get(url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
