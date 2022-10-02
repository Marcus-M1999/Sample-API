from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_forward_slash():
    response = client.get("/")
    assert response.status_code == 501 #status code we defined in main.py
    assert response.json() == {"detail": "not implemented"}

def test_hello_multi_name():
    response = client.get("/hello?name=Marcus%20and%20his%20friend")
    assert response.status_code == 200
    assert  response.json() == {"name": "Hello Marcus and his friend"}

def test_hello_marcus():
    response = client.get("/hello?name=marcus")
    assert response.status_code == 200 #status code we defined in main.py
    assert response.json() == {"name": "Hello marcus"}

def test_hello_error():
    response = client.get("/hello?name=")
    assert response.status_code == 422 #status code we defined in main.py
    assert response.json() == {"detail": "Bad Request: Invalid or missing name."}

def test_hello_quotes():
    response = client.get("/hello?name=%22%7B%7D%22")
    assert response.status_code == 200  # status code we defined in main.py
    assert response.json() == {"name": "Hello \"{}\""}



