# Bibliothèque en ligne – API FastAPI / Oracle

Projet 5BDDD (SUPINFO). API de gestion d'une bibliothèque en ligne : les utilisateurs
s'inscrivent, empruntent et rendent des livres ; les bibliothécaires (rôle `admin`)
gèrent le catalogue.

**Stack :** Python, FastAPI, SQLAlchemy, Alembic, Pydantic, Oracle (`oracledb`), JWT.

## Fonctionnalités

- **Utilisateurs** : inscription (nom, prénom, email, téléphone), connexion (JWT), consultation de ses emprunts.
- **Livres** : ajout, modification, suppression (admin), recherche par titre / auteur / genre, détail d'un livre.
- **Emprunts** : emprunter un livre (uniquement s'il est disponible), le rendre, historique par utilisateur.
- **Migrations** : schéma géré avec Alembic.
- **Documentation** : Swagger généré automatiquement par FastAPI.

## Prérequis

- Python 3.10 ou plus
- Une base Oracle accessible (ex. Oracle Free, service `FREEPDB1`)
- Un utilisateur Oracle dédié au projet

## Installation

```bash
git clone <url-du-depot>
cd TPFinal
python -m venv myenv
source myenv/bin/activate        # Windows : myenv\Scripts\activate
pip install -r requirement.txt
```

## Configuration


```
DB_USER=tpfinal
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=FREEPDB1
SECRET_KEY=une_longue_chaine_aleatoire
DATABASE_URL=oracle+oracledb://tpfinal:votre_mot_de_passe@localhost:1521/?service_name=FREEPDB1
```




## Créer le schéma (migrations)

```bash
alembic upgrade head
```

## Lancer l'API

```bash
uvicorn main:app --reload
```

- API : http://127.0.0.1:8000
- Documentation Swagger : http://127.0.0.1:8000/docs



## Routes principales

### Auth (`/auth`)
| Méthode | Route | Description |
|---|---|---|
| POST | `/auth/users/` | Inscription |
| POST | `/auth/login/` | Connexion, renvoie un token JWT |
| GET | `/auth/me` | Vérifie le token |

### Livres et emprunts (`/emprunt`) – token requis sauf recherche et détail
| Méthode | Route | Description |
|---|---|---|
| GET | `/emprunt/rechercher/{terme}` | Recherche par titre, auteur ou genre |
| GET | `/emprunt/detail/{idlivre}` | Détail d'un livre |
| POST | `/emprunt/emprunt/{livreId}` | Emprunter un livre (si disponible) |
| PATCH | `/emprunt/rendreLivre/{empruntId}` | Rendre un livre |
| GET | `/emprunt/mesEmprunt/` | Mes emprunts (en cours et historique) |

### Administration (`/admin`) – rôle `admin` requis
| Méthode | Route | Description |
|---|---|---|
| POST | `/admin/ajouterLivre` | Ajouter un livre |
| PUT | `/admin/modifierLivre/{livre_id}` | Modifier un livre |
| DELETE | `/admin/supprimerLivre/{idlivre}` | Supprimer un livre (non emprunté) |
| GET | `/admin/historique/{userId}` | Historique d'emprunts d'un utilisateur |
| PATCH | `/admin/promotion/{userID}` | Promouvoir un utilisateur en admin |
| GET | `/admin/isAdmin` | Vérifie le rôle admin |

## Modèle de données

- **users** : id, nom, prenom, email (unique), mdp (haché), telephone, role
- **livres** : id, titre, auteur, genre, date_publication, total, disponibles
- **emprunts** : id, user_id → users, book_id → livres, rendu

Un utilisateur peut emprunter plusieurs livres ; un livre n'est empruntable que si
`disponibles > 0`.

## Tests

Les tests utilisent une base SQLite en mémoire (la base Oracle n'est pas touchée) :

```bash
pytest
```

## Structure du projet

```
main.py            point d'entrée FastAPI
db.py              connexion SQLAlchemy / Oracle
models.py          modèles User, Book, emprunts
serviceJWT.py      création et vérification des tokens
auth/              inscription, connexion, hachage des mots de passe
admin/             routes d'administration
emprunt/           emprunts, recherche, détail
alembic/           migrations
tests/             tests pytest
```

