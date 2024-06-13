"""."""
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import app.actors.actor_service as ActorService

router = APIRouter()

class NPCRequest(BaseModel):
    """."""
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
    """."""
    message: str
    user_id: int

@router.post("/npcs")
async def create_npc(input_data: NPCRequest):
    """."""
    try:
        if input_data.template is None:
            raise HTTPException(status_code=400, detail="There must be a template selected.")
        return await ActorService.create(input_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}") from e
    