from fastapi import APIRouter, FastAPI, Depends, HTTPException
router = APIRouter(prefix= "/auth", tags=["Auth"])
import auth.auth_model as model
from sqlalchemy.orm import Session
from db import engine, SessionLocal, Base
import models
import auth.auth_model as schema


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
    new_user = models.User(nom=user.nom, prenom=user.prenom, email=user.email, telephone=user.telephone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#@router.post("/connexion", response_model=model.ConnexionOut,
# responses={400: {"description": "Connexion impossible"}},
#)
#def connexion(reponse:model.connexion):
#    response = service.connexion(
#        email=reponse.email,
#        motPasse=reponse.motPasse,
#    )
#    return response








# Crée les tables dans la base de données MySQL si elles n'existent pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Fonction utilitaire pour obtenir une session de base de données pour chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route POST : Créer un utilisateur dans MySQL
@app.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Vérifie si l'email existe déjà
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà enregistré")
    
    # Crée le nouvel utilisateur
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Route GET : Lire tous les utilisateurs de la base de données
@app.users_get if hasattr(app, "users_get") else app.get("/users/", response_model=list[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

