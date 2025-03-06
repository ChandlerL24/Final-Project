# Public Health Data API

This API provides access to global public health statistics, allowing users to retrieve and compare health data for different countries and years. It utilizes a local CSV file ("Global Health Statistics.csv") as its data source.

## API Methods

1.  **Retrieve Health Data for a Country and Year (`/health_data`)**

    * **Description:** Returns health data for a specific country and year, presented in an HTML table. Data can be aggregated by disease.
    * **Parameters:**
        * `country` (string, required): The name of the country.
        * `year` (integer, required): The year for which to retrieve data.
        * `aggregate` (boolean, optional, default: true): If true, aggregates data by disease, showing mean values for numerical columns.
    * **Data Source:** `Global Health Statistics.csv`
    * **Response:** An HTML table displaying health data, including "Disease Name," "Prevalence Rate (%)", "Mortality Rate (%)", etc.
    * **Example Usage:**
        * `GET /health_data?country=United%20States&year=2020`
        * `GET /health_data?country=Japan&year=2019&aggregate=false`

2.  **Compare Health Data Between Two Countries (`/health_compare`)**

    * **Description:** Compares health data between two specified countries for a given year, presenting the results in two separate HTML tables. Data can be aggregated by disease.
    * **Parameters:**
        * `country1` (string, required): The name of the first country.
        * `country2` (string, required): The name of the second country.
        * `year` (integer, required): The year for comparison.
        * `aggregate` (boolean, optional, default: true): If true, aggregates data by disease, showing mean values for numerical columns.
    * **Data Source:** `Global Health Statistics.csv`
    * **Response:** An HTML page with two tables, one for each country, displaying health data.
    * **Example Usage:**
        * `GET /health_compare?country1=Canada&country2=Mexico&year=2021`
        * `GET /health_compare?country1=Germany&country2=France&year=2022&aggregate=false`

## Getting Started

1.  **Installation:**
    * Ensure you have Python 3.7+ installed.
    * Install the required packages: `pip install fastapi uvicorn pandas tabulate`
2.  **Running the API:**
    * Place your `Global Health Statistics.csv` file in the same directory as the Python script.
    * Run the API using Uvicorn: `uvicorn main:app --reload` (replace `main` with your script's filename if different).
3.  **Accessing the API:**
    * Open your browser or use a tool like `curl` or Postman to access the API endpoints.
    * View the API documentation at `/docs` for interactive exploration.

## Data Source

* The API uses a local CSV file named `Global Health Statistics.csv`. Ensure this file is present in the same directory as your Python script.

## Notes

* Data is loaded into a Pandas DataFrame upon application startup.
* The API returns HTML responses, making it easy to view data in a web browser.
* Error handling is implemented to catch and display issues such as missing data or invalid parameters.
* The code includes logging for debugging and error tracking.

## Future Improvements

* Implement data validation and sanitization.
* Add more robust error handling and logging.
* Consider adding functionality to filter and sort data.
* Connect to external databases or APIs for real-time data.
* Add more detailed API documentation with example responses.
* Implement a more user-friendly frontend.
