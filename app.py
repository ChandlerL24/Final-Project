import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import pandas as pd
from tabulate import tabulate

# Configure logging for debugging and error tracking
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Public Health Data API",
    description="An API for accessing and exploring public health statistics.",
    version="1.0.0",
)

# Load CSV data into a Pandas DataFrame upon application startup
try:
    df = pd.read_csv("Global Health Statistics.csv")  
    logger.info("CSV loaded successfully!")
except Exception as e:
    logger.error(f"Error loading CSV file: {str(e)}")
    raise HTTPException(status_code=500, detail="Error loading CSV file")

# Root endpoint: Displays a welcome message and API usage instructions
@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint, displays a welcome message.
    """
    html_content = """
    <html>
        <head>
            <title>Public Health Data API</title>
        </head>
        <body>
            <h1>Welcome to the Public Health Data API program!</h1>
            <p>Use the /health_data endpoint to get data for a place and year.</p>
            <p>Use the /health_compare endpoint to compare data for two places and a year.</p>
            <p>Visit /docs to see the API documentation.</p>
        </body>
    </html>
    """
    return html_content

# Endpoint to retrieve health data for a single country and year
@app.get("/health_data", response_class=HTMLResponse)
async def health_data(
    country: str = Query(..., description="Country to retrieve data for"),
    year: int = Query(..., description="Year to retrieve data for"),
    aggregate: bool = Query(True, description="Aggregate data by disease?"),
):
    """
    Returns selected data for a specified country and year, with optional aggregation.
    """
    try:
        # Define the columns to be retrieved from the CSV
        selected_columns = [
            "Country",
            "Disease Name",
            "Prevalence Rate (%)",
            "Mortality Rate (%)",
            "Availability of Vaccines/Treatment",
            "Healthcare Access (%)",
            "Average Treatment Cost (USD)",
            "Recovery Rate (%)",
        ]

        # Find rows matching the specified country and year
        matching_rows = []
        for index, row in df.iterrows():
            if row["Country"].lower() == country.lower() and row["Year"] == year:
                matching_rows.append(row[selected_columns])

        # Raise an error if no matching data is found
        if not matching_rows:
            raise HTTPException(status_code=404, detail="Country or year not found.")

        # Create a DataFrame from the matching rows
        matching_df = pd.DataFrame(matching_rows)

        # Aggregate data by disease if requested
        if aggregate:
            numerical_cols = matching_df.select_dtypes(include=['number']).columns
            matching_df = matching_df.groupby("Disease Name")[numerical_cols].mean().reset_index()

        # Generate an HTML table from the DataFrame
        data_table = tabulate(matching_df, headers="keys", tablefmt="html")

        # Create the HTML response
        html_content = f"""
        <html>
            <head>
                <title>Health Data for {country} ({year})</title>
                <style>
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                </style>
            </head>
            <body>
                <h1>Health Data for {country} ({year})</h1>
                {data_table}
            </body>
        </html>
        """
        return html_content

    # Handle any exceptions during data retrieval
    except Exception as e:
        logger.error(f"Error retrieving health data: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error retrieving health data: {str(e)}")


# Endpoint to compare health data between two countries for a given year
@app.get("/health_compare", response_class=HTMLResponse)
async def health_compare(
    country1: str = Query(..., description="First country to compare"),
    country2: str = Query(..., description="Second country to compare"),
    year: int = Query(..., description="Year to compare"),
    aggregate: bool = Query(True, description="Aggregate data by disease?"),
):
    """
    Compares selected health data for two countries in a given year, with aggregation.
    """
    try:
        # Define the columns to be retrieved from the CSV
        selected_columns = [
            "Country",
            "Disease Name",
            "Prevalence Rate (%)",
            "Mortality Rate (%)",
            "Availability of Vaccines/Treatment",
            "Healthcare Access (%)",
            "Average Treatment Cost (USD)",
            "Recovery Rate (%)",
        ]

        # Find rows matching the specified countries and year
        country1_rows = []
        country2_rows = []

        for index, row in df.iterrows():
            if row["Year"] == year:
                if row["Country"].lower() == country1.lower():
                    country1_rows.append(row[selected_columns])
                elif row["Country"].lower() == country2.lower():
                    country2_rows.append(row[selected_columns])

        # Raise an error if no matching data is found
        if not country1_rows or not country2_rows:
            raise HTTPException(status_code=404, detail="Countries or year not found.")

        # Create DataFrames from the matching rows
        country1_df = pd.DataFrame(country1_rows)
        country2_df = pd.DataFrame(country2_rows)

        # Aggregate data by disease if requested
        if aggregate:
            numerical_cols = country1_df.select_dtypes(include=['number']).columns
            country1_df = country1_df.groupby("Disease Name")[numerical_cols].mean().reset_index()
            numerical_cols = country2_df.select_dtypes(include=['number']).columns
            country2_df = country2_df.groupby("Disease Name")[numerical_cols].mean().reset_index()

        # Generate HTML tables for each country
        table1 = tabulate(country1_df, headers="keys", tablefmt="html")
        table2 = tabulate(country2_df, headers="keys", tablefmt="html")

        # Create the HTML response for comparison
        html_content = f"""
        <html>
            <head>
                <title>Health Comparison: {country1} vs. {country2} ({year})</title>
                <style>
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                </style>
            </head>
            <body>
                <h1>Health Comparison: {country1} vs. {country2} ({year})</h1>
                <h2>{country1}</h2>
                {table1}
                <h2>{country2}</h2>
                {table2}
            </body>
        </html>
        """
        return html_content

    except HTTPException as http_exc:
        logger.error(f"HTTPException: {str(http_exc)}")
        raise http_exc

    # Handles any other exceptions during data comparison
    except Exception as e:
        logger.error(f"Error comparing health data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred while comparing health data.")
