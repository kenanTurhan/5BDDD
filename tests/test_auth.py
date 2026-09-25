import pytest

# 1. Inscription : Succès
def test_inscription_nouvel_utilisateur(client):
    response = client.post("/auth/users/", json={
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@test.com",
        "telephone": "0600000000",
        "mdp": "motdepassesecurise"
    })
    assert response.status_code == 200 
    data = response.json()
    assert data["email"] == "jean.dupont@test.com"

# 2. Inscription : Erreur 400 
def test_inscription_email_existant(client):
    response = client.post("/auth/users/", json={
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@test.com",
        "telephone": "0600000000",
        "mdp": "motdepassesecurise"
    })
    assert response.status_code == 400 
    assert response.json()["detail"] == "Cet email est déjà enregistré" 

# 3. Inscription : Erreur 422 
def test_inscription_champs_manquants(client):
    response = client.post("/auth/users/", json={
        "nom": "Dupont",
        # "prenom" manquant
        "email": "incomplet@test.com",
        "mdp": "motdepassesecurise"
    })
    assert response.status_code == 422

# 4. Connexion : Succès
def test_login_utilisateur_succes(client):
    response = client.post("/auth/login/", json={
        "email": "jean.dupont@test.com",
        "mdp": "motdepassesecurise"
    })
    assert response.status_code == 200 
    assert "access_token" in response.json() 

# 5. Connexion : Erreur 400 
def test_login_mauvais_email(client):
    response = client.post("/auth/login/", json={
        "email": "inconnu@test.com",
        "mdp": "motdepassesecurise"
    })
    assert response.status_code == 400 
    assert response.json()["detail"] == "Email ou mot de passe incorrect" 

# 6. Connexion : Erreur 400 
def test_login_mauvais_mdp(client):
    response = client.post("/auth/login/", json={
        "email": "jean.dupont@test.com",
        "mdp": "fauxmotdepasse"
    })
    assert response.status_code == 400 
    assert response.json()["detail"] == "Email ou mot de passe incorrect" 

# 7. Route privée "me" : Succès
def test_private_route_me(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200 
    assert "Hello" in response.json()["message"] 
