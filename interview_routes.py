import io
import os
import PyPDF2  # type: ignore
import instructor  # type: ignore
from openai import OpenAI
from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi import File, UploadFile

from models import CVAnalysisResponse, Interview, InterviewCreate, InterviewStatus
from database import (
    get_interview,
    set_interview,
    delete_interview,
    get_company,
    set_company,
)
from utils import generate_unique_id

router = APIRouter()


@router.post("/interviews", response_model=Interview)
async def create_interview(interview: InterviewCreate):
    interview_id = generate_unique_id()

    get_company(interview.company_id)
    company = get_company(interview.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    new_interview = Interview(
        id=interview_id,
        status=InterviewStatus.pending,
        company_data=company,
        candidate_data=interview.candidate_data,
    )

    set_interview(new_interview)
    company.interviews.append(new_interview)
    set_company(company)

    return new_interview


@router.get("/interviews/{interview_id}", response_model=Interview)
async def read_interview(interview_id: str):
    interview = get_interview(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


@router.delete("/interviews/{interview_id}")
async def delete_interview_route(interview_id: str):
    interview = get_interview(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    company = get_company(interview.company_data.id)
    if company:
        company.interviews = [i for i in company.interviews if i != interview_id]
        set_company(company)

    delete_interview(interview_id)
    return {"message": "Interview deleted successfully"}

api_key = os.getenv("OPENAI_API_KEY")
client = instructor.from_openai(OpenAI(api_key=api_key))


def get_cv_data(cv_text: str) -> CVAnalysisResponse:
    cv_data = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=CVAnalysisResponse,
        messages=[{"role": "user", "content": cv_text}],
    )
    return cv_data


@router.post("/interviews/upload_cv", response_model=CVAnalysisResponse)
async def upload_cv(file: UploadFile = File(...)):
    pdf_content = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))

    cv_text = ""
    for page in pdf_reader.pages:
        cv_text += page.extract_text()

    response = get_cv_data(cv_text)

    return response
