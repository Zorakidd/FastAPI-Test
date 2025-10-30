from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# Pydantic-Modell: Validierung + Konvertierung
class Item(BaseModel):
    name: str = Field(..., min_length=1)
    preis: float = Field(..., ge=0)
    beschreibung: Optional[str] = None

# 
ARTIKEL_SPEICHER: List[Item] = []

@app.get("/")
async def startseite():
    return {"nachricht": "Willkommen"}

# Alle Artikel abrufen
@app.get("/artikel/", response_model=List[Item])
async def artikel_liste():
    return ARTIKEL_SPEICHER

# Artikel esrtellen
@app.post("/artikel/", response_model=Item, status_code=201)
async def artikel_erstellen(item: Item):
    # Pydantic prüft/konvertiert automatisch (z.B. "9.99" -> 9.99)
    ARTIKEL_SPEICHER.append(item)
    return item
