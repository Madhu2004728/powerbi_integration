from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import powerbi

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],     # Allows all HTTP methods
    allow_headers=["*"],     # Allows all headers
)

app.include_router(
    powerbi.router,
    prefix="/api/powerbi",
    tags=["Power BI"]
)