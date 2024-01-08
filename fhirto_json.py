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

    # Repeat similar blocks for other data points like Vaccination Rate, Population, etc.

    # Create the observation resource for each entry
    observation = Observation(
        status="final",
        category=[{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "survey"}]}],
        code={"coding": [{"system": "http://loinc.org", "code": "HealthData"}], "text": "Health Statistics"},
        subject={"reference": f"Location/{entry['Bundesland'].lower().replace(' ', '-')}"},
        component=components_list
    )

    fhir_data["entry"].append({"resource": observation.dict()})

# Convert the FHIR data to JSON
fhir_json = json.dumps(fhir_data, indent=2, cls=DecimalEncoder)

# Save the JSON to a file
with open("health_data_fhir.json", "w") as f:
    f.write(fhir_json)

print("all good.")
