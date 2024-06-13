"""."""
from http.client import HTTPException
from fastapi import APIRouter
import httpx
import app.endpoints.external_api_service as ExternalAPIService
from app.endpoints.external_api import ExternalApi

router = APIRouter()

@router.get("/load_data")
async def get_data(url: str):
    """."""
    try:
        response = await ExternalApi.get(url)
        return response
    except httpx.RequestError as e:
        print(f"Error al hacer la solicitud: {e}")
        raise HTTPException(status_code=500, detail="Error al hacer la solicitud") from e
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error inesperado") from e

@router.get("/load_constant_data")
async def get_constant_data(const: str):
    """."""
    try:
        return await ExternalAPIService.get_data_by_constants(const)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}") from e
