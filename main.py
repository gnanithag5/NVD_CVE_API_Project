from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Define a simple route
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
