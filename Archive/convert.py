import pandas as pd
from fhir.resources.bundle import Bundle
from fhir.resources.bundle import BundleEntry, BundleEntryRequest
from fhir.resources.location import Location
from fhir.resources.observation import Observation
from datetime import datetime
import pytz
import uuid

# Load the CSV file
data = pd.read_csv('Archive/cities_data.csv')

# Create a list for bundle entries
bundle_entries = []

for index, row in data.iterrows():
    # Generate a unique fullUrl for each resource
    location_fullUrl = f"urn:uuid:{uuid.uuid4()}"
    observation_cases_fullUrl = f"urn:uuid:{uuid.uuid4()}"
    observation_deaths_fullUrl = f"urn:uuid:{uuid.uuid4()}"

    # Create a Location resource for each city
    location = Location.construct()
    location.name = row['city']
    location.id = f"location-{index}"

    # Check for NaN values in the CSV and replace them with a default value if necessary
    covid_cases = row['covid_cases'] if pd.notna(row['covid_cases']) else 0
    deaths = row['deaths'] if pd.notna(row['deaths']) else 0

    # Format the current datetime in ISO 8601 format without fractional seconds
    current_datetime = datetime.now(pytz.utc).isoformat()

   # Create an Observation resource for COVID-19 cases
    observation_cases = Observation.construct(
        id=f"covid-cases-{index}",
        status='final',
        category=[{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "laboratory"}]
        }],
        code={
            "coding": [{"system": "http://loinc.org", "code": "94500-6", "display": "SARS-CoV-2 (COVID-19) RNA [Presence] in Respiratory specimen by NAA with probe detection"}]
        },
        valueQuantity={
            "value": covid_cases,
            "unit": "cases",
            "system": "http://unitsofmeasure.org",
            "code": "{cases}"
        },
        issued=current_datetime,
        subject={"reference": f"Location/{location.id}"}
    )

    # Create an Observation resource for COVID-19 deaths
    observation_deaths = Observation.construct(
        id=f"covid-deaths-{index}",
        status='final',
        category=[{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "survey"}]  # Adjusted category code
        }],
        code={
            "coding": [{"system": "http://hl7.org/fhir/sid/icd-10-cm", "code": "U07.1", "display": "COVID-19"}]  # Adjusted display name
        },
        valueQuantity={
            "value": deaths,
            "unit": "deaths",
            "system": "http://unitsofmeasure.org",
            "code": "{deaths}"
        },
        issued=current_datetime,
        subject={"reference": f"Location/{location.id}"}
    )



    # Create requests for each entry
    location_request = BundleEntryRequest.construct(method="POST", url="Location")
    observation_cases_request = BundleEntryRequest.construct(method="POST", url="Observation")
    observation_deaths_request = BundleEntryRequest.construct(method="POST", url="Observation")

    # Add resources to bundle entries with fullUrl and request
    bundle_entries.append(BundleEntry.construct(fullUrl=location_fullUrl, resource=location, request=location_request))
    bundle_entries.append(BundleEntry.construct(fullUrl=observation_cases_fullUrl, resource=observation_cases, request=observation_cases_request))
    bundle_entries.append(BundleEntry.construct(fullUrl=observation_deaths_fullUrl, resource=observation_deaths, request=observation_deaths_request))

# Create the bundle
bundle = Bundle.construct()
bundle.type = "batch"
bundle.entry = bundle_entries

# Convert the bundle to JSON
bundle_json = bundle.json(indent=4)

# Output the JSON or save it to a file
print("all good here")

# Save the JSON to a file
with open('new4.json', 'w') as file:
    file.write(bundle_json)
