from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
token = None

def test_register_user():
    # Define test data
    user_data = {"username": "john_wick", "first_name": "John", "last_name": "Wick", "email": "john@test.com", "password": "password123"}

    # Make a POST request to the /register/ endpoint
    response = client.post("/api/register/", json=user_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response message is the expected one
    assert response.json() == {"message": "User registered successfully"}

def test_login_user():
    global token

    # Define test data
    user_data = {"username": "john_wick", "password": "password123"}

    # Make a POST request to the /login/ endpoint
    response = client.post("/api/login/", json=user_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response contains the access_token key
    assert "token" in response.json()

    # Extract the token from the response JSON
    token = response.json()["token"]

    # Now you can use the token in subsequent requests or tests
    assert token is not None

    # Check if the response message is the expected one
    assert response.json() == {"message": "Login successful", "token": token}

def test_user_authorized():
    global token

    # Define test data
    print(token)
    user_data = {"token": token}

    # Make a POST request to the /login/ endpoint
    response = client.post("/api/authorized/", json=user_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response message is the expected one
    assert response.json() == {"message": "Authorized"}
