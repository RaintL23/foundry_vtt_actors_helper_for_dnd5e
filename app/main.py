# mi_proyecto/main.py
from fastapi import FastAPI
from app.endpoints import external_api_routes
from app.actors import npcs

app = FastAPI()

# Incluir los routers de los endpoints
app.include_router(external_api_routes.router)
app.include_router(npcs.router)

@app.get("/")
def read_root():
    """."""
    return {"Hello": "World"}
