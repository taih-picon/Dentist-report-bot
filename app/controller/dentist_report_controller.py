import asyncio
import json
import shutil
import logging
import os

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status

from app.service.speech2report_service import Speech2ReportService
from app.controller.prompts import DENTIS_REPORT_PROMPT
from app.config.settings import SessionLocal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

speech2report_service = Speech2ReportService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DentisReportController:
    def __init__(self,router: APIRouter = Depends()) :
        self.router = router

        @self.router.post("/api/speech_recognition_to_report")
        async def speech_recognition_to_report(
            background_tasks: BackgroundTasks, files: list[UploadFile] = File(...)
        ):
            try: 
                upload_folder = "uploads"
                os.makedirs(upload_folder, exist_ok = True)
                for uploaded_file in files:
                    with open(
                        os.path.join(upload_folder,uploaded_file.filename), "wb"
                    ) as buffer:
                        shutil.copyfileobj(uploaded_file.file, buffer)
                file_path = os.path.join(upload_folder, uploaded_file.filename)
                text = speech2report_service.speech_to_text(speech_file_path = file_path)
                print(text)
                report = speech2report_service.complete_report(DENTIS_REPORT_PROMPT,text)
                print(report)
                background_tasks.add_task(remove_file_in_folder, upload_folder)
                return {"status": "Ok", "code": 200, "data": report}
            except Exception as e:
                logger.error(f'Erro speech generate answer: {e}')
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = "Failed to speech generate answer"
                )
        async def remove_file_in_folder(directory):
            await asyncio.sleep(5)
            try:
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        logger.info(f"Removed file: {file_path}")
            except Exception as e:
                logger.error(f"Error removing files in directory: {e}")