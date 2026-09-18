from fastapi import APIRouter, FastAPI, Depends, HTTPException
import auth.auth_model as model
from sqlalchemy.orm import Session
from db import engine, SessionLocal, Base
import models
import auth.auth_model as schema
import auth.serviceMdp as service
from serviceJWT import create_token, current_user
router = APIRouter(prefix= "/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Vérifie si l'email existe déjà
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà enregistré")
    
    # Crée le nouvel utilisateur
    new_user = models.User(nom=user.nom, prenom=user.prenom, email=user.email, telephone=user.telephone, mdp=service.hash_password(user.mdp))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login/")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    #vérifie si le mail existe:
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")
    
    if not service.verify_password(password, db_user.mdp):
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")

    #return db_user
    #return token
    return create_token(db_user.email)
