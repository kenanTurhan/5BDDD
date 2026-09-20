from fastapi import APIRouter, FastAPI, Depends, HTTPException
import auth.auth_model as model
from sqlalchemy.orm import Session
from db import engine, SessionLocal, Base
import models
import auth.auth_model as schema
import auth.serviceMdp as service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from serviceJWT import create_token, current_user
router = APIRouter(prefix= "/emprunt", tags=["emprunt"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/emprunt/{livreId}")
def emprunter(livreId:int, username: str = Depends(current_user), db: Session = Depends(get_db)):
    db.query(models.Book).filter(models.Book.id == livreId).update({"disponibles": models.Book.disponibles -1})
    db.commit()
    #ajouter le user et livre dans table emprunt
    db_user = db.query(models.User).filter(models.User.email == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="L'utilisateur n'éxiste pas")

    db_livre = db.query(models.Book).filter(models.Book.id == livreId)
    new_emprunt = models.emprunts(user_id=db_user.id, book_id=livreId)
    db.add(new_emprunt)
    db.commit()
    return(new_emprunt)


    