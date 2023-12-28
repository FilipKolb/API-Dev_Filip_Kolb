import requests
import json

def test_read_pokemons():
    response = requests.get('http://127.0.0.1:8000/pokemon/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_pokemon():
    # Assuming there is at least one Pokemon in the testing database
    response = requests.get('http://127.0.0.1:8000/pokemon/1')
    assert response.status_code == 200
    assert "id" in response.json()
    assert "name" in response.json()
    assert "level" in response.json()
    assert "type" in response.json()

def get_token():
    # Replace 'username' and 'password' with valid credentials from your test data
    response = requests.post('http://127.0.0.1:8000/token', data={"username": "test", "password": "test"})
    return response.json()["access_token"]

def test_read_trainers():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get('http://127.0.0.1:8000/trainers/', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_trainer():
    # Assuming there is at least one Trainer in the testing database
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get('http://127.0.0.1:8000/trainers/1', headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "name" in response.json()
    assert "password" not in response.json()  # Password should be excluded