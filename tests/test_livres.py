import pytest

# 1. Vérification rôle admin : Succès
def test_is_admin_success(client, admin_headers):
    response = client.get("/admin/isAdmin", headers=admin_headers)
    assert response.status_code == 200 
    assert "Vous êtes bibliothécaire" in response.json()["message"] 

# 2. Vérification rôle admin : Erreur 400 
def test_is_admin_forbidden(client, auth_headers):
    response = client.get("/admin/isAdmin", headers=auth_headers)
    assert response.status_code == 400 
    assert response.json()["detail"] == "Cette action est réservé au bibliothequaires" 

# 3. Ajouter un livre : Succès 
def test_ajouter_livre_admin(client, admin_headers):
    response = client.post("/admin/ajouterLivre", json={
        "titre": "Dune",
        "auteur": "Frank Herbert",
        "genre": "Science-Fiction",
        "date_publication": "1965-08-01",
        "total": 5,
        "disponibles": 5
    }, headers=admin_headers)
    assert response.status_code == 200 
    assert response.json()["titre"] == "Dune" 

# 4. Modifier un livre : Succès
def test_modifier_livre(client, admin_headers):
    response = client.put("/admin/modifierLivre/1", json={"disponibles": 4}, headers=admin_headers)
    assert response.status_code == 200 
    assert response.json()["disponibles"] == 4 

# 5. Modifier un livre : Erreur 404
def test_modifier_livre_non_trouve(client, admin_headers):
    response = client.put("/admin/modifierLivre/999", json={"disponibles": 4}, headers=admin_headers)
    assert response.status_code == 404 
    assert response.json()["detail"] == "Livre non trouvé" 

# 6. Recherche livre : Succès
def test_rechercher_livre_succes(client):
    response = client.get("/emprunt/rechercher/Herbert")
    assert response.status_code == 200 
    assert len(response.json()) > 0 

# 7. Recherche livre : Erreur 404 
def test_rechercher_livre_non_trouve(client):
    response = client.get("/emprunt/rechercher/Zfzefzef")
    assert response.status_code == 404 
    assert response.json()["detail"] == "Aucun livre correspond à la recherche" 

# 8. Détail livre : Succès
def test_detail_livre_specifique(client):
    response = client.get("/emprunt/detail/1")
    assert response.status_code == 200 

# 9. Détail livre : Erreur 404
def test_detail_livre_non_trouve(client):
    response = client.get("/emprunt/detail/999")
    assert response.status_code == 404 
    assert response.json()["detail"] == "Aucun livre correspond à la recherche" 

# 10. Supprimer livre : Erreur 403 
def test_supprimer_livre_emprunte(client, admin_headers):
    response = client.delete("/admin/supprimerLivre/1", headers=admin_headers)
    assert response.status_code == 403 
    assert response.json()["detail"] == "Le livre est actuelement emprumpter" 

# 11. Supprimer livre : Succès
def test_supprimer_livre(client, admin_headers):
    response = client.delete("/admin/supprimerLivre/2", headers=admin_headers)
    assert response.status_code == 200 