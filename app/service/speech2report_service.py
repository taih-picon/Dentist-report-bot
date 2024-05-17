from openai import OpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config.settings import OPENAI_API_KEY
from typing import List

speech_client = OpenAI(api_key=OPENAI_API_KEY)




class ToothStatus(BaseModel):
    """The condition of teeth."""
    missing: List[int] = []
    decayed: List[int] = []
    filled: List[int] = []

class ToothAction(BaseModel):
    """Actions to be taken for teeth."""
    treatment_name: str
    teeth: List[int]

class DentalInformation(BaseModel):
    """Dental information including tooth condition and actions."""
    status: ToothStatus
    treatment: List[ToothAction] = Field(description='action applicable on to teeth with problems')

parser = JsonOutputParser(pydantic_object=DentalInformation)

class Speech2ReportService:
    def __init__(self):
        self.speech_client = speech_client
        self.chat_model = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY, model_name = "gpt-4o", temperature= 0.0
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
        paser = JsonOutputParser(pydantic_object = DentalInformation)
        chain = prompt_template | self.chat_model | paser
        result = chain.invoke({"raw_infomation": text, "format": parser.get_format_instructions()})
        return result
