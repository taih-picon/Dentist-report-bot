from openai import OpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config.settings import OPENAI_API_KEY
from typing import List

speech_client = OpenAI(api_key=OPENAI_API_KEY)




class Status(BaseModel):
    missing: List[str] = Field(description="The list of missing teeth.")
    decayed: List[str] = Field(description="The list of decayed teeth.")
    filled: List[str] = Field(description="The list of filled teeth.")

class Treatment(BaseModel):
    treatment_name: str = Field(description="Name of the treatment for teeth.")
    teeth: List[str] = Field(description="The list of teeth for treatment.")

class DentistReport(BaseModel):
    status: Status = Field(description="Status of teeth")
    treatments: List[Treatment] = Field(description="List of treatments for teeth.")

class Speech2ReportService:
    def __init__(self):
        self.speech_client = speech_client
        self.chat_model = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY, model_name = "gpt-4o", temperature= 0.2
        )

    def speech_to_text(self,speech_file_path):
        audio_file = open(speech_file_path, "rb")
        transcript = self.speech_client.audio.transcriptions.create(
            file = audio_file,
            model = "whisper-1",
            language = "en",
            response_format = "verbose_json"
        )
        return transcript.text
    
    def complete_report(self, dentist_report_template, text):
        prompt_template = ChatPromptTemplate.from_template(dentist_report_template)
        paser = JsonOutputParser(pydantic_object = DentistReport)
        chain = prompt_template | self.chat_model | paser
        result = chain.invoke({"raw_infomation": text})
        return result
