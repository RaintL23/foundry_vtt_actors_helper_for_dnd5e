"""."""
from http.client import HTTPException
import httpx
import app.static.constants as app_constants
from app.endpoints.external_api import ExternalApi

async def get_data_by_constants(const: str):
    """."""
    try:
        if const is not None and const.strip() != '':
            const_separate = const.split(",")
            final_response = ()
            for const_item in const_separate:
                match const_item:
                    case "manifest":
                        final_response += (
                            await prepare_data(app_constants.URL_MANIFEST,const_item,0),)
                    case "spells":
                        final_response += (
                            await prepare_data(app_constants.URL_SPELLS,const_item,0),)
                    case "spelllist":
                        final_response += (
                            await prepare_data(app_constants.URL_SPELLLIST,const_item,0),)
                    case "monsters":
                        final_response += (
                            await prepare_data(app_constants.URL_MONSTERS,const_item,0),)
                    case "documents":
                        final_response += (
                            await prepare_data(app_constants.URL_DOCUMENTS,const_item,0),)
                    case "backgrounds":
                        final_response += (
                            await prepare_data(app_constants.URL_BACKGROUNDS,const_item,0),)
                    case "planes":
                        final_response += (
                            await prepare_data(app_constants.URL_PLANES,const_item,0),)
                    case "sections":
                        final_response += (
                            await prepare_data(app_constants.URL_SECTIONS,const_item,0),)
                    case "feats":
                        final_response += (
                            await prepare_data(app_constants.URL_FEATS,const_item,0),)
                    case "conditions":
                        final_response += (
                            await prepare_data(app_constants.URL_CONDITIONS,const_item,0),)
                    case "races":
                        final_response += (
                            await prepare_data(app_constants.URL_RACES,const_item,0),)
                    case "classes":
                        final_response += (
                            await prepare_data(app_constants.URL_CLASSES,const_item,0),)
                    case "magicitems":
                        final_response += (
                            await prepare_data(app_constants.URL_MAGICITEMS,const_item,0),)
                    case "weapons":
                        final_response += (
                            await prepare_data(app_constants.URL_WEAPONS,const_item,0),)
                    case "armor":
                        final_response += (
                            await prepare_data(app_constants.URL_ARMOR,const_item,0),)
                    case "search":
                        final_response += (
                            await prepare_data(app_constants.URL_SEARCH,const_item,0),)
                    case "items":
                        final_response += (
                            await prepare_data(app_constants.URL_ITEMS,const_item,1),)
            return final_response
        else:
            raise HTTPException(status_code=400, detail="Falta especificar que se desea buscar.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}") from e

async def prepare_data(endpoint: str, name: str, url_type: int):
    """."""
    try:
        response_json = {
            "name":name,
            "count": 0,
            "items":()
        }
        response = None
        match url_type:
            case 0:
                response = await search_data(endpoint)
            case 1:
                response = await search_items_data()
        if response is not None:
            response_json["items"] = response
            response_json["count"] = len(response_json["items"])
        return response_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}") from e

async def search_data(endpoint: str):
    """."""
    try:
        response = await ExternalApi.get(endpoint)
        response_items = []
        if (response is not None and "count" in response and response["count"] > 0):
            response_items += response["results"]
            if "next" in response and response["next"] is not None:
                response_items += await search_data(response["next"])
        return response_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}") from e

async def search_items_data():
    """."""
    try:
        response = ()
        response += (await ExternalApi.get(app_constants.URL_ITEMS),)
        response += (await ExternalApi.get(app_constants.URL_ITEMS_BASE),)
        response += (await ExternalApi.get(app_constants.URL_ITEMS_MAGIC_VARIANTS),)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}") from e
