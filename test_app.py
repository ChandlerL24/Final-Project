import pytest
from fastapi.testclient import TestClient
from app import app  

client = TestClient(app)

# Test that the root endpoint works and provides instructions
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the Public Health Data API" in response.text
    assert "Use the /health_data endpoint" in response.text

# Test that the /health_data endpoint returns valid data for a given country and year
def test_health_data_valid():
    response = client.get("/health_data?country=Japan&year=2020")
    assert response.status_code == 200
    assert "Japan" in response.text  

# Test the /health_data endpoint with invalid country
def test_health_data_invalid_country():
    response = client.get("/health_data?country=FakeCountry&year=2020")
    assert response.status_code == 404
    assert "Country or year not found." in response.json()  

# Test the /health_data endpoint with invalid year
def test_health_data_invalid_year():
    response = client.get("/health_data?country=USA&year=9999")
    assert response.status_code == 404
    assert "Country or year not found." in response.json()  

# Test the /health_compare endpoint with valid countries and year
def test_health_compare_valid():
    response = client.get("/health_compare?country1=Russia&country2=Canada&year=2020")
    assert response.status_code == 200
    assert "Russia" in response.text  
    assert "Canada" in response.text  

# Test the /health_compare endpoint with invalid countries
def test_health_compare_invalid_countries():
    response = client.get("/health_compare?country1=FakeCountry1&country2=FakeCountry2&year=2020")
    assert response.status_code == 404
    assert "Countries or year not found." in response.json()  

# Test the /health_compare endpoint with aggregation set to False
def test_health_compare_no_aggregation():
    response = client.get("/health_compare?country1=United%20States&country2=Canada&year=2020&aggregate=false")
    assert response.status_code == 200
    assert "United States" in response.text 
    assert "Canada" in response.text 
    assert "Disease Name" in response.text  

# Test the /health_compare endpoint with aggregation set to True (default)
def test_health_compare_with_aggregation():
    response = client.get("/health_compare?country1=United%20States&country2=Canada&year=2020&aggregate=true")
    assert response.status_code == 200
    assert "United States" in response.text  
    assert "Canada" in response.text  
    assert "Disease Name" in response.text  
