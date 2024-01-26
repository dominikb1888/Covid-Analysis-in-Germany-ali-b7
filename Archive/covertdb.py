import json
import sqlite3
from fhir.resources.bundle import Bundle
import pathlib

class JsonInDatabaseTransformer:
    def __init__(self):
        pass

    def create_table(self, cursor):
        # Drop the table if it exists
        # cursor.execute('DROP TABLE IF EXISTS covid_data1;')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS covid_data1(
                city TEXT PRIMARY KEY,
                population INT,
                vaccination_rate DECIMAL,
                covid_cases INT,
                deaths INT,
                covid_cases_2020 INT,
                covid_cases_2021 INT,
                covid_cases_2022 INT
            );
        ''')

    def insert_data(self, cursor, location, data):
        city = location.split("/")[1]
        population = int(data['population'])
        vaccination_rate = float(data['vaccination-rate'])
        covid_cases = int(data['covid-cases'])
        deaths = int(data['deaths'])
        covid_cases_2020 = int(data['covid_cases_2020'])
        covid_cases_2021 = int(data['covid_cases_2021'])
        covid_cases_2022 = int(data['covid_cases_2022'])

        cursor.execute('''
            INSERT OR IGNORE INTO covid_data1 (city, population, vaccination_rate, covid_cases, deaths, 
                                              covid_cases_2020, covid_cases_2021, covid_cases_2022)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        ''', (city, population, vaccination_rate, covid_cases, deaths, 
              covid_cases_2020, covid_cases_2021, covid_cases_2022))

    def push_json_data_in_db(self, json_path, db_name='data11_for_web_application.db'):
    # Connect to the SQLite database
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

    # Create the table
        self.create_table(cursor)

    # Read data from the JSON file
        filename = pathlib.Path(json_path)
        bundle = Bundle.parse_file(filename)
        for entry in bundle.entry:
        # Check if the resource is an Observation
            if entry.resource.resource_type == 'Observation':
                location = entry.resource.subject.reference if entry.resource.subject else None
                data_dict = {}
            
            # Check if component is not None before iterating
                if entry.resource.component:
                    for comp in entry.resource.component:
                        if comp.code and comp.code.coding and comp.valueQuantity:
                            code = comp.code.coding[0].code if comp.code.coding else None
                            value = comp.valueQuantity.value if comp.valueQuantity else None
                            if code and value is not None:
                                data_dict[code] = value

                if location and data_dict:
                    self.insert_data(cursor, location, data_dict)

    # Commit the changes and close the connection
        connection.commit()
        connection.close()




if __name__ == "__main__":
    json_in_db = JsonInDatabaseTransformer()
    json_in_db.push_json_data_in_db('new4.json')

