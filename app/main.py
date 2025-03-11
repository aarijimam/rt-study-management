from fastapi import FastAPI
from app.api.routes import allergy
from app.core.database import Base, engine
import uvicorn

app = FastAPI(title="Study Management API")

# Include allergy routes
app.include_router(allergy.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)