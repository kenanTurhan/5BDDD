from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: Optional[str] = None
    mdp: str


class User(UserCreate):
    id: int
    role: str

    class Config:
        from_attributes = True
