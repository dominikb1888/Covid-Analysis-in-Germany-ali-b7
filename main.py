from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Serve static files (HTML, JS, CSS)
app.mount("/", StaticFiles(directory="./", html=True), name="static")


# Endpoint to serve the HTML file
@app.get("/")
def get_html():
    return FileResponse("./index.html")


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

# run application
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload
