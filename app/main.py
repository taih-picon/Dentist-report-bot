import os

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import engine, settings
from app.controller.dentist_report_controller import DentisReportController
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # Use the list of origins read from the environment
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()

# Create Services

# sdlafhalk
# Create controllers
dentist_report_controller = DentisReportController(router)
app.include_router(router)
@app.get("/")
async def read_root():
    return {"message": settings.app_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)

    