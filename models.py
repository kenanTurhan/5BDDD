from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime, Identity
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Identity(), primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    mdp = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    telephone = Column(String(20))
    role = Column(String(20), default="user") 

    emprunts = relationship("emprunts", back_populates="user")

class Book(Base):
    __tablename__ = "livres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(200), nullable=False, index=True)
    auteur = Column(String(100), nullable=False, index=True)
    genre = Column(String(50), index=True)
    date_publication = Column(Date)
    
    total = Column(Integer, nullable=False, default=1)
    disponibles = Column(Integer, nullable=False, default=1)

    emprunts = relationship("emprunts", back_populates="book")

class emprunts(Base):
    __tablename__ = "emprunts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("livres.id"), nullable=False)

    user = relationship("User", back_populates="emprunts")
    book = relationship("Book", back_populates="emprunts")
