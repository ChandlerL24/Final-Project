from fastapi import FastAPI, HTTPException
from typing import Optional
import requests


# FastAPI app setup
app = FastAPI()


@app.get('/')
def default_route():
    return {'Welcome to the Public Health Data API Program!'}

# Replace with your actual API key from City Health Dashboard
API_KEY = "41a57425-dbc2-4c8d-ba88-230d28dbf38e"
CITY_HEALTH_DASHBOARD_API_URL = "https://www.cityhealthdashboard.com/api/data/"

# Helper function to fetch data from City Health Dashboard API
def fetch_data_from_city_health_dashboard(endpoint: str, params: Optional[dict] = None):
    headers = {
        "Authorization": f"Bearer {API_KEY}"  # Authentication with Bearer token
    }

    # Construct the full URL for the API request
    url = f"{CITY_HEALTH_DASHBOARD_API_URL}{endpoint}"

    # Send a GET request to the API
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {response.text}")

    # Return the JSON response from the API
    return response.json()


# Method to fetch city-level disease statistics (e.g., for COVID-19 or Flu)
@app.get("/disease-statistics")
def get_disease_statistics(city_name: str):
    # Example disease data fetch (Modify based on actual disease data sources if available)
    params = {
        "token": API_KEY,
        "geo_name": city_name.replace(" ", "+"),
        "geo_level": "city"
    }

    try:
        data = fetch_data_from_city_health_dashboard("metric-data/1", params=params)  # Use appropriate metric ID for disease
        return data
    except HTTPException as e:
        raise e


# Method to fetch vaccination rates for a given city
@app.get("/vaccination-rates")
def get_vaccination_rates(city_name: str):
    # Replace with the correct metric ID for vaccination rates
    params = {
        "token": API_KEY,
        "geo_name": city_name.replace(" ", "+"),
        "geo_level": "city"
    }

    try:
        data = fetch_data_from_city_health_dashboard("metric-data/5", params=params)  # Adjust with the appropriate metric ID for vaccination
        return data
    except HTTPException as e:
        raise e


# Method to fetch trend data for a given city and disease
@app.get("/trend-analysis")
def trend_analysis(city_name: str, disease: str):
    # Fetch historical trend data for the specified city and disease (metric_id for the disease)
    disease_metrics = {"flu": "1", "covid": "2"}  # Define the metric ID mapping for diseases

    if disease not in disease_metrics:
        raise HTTPException(status_code=400, detail="Invalid disease name")

    metric_id = disease_metrics[disease]
    params = {
        "token": API_KEY,
        "geo_name": city_name.replace(" ", "+"),
        "geo_level": "city"
    }

    try:
        data = fetch_data_from_city_health_dashboard(f"metric-data/{metric_id}", params=params)
        return data
    except HTTPException as e:
        raise e


# Method for comparing health metrics across cities
@app.get("/compare")
def compare_health_metrics(cities: str, metrics: Optional[str] = None):
    city_list = cities.split(',')
    comparison_data = {}

    for city in city_list:
        # Example: Comparing vaccination rates and disease statistics
        try:
            params = {
                "token": API_KEY,
                "geo_name": city.replace(" ", "+"),
                "geo_level": "city"
            }

            # Get health metrics for each city (vaccination, disease, etc.)
            disease_data = fetch_data_from_city_health_dashboard("metric-data/1", params=params)
            vaccination_data = fetch_data_from_city_health_dashboard("metric-data/5", params=params)

            comparison_data[city] = {
                "disease_data": disease_data,
                "vaccination_data": vaccination_data
            }
        except HTTPException as e:
            comparison_data[city] = {"error": f"Error fetching data: {e.detail}"}

    return comparison_data


# Method to fetch risk assessment based on disease data and vaccination rates
@app.get("/risk-assessment")
def risk_assessment(city_name: str):
    # Risk assessment based on diseases (e.g., COVID-19) and vaccination rates
    disease_data = get_disease_statistics(city_name)
    vaccination_data = get_vaccination_rates(city_name)

    # Simplified risk level calculation
    covid_cases = disease_data.get('value', 0)  # Replace with actual data keys
    vaccination_rate = vaccination_data.get('value', 0)

    # Risk assessment logic
    if covid_cases > 10000 and vaccination_rate < 70:
        risk_level = "High"
    elif covid_cases > 5000 and vaccination_rate < 85:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {"city": city_name, "risk_level": risk_level}


# Endpoint to fetch geographies for a given state (e.g., Alabama)
@app.get("/geographies")
def get_geographies(state_abbr: str, census_parent_shape_year: str = "2020"):
    params = {
        "token": API_KEY,
        "state_abbr": state_abbr,
        "census_parent_shape_year": census_parent_shape_year
    }

    try:
        data = fetch_data_from_city_health_dashboard("geographies", params=params)
        return data
    except HTTPException as e:
        raise e

