from dataclasses import dataclass
from fastapi import FastAPI

@dataclass
class Item:
    name: str
    preis: float
    beschreibung: str | None = None

app = FastAPI()

@app.post("/items/")
async def erstelle_item(item: Item):
    return item
