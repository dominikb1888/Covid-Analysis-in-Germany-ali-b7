import json
import sqlite3
import pathlib

def create_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS covid_data;')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS covid_data(
            id INTEGER PRIMARY KEY,
            city TEXT,
            population INT,
            covid_cases INT,
            covid_cases_2020 INT,
            covid_cases_2021 INT,
            covid_cases_2022 INT,
            vaccination_rate DECIMAL,
            deaths INT
        );
    ''')

def insert_data(cursor, city, population, covid_cases, covid_cases_2020, covid_cases_2021, covid_cases_2022, vaccination_rate, deaths):
    cursor.execute('''
        INSERT INTO covid_data (city, population, covid_cases, covid_cases_2020, covid_cases_2021, covid_cases_2022, vaccination_rate, deaths)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    ''', (city, population, covid_cases, covid_cases_2020, covid_cases_2021, covid_cases_2022, vaccination_rate, deaths))

def main():
    database_file = 'test2.db'
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    create_table(cursor)

    filename = pathlib.Path("covid_data.json")
    with open(filename, 'r') as file:
        data = json.load(file)
        for entry in data["entry"]:
            resource = entry["resource"]

            # Extract data from the resource
            city = resource["City"]
            population = int(resource["Population"])
            covid_cases = int(resource["CovidCases"])
            covid_cases_2020 = int(resource["CovidCases2020"])
            covid_cases_2021 = int(resource["CovidCases2021"])
            covid_cases_2022 = int(resource["CovidCases2022"])
            # Convert vaccination rate from percentage string to decimal
            vaccination_rate = float(resource["VaccinationRate"].rstrip('%')) / 100
            deaths = int(resource["Deaths"])

            insert_data(cursor, city, population, covid_cases, covid_cases_2020, covid_cases_2021, covid_cases_2022, vaccination_rate, deaths)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
