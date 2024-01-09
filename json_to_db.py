import json
import sqlite3
import pathlib

def create_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS covid_data;')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS covid_data(
            id INTEGER PRIMARY KEY,
            location TEXT,
            population INT,
            covid_cases INT,
            vaccination_rate DECIMAL,
            total_deaths INT
        );
    ''')

def insert_data(cursor, location, covid_cases, vaccination_rate, population, total_deaths):
    cursor.execute('''
        INSERT INTO covid_data (location, population, covid_cases, vaccination_rate, total_deaths)
        VALUES (?, ?, ?, ?, ?);
    ''', (location, population, covid_cases, vaccination_rate, total_deaths))

def main():
    database_file = 'covid_data.db'
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    create_table(cursor)

    filename = pathlib.Path("health_data_fhir.json")
    with open(filename, 'r') as file:
        data = json.load(file)
        for entry in data["entry"]:
            resource = entry["resource"]
            location = resource["subject"]["reference"].split("/")[1]

            # Initialize variables
            covid_cases = vaccination_rate = population = total_deaths = None

            # Check if 'component' key exists in the resource
            if "component" in resource:
                for component in resource["component"]:
                    code = component["code"]["coding"][0]["code"]
                    value = component["valueQuantity"]["value"]

                    if code == "CovidCases":
                        covid_cases = int(value)
                    elif code == "VaccinationRate":
                        vaccination_rate = float(value)
                    elif code == "Population":
                        population = int(value)
                    elif code == "TotalDeaths":
                        total_deaths = int(value)

                insert_data(cursor, location, covid_cases, vaccination_rate, population, total_deaths)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()