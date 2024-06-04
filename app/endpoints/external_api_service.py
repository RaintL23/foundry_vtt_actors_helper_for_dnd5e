# app/fetch_data.py
import httpx
import app.static.constants as app_constants
from http.client import HTTPException
from fastapi import APIRouter

from app.endpoints.external_api import ExternalApi

router = APIRouter()

@router.get("/load_data")
async def get_data(url: str):
    try:
        response = await ExternalApi.get(url)
        return response
    except httpx.RequestError as e:
        print(f"Error al hacer la solicitud: {e}")
        raise HTTPException(status_code=500, detail="Error al hacer la solicitud")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error inesperado")

@router.get("/load_constant_data")
async def get_constant_data(const: str):
    try:
        if const is not None and const.strip() != '':
            const_separate = const.split(",")
            final_response = ()
            for const_item in const_separate:
                match const_item:
                    case "manifest":
                        final_response += (await prepare_data(app_constants.URL_MANIFEST,const_item),)
                    case "spells":
                        final_response += (await prepare_data(app_constants.URL_SPELLS,const_item),)
                    case "spelllist":
                        final_response += (await prepare_data(app_constants.URL_SPELLLIST,const_item),)
                    case "monsters":
                        final_response += (await prepare_data(app_constants.URL_MONSTERS,const_item),)
                    case "documents":
                        final_response += (await prepare_data(app_constants.URL_DOCUMENTS,const_item),)
                    case "backgrounds":
                        final_response += (await prepare_data(app_constants.URL_BACKGROUNDS,const_item),)
                    case "planes":
                        final_response += (await prepare_data(app_constants.URL_PLANES,const_item),)
                    case "sections":
                        final_response += (await prepare_data(app_constants.URL_SECTIONS,const_item),)
                    case "feats":
                        final_response += (await prepare_data(app_constants.URL_FEATS,const_item),)
                    case "conditions":
                        final_response += (await prepare_data(app_constants.URL_CONDITIONS,const_item),)
                    case "races":
                        final_response += (await prepare_data(app_constants.URL_RACES,const_item),)
                    case "classes":
                        final_response += (await prepare_data(app_constants.URL_CLASSES,const_item),)
                    case "magicitems":
                        final_response += (await prepare_data(app_constants.URL_MAGICITEMS,const_item),)
                    case "weapons":
                        final_response += (await prepare_data(app_constants.URL_WEAPONS,const_item),)
                    case "armor":
                        final_response += (await prepare_data(app_constants.URL_ARMOR,const_item),)
                    case "search":
                        final_response += (await prepare_data(app_constants.URL_SEARCH,const_item),)
            return final_response
        else:
            raise HTTPException(status_code=400, detail="Falta especificar que se desea buscar.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}")

async def prepare_data(endpoint: str, name: str):
    try:
        response_json = {
            "name":name,
            "count": 0,
            "items":()
        }
        response = await search_data(endpoint)
        if response is not None:
            response_json["items"] = response
            response_json["count"] = len(response_json["items"])
        return response_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}")

async def search_data(endpoint: str):
    try:
        response = await ExternalApi.get(endpoint)
        response_items = []
        if (response is not None and "count" in response and response["count"] > 0):
            response_items += response["results"]
            if "next" in response and response["next"] is not None:
                response_items += await search_data(response["next"])
        return response_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}")