from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
from jsonindb import JsonInDatabaseTransformer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db_connection():
    conn = sqlite3.connect('data_for_web_application.db')  # Adjust the path to your database file if necessary
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def get_html():
    return FileResponse("index.html")


@app.get("/data")
def read_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM covid_data1').fetchall()
    conn.close()
    return [dict(item) for item in items]

"""
@app.get("/data2")
def read_items():
    conn = get_db_connection()
    items = conn.execute('SELECT city, covid_cases_2020, covid_cases_2021, covid_cases_2022  FROM covid_data1').fetchall()  # Replace 'your_table_name' with your actual table name
    conn.close()
    return [dict(item) for item in items]
"""

@app.post("/uploadjson/")
async def upload_json(file: UploadFile = File(...)):
    if file.filename.endswith(".json"):
        try:
            temp_file_path = f"temp_{file.filename}"
            with open(temp_file_path, "wb") as temp_file:
                content = await file.read()
                temp_file.write(content)

            json_in_db = JsonInDatabaseTransformer()
            json_in_db.push_json_data_in_db(temp_file_path)

            return {"status": "File uploaded and data inserted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing JSON file: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Uploaded file must be a JSON file")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

# run application
# uvicorn main:app --host 127.0.0.1 --port 8080 --reload
app.mount("/", StaticFiles(directory="./", html=True), name="static")