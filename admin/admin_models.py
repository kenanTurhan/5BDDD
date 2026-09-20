from pydantic import BaseModel
from datetime import date

from typing import Optional

class ajouterLivre(BaseModel):
    titre: str
    auteur: str
    genre: str
    date_publication: date
    total: int
    disponibles: int

class modifierLivre(BaseModel):
    titre: Optional[str] = None
    auteur: Optional[str] = None
    genre: Optional[str] = None
    date_publication: Optional[date] = None
    total: Optional[int] = None
    disponibles: Optional[int] = None

