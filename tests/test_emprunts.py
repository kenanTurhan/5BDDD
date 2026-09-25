import pytest

# 1. Emprunter un livre : Succès
def test_emprunter_livre_disponible(client, auth_headers):
    response = client.post("/emprunt/emprunt/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["rendu"] == False

# 2. Emprunter un livre : Erreur 404
def test_emprunter_livre_non_trouve(client, auth_headers):
    response = client.post("/emprunt/emprunt/999", headers=auth_headers)
    assert response.status_code == 404 
    assert response.json()["detail"] == "livre pas trouvé"

# 3. Emprunter plusieurs livres simultanément
def test_emprunter_plusieurs_livres(client, auth_headers):
    client.post("/emprunt/emprunt/1", headers=auth_headers)
    response = client.post("/emprunt/emprunt/2", headers=auth_headers)
    assert response.status_code == 200 

# 4. Emprunter un livre : Erreur 403
def test_emprunter_livre_indisponible(client, auth_headers):
    response = client.post("/emprunt/emprunt/3", headers=auth_headers)
    assert response.status_code == 403 #[cite: 4]
    assert response.json()["detail"] == "Plus de stock"

# 5. Consulter ses propres emprunts
def test_consultation_mes_emprunts(client, auth_headers):
    response = client.get("/emprunt/mesEmprunt/", headers=auth_headers)
    assert response.status_code == 200 
    assert isinstance(response.json(), list) 

# 6. Rendre un livre : Succès et mise à jour stock
def test_rendre_livre_succes(client, auth_headers):
    livre_avant = client.get("/emprunt/detail/1").json()
    stock_avant = livre_avant["disponibles"]

    # ID d'emprunt = 1
    response = client.patch("/emprunt/rendreLivre/1", headers=auth_headers)
    assert response.status_code == 200 
    assert response.json()["message"] == "Livre rendu" 

    livre_apres = client.get("/emprunt/detail/1").json()
    assert livre_apres["disponibles"] == stock_avant + 1 

# 7. Rendre un livre : Erreur 404 
def test_rendre_livre_deja_rendu(client, auth_headers):
    response = client.patch("/emprunt/rendreLivre/1", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Emprunt déjà rendu" 

# 8. Historique global pour un Admin
def test_generation_historique_emprunts_admin(client, admin_headers):
    response = client.get("/admin/historique/1", headers=admin_headers)
    assert response.status_code == 200 
    assert isinstance(response.json(), list)

# 9. Promouvoir un utilisateur en Admin : Succès
def test_promouvoir_admin_succes(client, admin_headers):
    response = client.patch("/admin/promotion/2", headers=admin_headers)
    assert response.status_code == 200 
    assert response.json()["role"] == "admin" 

# 10. Promouvoir un utilisateur en Admin : Erreur 404
def test_promouvoir_admin_non_trouve(client, admin_headers):
    response = client.patch("/admin/promotion/999", headers=admin_headers)
    assert response.status_code == 404 
    assert response.json()["detail"] == "L'utilisateur n'éxiste pas"