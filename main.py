from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": False})


# Pydantic-Modell: Validierung
class Item(BaseModel):
    listen_Eintrag_id: str = Field(...)
    @field_validator ('listen_Eintrag_id')
    def listen_id_validator(cls, value):
        if not value.isdigit():
            raise ValueError('Die ID darf nur aus Ziffern bestehn')
        return value
    name: str = Field(..., min_length=2)
    preis: float = Field(..., ge=0)
    beschreibung: Optional[str] = None


ARTIKEL_SPEICHER: List[Item] = []


@app.get("/")
async def startseite():
    return "Willkommen"


def test(name: int):
    return str(name)

# Alle Artikel abrufen
@app.get("/artikel/", response_model=List[Item])
async def artikel_liste():
    if not ARTIKEL_SPEICHER:
        return "Liste ist Leer, es müssen Artikel erst Hinzugefügt werden"
    else:
        return ARTIKEL_SPEICHER


# Artikel esrtellen
@app.post("/artikel/", response_model=Item, status_code=201)
async def artikel_erstellen(item: Item):
    # Pydantic prüft/konvertiert automatisch (z.B. "9.99" -> 9.99)
    ARTIKEL_SPEICHER.append(item)
    return item

    
# Artikel löschen
@app.delete("/artikel/", status_code=200)
async def artikel_loeschen(artikel_id: str):
    # Durchsuche/Iteriere die Liste nach einem Artikell mit der ID
    for index, artikel in enumerate(ARTIKEL_SPEICHER):
        if artikel.listen_Eintrag_id == artikel_id:
            geloeschter_Artikel = artikel.name
            # Entfernt den Artikel aus der Liste
            ARTIKEL_SPEICHER.pop(index)
            return {"message": f"Artikel {geloeschter_Artikel} mit der ID {artikel_id} wurde gelöscht"}
    # Wenn die ID nicht gefunden wurde, werfe einen 404-Fehler
    raise HTTPException(status_code=404, detail=f"Artikel mit ID {artikel_id} nicht gefunden")


# @app.delete("/artikel-loeschen/{artikel_id}", status_code=200)
# async def artikel_loeschen(artikel_id: str):
#     for index, artikel in enumerate(ARTIKEL_SPEICHER):
#         if artikel.listen_Eintrag_id == artikel_id:
#             geloeschter_Artikel = artikel.name
#             ARTIKEL_SPEICHER.pop(index)
#             return {"message": f"Artikel {geloeschter_Artikel} mit der ID {artikel_id} wurde gelöscht"}
#     raise HTTPException(status_code=404, detail=f"Artikel mit ID {artikel_id} nicht gefunden")


# # Artikel Liste als feste JSON Speichern
# @app.post("/artikel/", status_code=201)
# async def artikel_liste_speichern():
#     try:
#         with open("datei.json", "w") as datei:
#             json.dump(ARTIKEL_SPEICHER, datei)
#         return {"message": f"{len(daten)} Artikel gespeichert", "pfad": str(DATEI_PFAD)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Speichern fehlgeschlagen: {e}")