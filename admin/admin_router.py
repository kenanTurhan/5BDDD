from fastapi import APIRouter, FastAPI, Depends, HTTPException
import auth.auth_model as model
from sqlalchemy.orm import Session
from db import engine, SessionLocal, Base
import models
import admin.admin_models as schema
import auth.serviceMdp as service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from serviceJWT import create_token, current_user
router = APIRouter(prefix= "/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/isAdmin")
def private_route(username: str = Depends(current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == username, models.User.role == "admin").first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Cette action est réservé au bibliothequaires")

    return {"message": f"Bonjours, {username}. Vous êtes bibliothécaire."}

@router.post("/ajouterLivre")
def ajouter_livre( livre: schema.ajouterLivre, username : str = Depends(current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == username, models.User.role == "admin").first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Cette action est réservé au bibliothequaires")

    new_livre = models.Book(
        titre=livre.titre,
        auteur=livre.auteur,
        genre=livre.genre,
        date_publication=livre.date_publication,
        total=livre.total,
        disponibles=livre.disponibles
    )
    db.add(new_livre)
    db.commit()
    db.refresh(new_livre)
    return new_livre

@router.put("/modifierLivre/{livre_id}")
def modifier_livre(livre_id: int, livre: schema.modifierLivre, username: str = Depends(current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == username, models.User.role == "admin").first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Cette action est réservé au bibliothequaires")
    db_livre = db.query(models.Book).filter(models.Book.id == livre_id).first()
    if not db_livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    db_livre.titre = livre.titre if livre.titre is not None else db_livre.titre
    db_livre.auteur = livre.auteur if livre.auteur is not None else db_livre.auteur
    db_livre.genre = livre.genre if livre.genre is not None else db_livre.genre
    db_livre.date_publication = livre.date_publication if livre.date_publication is not None else db_livre.date_publication
    db_livre.total = livre.total if livre.total is not None else db_livre.total
    db_livre.disponibles = livre.disponibles if livre.disponibles is not None else db_livre.disponibles
    db.commit()
    db.refresh(db_livre)
    return db_livre


@router.patch("/promotion/{userID}")
def promouvoirAdmin(user_id: int, username: str = Depends(current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == username, models.User.role == "admin").first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Cette action est réservé au bibliothequaires")
    
    db_nvAdmin = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_nvAdmin:
        raise HTTPException(status_code=404, detail="L'utilisateur n'éxiste pas")
    
    db.query(models.User).filter(models.User.id == user_id).update({"role": "admin"})
    db.commit()
    db.refresh(db_nvAdmin)
    return (db_nvAdmin)

