"""
Configuration pytest partagée par tous les fichiers de test (tests/test_*.py).

Ce fichier est chargé AUTOMATIQUEMENT par pytest (pas besoin de l'importer).
Il définit les "fixtures" utilisées comme paramètres dans les tests,
par ex. `def test_xxx(client, auth_headers):`.
"""
import pytest
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from db import Base
import models

# Chaque routeur définit sa PROPRE fonction get_db() (auth_router.get_db,
# admin_router.get_db, emprunt_router.get_db) : ce sont 3 objets différents
# même si le code est identique, donc il faut les importer et les surcharger
# tous les 3 séparément.
import auth.auth_router as auth_router
import admin.admin_router as admin_router
import emprunt.emprunt_router as emprunt_router

import auth.serviceMdp as service
from serviceJWT import create_token


# --------------------------------------------------------------------------
# 1. Base de données de TEST
# --------------------------------------------------------------------------
# On ne veut surtout pas que les tests écrivent dans la vraie base Oracle
# (définie dans db.py / .env). On utilise donc une base SQLite en mémoire,
# créée à la volée, qui disparaît à la fin des tests.
#
# `StaticPool` + `check_same_thread=False` sont nécessaires pour qu'une base
# SQLite "in-memory" soit partagée entre toutes les connexions ouvertes par
# le TestClient (par défaut chaque connexion SQLite en mémoire est isolée).
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Remplace le get_db() de chaque routeur : fournit une session
    connectée à la base de test au lieu de la vraie base Oracle."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# `dependency_overrides` est un mécanisme FastAPI : quand une route demande
# `Depends(get_db)`, FastAPI regarde d'abord si une fonction de remplacement
# a été enregistrée ici, et l'utilise à la place.
app.dependency_overrides[auth_router.get_db] = override_get_db
app.dependency_overrides[admin_router.get_db] = override_get_db
app.dependency_overrides[emprunt_router.get_db] = override_get_db


# --------------------------------------------------------------------------
# 2. Création des tables + jeu de données initial
# --------------------------------------------------------------------------
# scope="session" => cette fixture ne s'exécute qu'UNE SEULE fois pour tout
# le lancement de pytest (pas avant chaque test). C'est indispensable ici
# car vos tests sont "chaînés" : test_emprunts.py suppose que le livre 1
# existe déjà, test_promouvoir_admin_succes suppose que l'utilisateur 2
# existe déjà, etc. Ce ne sont pas des tests isolés les uns des autres.
#
# autouse=True => s'exécute automatiquement, sans avoir à l'écrire en
# paramètre de chaque test.
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    # Un compte admin, créé directement en base (id=1) : il sert pour la
    # fixture admin_headers ci-dessous, et il faut qu'il existe AVANT
    # jean.dupont (créé via l'API dans test_auth.py) pour que
    # jean.dupont obtienne bien l'id=2, comme l'attend
    # test_promouvoir_admin_succes (PATCH /admin/promotion/2).
    admin = models.User(
        nom="Biblio",
        prenom="Admin",
        email="admin@test.com",
        telephone="0000000000",
        mdp=service.hash_password("adminpass"),
        role="admin",
    )
    db.add(admin)

    # 3 livres de départ, avec des stocks pensés pour les scénarios déjà
    # écrits dans tests/test_emprunts.py :
    #   - livre 1 et 2 : disponibles (pour les emprunts qui doivent réussir)
    #   - livre 3      : stock à 0 (pour tester l'erreur "Plus de stock")
    livre1 = models.Book(
        titre="1984", auteur="George Orwell", genre="Dystopie",
        date_publication=date(1949, 6, 8), total=3, disponibles=3,
    )
    livre2 = models.Book(
        titre="Le Petit Prince", auteur="Antoine de Saint-Exupéry", genre="Conte",
        date_publication=date(1943, 4, 6), total=2, disponibles=2,
    )
    livre3 = models.Book(
        titre="Fondation", auteur="Isaac Asimov", genre="Science-Fiction",
        date_publication=date(1951, 5, 1), total=1, disponibles=0,
    )
    db.add_all([livre1, livre2, livre3])

    db.commit()
    db.close()

    yield  # <- tous les tests s'exécutent ici

    Base.metadata.drop_all(bind=engine)


# --------------------------------------------------------------------------
# 3. Fixtures utilisées comme paramètres dans les tests
# --------------------------------------------------------------------------
@pytest.fixture(scope="session")
def client():
    """Client HTTP de test pour appeler l'API FastAPI sans lancer de vrai
    serveur (pas de uvicorn, pas de port réseau)."""
    return TestClient(app)


@pytest.fixture(scope="session")
def auth_headers():
    """Headers d'authentification pour un utilisateur normal.

    On génère directement un token JWT via create_token(), sans passer par
    /auth/login/, pour ne pas dépendre du bon fonctionnement de la route de
    login dans les autres tests. L'utilisateur jean.dupont@test.com est créé
    par tests/test_auth.py, qui s'exécute avant les tests qui utilisent
    cette fixture.
    """
    token = create_token("jean.dupont@test.com")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def admin_headers():
    """Headers d'authentification pour le compte admin seedé ci-dessus."""
    token = create_token("admin@test.com")
    return {"Authorization": f"Bearer {token}"}
