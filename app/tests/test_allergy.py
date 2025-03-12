# Test cases for the allergy endpoints
import pytest
from fastapi.testclient import TestClient
from app.core.config import config
from app.main import app

client = TestClient(app)

def test_create_allergies():
    response = client.post(
        "/allergies/",
        headers={"access_token": f"{config.API_KEY}"},
        json=[
            {"allergyname": "Peanuts", "type": "Food"},
            {"allergyname": "Dust", "type": "Environmental"}
        ]
    )
    assert response.status_code == 200
    data = response.json()
    assert "added" in data
    assert "existing" in data

def test_get_all_allergies():
    response = client.get(
        "/allergies/",
        headers={"access_token": f"{config.API_KEY}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)



test_id = -1

def test_get_allergy_by_id():
    global test_id
    test_id = -1
    # First, create an allergy to ensure there is one to retrieve
    create_response = client.post(
        "/allergies/",
        headers={"access_token": f"{config.API_KEY}"},
        json=[{"allergyname": "Test Allergy", "type": "Test Type"}]
    )
    assert create_response.status_code == 200
    created_allergy = create_response.json()["added"][0]

    # Now, retrieve the allergy by ID
    allergy_id = created_allergy["allergyid"]
    test_id = allergy_id
    response = client.get(
        f"/allergies/{allergy_id}",
        headers={"access_token": f"{config.API_KEY}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["allergyid"] == allergy_id
    assert data["allergyname"] == "Test Allergy"
    assert data["type"] == "Test Type"

def test_delete_allergy():
    
    if test_id == -1:
        # First, create an allergy to ensure there is one to delete
        create_response = client.post(
            "/allergies/",
            headers={"access_token": f"{config.API_KEY}"},
            json=[{"allergyname": "Delete Allergy", "type": "Delete Type"}]
        )
        assert create_response.status_code == 200
        created_allergy = create_response.json()["added"][0]

        # Now, delete the allergy by ID
        allergy_id = created_allergy["allergyid"]
    else:
        allergy_id = test_id
        
    print(f"AlleryID: {allergy_id}")
    response = client.delete(
        f"/allergies/{allergy_id}",
        headers={"access_token": f"{config.API_KEY}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Allergy deleted successfully"
    
test_delete_allergy()