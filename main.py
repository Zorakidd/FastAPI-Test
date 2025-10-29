from dataclasses import dataclass
from fastapi import FastAPI

@dataclass
class Item:
    name: str
    preis: float
    beschreibung: str | None = None

app = FastAPI()

# Endpunkt 1: GET Hallo-Welt
@app.get("/")
async def startseite():
    return {"nachricht": "Willkommen zur FastAPI-Anwendung!"}

# Endpunkt 2: POST Artikel erstellen
@app.post("/artikel/")
async def artikel_erstellen(item: Item):
    return {
        "status": "Artikel erstellt",
        "artikel": item
    }
