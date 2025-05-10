from fastapi.testclient import TestClient
from main import app, reset_data
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_function():
    reset_data()

    client.post("/add", json={"lat": 55.7526, "lng": 37.6211, "name": "St. Basil's Cathedral", "type": "Place of Worship",
        "description": "The Cathedral of Vasily the Blessed, commonly known as Saint Basil's Cathedral, is a church in Red Square in Moscow, Russia.",})
    client.post("/add", json={"lat": 48.8584, "lng": 2.2945, "name": "Eiffel Tower", "type": "Monument",
        "description": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",})
    client.post("/add", json={"lat": 40.6892, "lng": -74.0445, "name": "Statue of Liberty", "type": "Monument",
        "description": "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor in New York City.",})


def test_get_all():
    response = client.get("/get_all")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_all_name_type_sort_search():
    response = client.get("/get_all_name_type_sort", params={"search": "Monument"})
    assert response.status_code == 200
    assert all("monument" in f"{l['type']}".lower() for l in response.json())


def test_get_all_name_type_sort_by_lat():
    response = client.get("/get_all_name_type_sort", params={"sort": 1})
    data = response.json()
    assert response.status_code == 200
    assert data[0]["lat"] >= data[1]["lat"]


def test_get_all_name():
    response = client.get("/get_all_name", params={"search": "eiffel"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Eiffel Tower"


def test_add_landmark():
    response = client.post("/add", json={"lat": 41.8902, "lng": 12.4922, "name": "Colosseum", "type": "Ancient Ruins",
        "description": "The Colosseum is an oval amphitheatre in the centre of the city of Rome, Italy, the largest ancient amphitheatre ever built.",})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Colosseum"
    assert data["id"] == 4

def test_add_bad_data():
    response = client.post("/add", json={"lat": 100, "lng": 12.4922, "name": "Colosseum", "type": "Ancient Ruins",
        "description": "The Colosseum is an oval amphitheatre in the centre of the city of Rome, Italy, the largest ancient amphitheatre ever built.",})
    assert response.status_code == 422


def test_delete_landmark():
    response = client.delete("/delete/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"
    assert all(l["id"] != 1 for l in client.get("/get_all").json())


def test_delete_nonexistent():
    response = client.delete("/delete/999")
    assert response.status_code == 404


def test_update_landmark():
    response = client.patch("/update/2", json={
        "lat": 40.6892, "lng": -74.0445, "name": "Statue of Liberty Updated", "type": "Monument",
        "description": "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor in New York City."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Statue of Liberty Updated"


def test_update_nonexistent():
    response = client.patch("/update/999", json={
        "lat": 40.6892, "lng": -74.0445, "name": "Ghost", "type": "Myth",
        "description": "No one sees it",
    })
    assert response.status_code == 404

def test_update_bad_data():
    response = client.patch("/update/999", json={
        "lat": 1000.6892, "lng": -74.0445, "name": "Ghost", "type": "Myth",
        "description": "No one sees it",
    })
    assert response.status_code == 422
