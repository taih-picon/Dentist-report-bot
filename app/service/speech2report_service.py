from openai import OpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config.settings import OPENAI_API_KEY


speech_client = OpenAI(api_key=OPENAI_API_KEY)


class Dentist_Report(BaseModel):
    """Dentist report from speech."""
    patient_name : str = Field(description="Patient name")
    date_of_birth : str = Field (description = "Birth day of patient")
    address : str = Field (description = "patient address")
    contact_number : str = Field (description =" patient contact number")
    dental_health_history : str = Field(description = "Dental health history of patient")
    examination_findings : str = Field(description = "Examination findings of patient")
    diagnois: str = Field(description="Diagnosis of patient")
    treatment_plan : str = Field(description="treatment plan for patient")
    advice_and_guidance: str = Field(description="advice and guidance for patient")
    conclusion : str = Field(description="conclusion"),

class Speech2ReportService:
    def __init__(self):
        self.speech_client = speech_client
        self.chat_model = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY, model_name = "gpt-3.5-turbo", temperature= 0.2
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
        paser = JsonOutputParser(pydantic_object = Dentist_Report)
        chain = prompt_template | self.chat_model | paser
        result = chain.invoke({"raw_infomation": text})
        return result
