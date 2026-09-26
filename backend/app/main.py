from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .api import entities, documents, analysis
from .db.session import engine, Base
# Import all models so SQLAlchemy registers them before create_all
from .models import entity, document, analysis as analysis_model  # noqa: F401

# Create tables (Simplification for now, usually done with Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Credit_IQ (CAMS) API")

# Enable CORS for the React frontend
cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(entities.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Credit_IQ (CAMS) API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
