from fastapi import APIRouter, FastAPI, Depends, HTTPException
import auth.auth_model as model
from sqlalchemy.orm import Session
from db import engine, SessionLocal, Base
import models
import auth.auth_model as schema
import auth.serviceMdp as service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import or_

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
    #ajouter le user et livre dans table emprunt
    db_user = db.query(models.User).filter(models.User.email == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="L'utilisateur n'éxiste pas")

    db_livre = db.query(models.Book).filter(models.Book.id == livreId).first()
    if not db_livre: 
        raise HTTPException(status_code=404, detail="livre pas trouvé")

    #verifier disponibilité
    if db_livre.disponibles < 1:
        raise HTTPException(status_code=403, detail="Plus de stock")

    

    new_emprunt = models.emprunts(user_id=db_user.id, book_id=livreId, rendu=False)
    db.add(new_emprunt)
    db.commit()
    #retirer un livre du nb disponible de la table book
    db.query(models.Book).filter(models.Book.id == livreId).update({"disponibles": models.Book.disponibles -1})
    db.commit()

    return(new_emprunt)

@router.patch("/rendreLivre/{empruntId}")
def rendreLivre(empruntId:int, username: str = Depends(current_user), db: Session = Depends(get_db)):
    db_emprunt = db.query(models.emprunts).filter(models.emprunts.id == empruntId, models.emprunts.rendu == False).first()
    if not db_emprunt:
        raise HTTPException(status_code=404, detail="Emprunt déjà rendu")

    livreId = db_emprunt.book_id
    # db.delete(db_emprunt)
    db.query(models.emprunts).filter(models.emprunts.id == empruntId).update({"rendu": True})

    #ajouter un livre du nb disponible de la table book
    db.query(models.Book).filter(models.Book.id == livreId).update({"disponibles": models.Book.disponibles +1})
    db.commit()
    return {"message": "Livre rendu"}




@router.get("/rechercher/{titre}")
def rechercherLibre(titre: str, db: Session = Depends(get_db)):
    db_livre = db.query(models.Book).filter(
        or_(
            models.Book.titre.ilike(titre),
            models.Book.auteur.ilike(titre),
            models.Book.genre.ilike(titre),
        )
    ).all()
    if not db_livre :
        raise HTTPException(status_code=404, detail="Aucun livre correspond à la recherche")
    return db_livre
    

@router.get("/detail/{idlivre}")
def getDetailLivre(idlivre:int, db: Session = Depends(get_db)):
    db_livre = db.query(models.Book).filter(models.Book.id == idlivre).first()
    if db_livre is None:
        raise HTTPException(status_code=404, detail="Aucun livre correspond à la recherche")
    else:
        return db_livre

@router.get("/mesEmprunt/")
def getMesEmprunt(username: str = Depends(current_user), db: Session = Depends(get_db) ):
    idUser = db.query(models.User).filter(models.User.email == username).first()
    empruntUser = db.query(models.emprunts).filter(models.emprunts.user_id == idUser.id).all()
    return (empruntUser)