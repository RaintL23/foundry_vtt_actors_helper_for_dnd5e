import json
import os
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import app.actors.actor_service as ActorService

router = APIRouter()

class NPCRequest(BaseModel):
    template: Optional[str] = None
    urls: Optional[str] = None
    actor_type: Optional[str] = "npc"
    name: Optional[str] = "generic_npc"
    race: Optional[str] = None
    attribute_array: Optional[str] = "terrible"
    hit_dice: Optional[int] = 10
    size: Optional[str] = "medium"
    neceorat: Optional[bool] = False

class NPCResponse(BaseModel):
    message: str
    user_id: int

@router.post("/npcs")
async def create_npc(input: NPCRequest):
    try:
        if input.template is None:
            raise HTTPException(status_code=400, detail="Tiene que haber un template seleccionado.")
        
        ### Lo ideal es que el usuario suba la dirección del archivo pero por ahora lo vamos a poner hardcoded
        ### para simplicar el desarrollo de la funcionalidad, esto se puede resolver cuando haya un frontend
        json_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../files/test2.json"))
        if not os.path.exists(json_file_path):
            raise HTTPException(status_code=500, detail="No se pudo encontrar el archivo json base para crear al Actor")
        json_data = {}
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)

        return await ActorService.create(json_data, input.model_dump())
        # user_id = 12345
        # response = NPCResponse(
        #     message=f"Usuario {input.name} creado con éxito.",
        #     user_id=user_id
        # )
        # return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}")
    