from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
)

def get_db_connection():
    conn = sqlite3.connect('covid_data.db')  
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def get_html():
    return FileResponse("index.html")

@app.get("/data")
def read_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM covid_data').fetchall()
    conn.close()
    return [dict(item) for item in items]

@app.get("/fhir/city/{city_id}")
def get_city(city_id: int):
    conn = get_db_connection()
    city = conn.execute('SELECT * FROM fhir_city WHERE id = ?', (city_id,)).fetchone()
    conn.close()
    if city:
        return dict(city)
    raise HTTPException(status_code=404, detail="City not found")

@app.post("/fhir/city")
def create_city(city_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO fhir_city (city, population, vaccination_rate, covid_cases, deaths, covid_cases_2020, covid_cases_2021, covid_cases_2022) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    ''', (city_data['City'], city_data['Population'], city_data['VaccinationRate'], city_data['CovidCases'], city_data['Deaths'], city_data['CovidCases2020'], city_data['CovidCases2021'], city_data['CovidCases2022']))
    conn.commit()
    conn.close()
    return {"message": "City data created successfully"}

@app.put("/fhir/city/{city_id}")
def update_city(city_id: int, city_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE fhir_city
        SET city = ?, population = ?, vaccination_rate = ?, covid_cases = ?, deaths = ?, covid_cases_2020 = ?, covid_cases_2021 = ?, covid_cases_2022 = ?
        WHERE id = ?;
    ''', (city_data['City'], city_data['Population'], city_data['VaccinationRate'], city_data['CovidCases'], city_data['Deaths'], city_data['CovidCases2020'], city_data['CovidCases2021'], city_data['CovidCases2022'], city_id))
    conn.commit()
    conn.close()
    return {"message": "City data updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

app.mount("/", StaticFiles(directory="./", html=True), name="static")



# run application
# uvicorn main:app --host 127.0.0.1 --port 8080 --reload
