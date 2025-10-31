from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel # type: ignore

app = FastAPI()

@app.get(f"/")
def root():
    return {"message": "Hello World from FastAPI!"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 