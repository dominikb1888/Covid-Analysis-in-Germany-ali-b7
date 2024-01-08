import pandas as pd
import json
import chardet

# Function to detect the encoding of a file
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Load CSV files with detected encoding
states_df = pd.read_csv("states_data.csv", encoding=detect_encoding("states_data.csv"))
cities_df = pd.read_csv("cities_data.csv", encoding=detect_encoding("cities_data.csv"))

# Create FHIR-like resources
fhir_resources = []

# Add StateData resources
for _, entry in states_df.iterrows():
    resource = {
        "resourceType": "StateData",
        "Bundesland": entry["Bundesland"],
        "CovidCases": entry["Covid Cases"],
        "VaccinationRate": entry["Vaccination Rate"],
        "Population": entry["Population"],
        "TotalDeaths": entry["Total Deaths"],
        "CovidCases2020": entry["covid_cases_2020"],
        "CovidCases2021": entry["covid_cases_2021"],
        "CovidCases2022": entry["covid_cases_2022"]
    }
    fhir_resources.append(resource)