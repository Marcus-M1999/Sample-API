import sys
sys.path.append('../')
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app
from datetime import datetime
import requests
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

def test_predict_good():
    response = requests.post("http://localhost:8000/predict",
                           data={"MedInc":8.3252, "HouseAge":41, "AveRooms":6.98412698, "AveBedrms":1.02380952, "Population":322
                               , "AveOccup":2.55555556, "Latitude":37.88, "Longitude":-122.23})
    print(response.request)
    print(response.content)
    print(response.json())
    assert response.status_code == 200  # status code we defined in main.py
    assert response.json() == {"output(s)": [4.413388694639972]}

def test_predict_good_2():
    data = {'MedInc': 8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0
        , 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23}
    response = client.post("/predict",
                           headers={"data": "Input"},
                           json=data)
    print(response.headers)
    assert response.status_code == 200  # status code we defined in main.py

    assert response.json() == {"output(s)": [4.413388694639972]}

def test_predict_bad_feature():
    response = client.post("/predict",
                           headers={"HouseAge": "Age of House",
                                    "AveRooms": "Average number of Rooms", "AveBedrms": "Average number of Bedrooms"
                               , "Population": "Population of area", "AveOccup": "Avearge Occupancy",
                                    "Latitude": "Lattitude", "Longitude": "Longitude"},
                           json={'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556
                               , 'Latitude': 37.88, 'Longitude': -122.23})
    assert response.status_code == 422  # status code we defined in main.py
    assert response.json() == {'detail': [{'loc': ['query', 'data'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_predict_bad_value():
    response = client.post("/predict",
                           headers={"MedInc": "Medium Income", "HouseAge": "Age of House",
                                    "AveRooms": "Average number of Rooms", "AveBedrms": "Average number of Bedrooms"
                               , "Population": "Population of area", "AveOccup": "Avearge Occupancy",
                                    "Latitude": "Lattitude", "Longitude": "Longitude"},
                           json={'MedInc': -15551, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0
                               , 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23})
    assert response.status_code == 422  # status code we defined in main.py
    assert response.json() == {'detail': [{'loc': ['query', 'data'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_predict_multi_vals():
    response = client.post("/predict",
                           headers={"MedInc": "Medium Income", "HouseAge": "Age of House",
                                    "AveRooms": "Average number of Rooms", "AveBedrms": "Average number of Bedrooms"
                               , "Population": "Population of area", "AveOccup": "Avearge Occupancy",
                                    "Latitude": "Lattitude", "Longitude": "Longitude"},
                           json={'MedInc': -15551, 'Extra input': 989, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0
                               , 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23})
    assert response.status_code == 422  # status code we defined in main.py
    assert response.json() == {'detail': [{'loc': ['query', 'data'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200 #status code we defined in main.py
    assert response.json()["Current Date/Time"][:16] == datetime.now().isoformat()[:16]
