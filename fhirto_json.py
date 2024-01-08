import json
from decimal import Decimal

from fhir.resources.observation import Observation
from fhir.resources.quantity import Quantity

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Load the FHIR data from the previous step
with open("merged_fhir_data.json") as json_data:
    data = json.load(json_data)

fhir_data = {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": []
}

# Process each entry in the loaded FHIR data
for resource in data["entry"]:
    entry = resource["resource"]
    components_list = []

    # Add components based on the CSV data structure
    # Example for Covid Cases, adjust according to actual data structure
    if "CovidCases" in entry:
        components_list.append({
            "code": {"coding": [{"system": "http://loinc.org", "code": "CovidCases"}], "text": "COVID-19 Cases"},
            "valueQuantity": Quantity(value=entry["CovidCases"], unit="cases", system="http://unitsofmeasure.org", code="{cases}")
        })

     # Process Vaccination Rate
    if "VaccinationRate" in entry:
        vaccination_rate = convert_percentage_to_decimal(entry["VaccinationRate"])
        if vaccination_rate is not None:
            components_list.append({
                "code": {"coding": [{"system": "http://loinc.org", "code": "VaccinationRate"}], "text": "Vaccination Rate"},
                "valueQuantity": Quantity(value=vaccination_rate, unit="%", system="http://unitsofmeasure.org", code="{percent}")
            })

    # Process Population
    if "Population" in entry and isinstance(entry["Population"], int):
        components_list.append({
            "code": {"coding": [{"system": "http://loinc.org", "code": "Population"}], "text": "Population"},
            "valueQuantity": Quantity(value=entry["Population"], unit="individuals", system="http://unitsofmeasure.org", code="{individuals}")
        })

    # Process Total Deaths
    if "TotalDeaths" in entry and isinstance(entry["TotalDeaths"], int):
        components_list.append({
            "code": {"coding": [{"system": "http://loinc.org", "code": "TotalDeaths"}], "text": "Total Deaths"},
            "valueQuantity": Quantity(value=entry["TotalDeaths"], unit="deaths", system="http://unitsofmeasure.org", code="{deaths}")
        })

    # Repeat similar blocks for other data points like Vaccination Rate, Population, etc.

# Check if 'Bundesland' or 'City' key exists
    location_key = 'Bundesland' if 'Bundesland' in entry else 'City'
    subject_reference = f"Location/{entry[location_key].lower().replace(' ', '-')}" if location_key in entry else "Location/unknown"

    # Create the observation resource for each entry
    observation = Observation(
        status="final",
        category=[{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "survey"}]}],
        code={"coding": [{"system": "http://loinc.org", "code": "HealthData"}], "text": "Health Statistics"},
        subject={"reference": subject_reference},
        component=components_list
    )

    fhir_data["entry"].append({"resource": observation.dict()})

# Convert the FHIR data to JSON
fhir_json = json.dumps(fhir_data, indent=2, cls=DecimalEncoder)

# Save the JSON to a file
with open("health_data_fhir.json", "w") as f:
    f.write(fhir_json)

print("all good.")
