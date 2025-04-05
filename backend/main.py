from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, scan

app = FastAPI()

app.include_router(upload.router, prefix="/upload")
app.include_router(scan.router, prefix="/scan")

# CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
