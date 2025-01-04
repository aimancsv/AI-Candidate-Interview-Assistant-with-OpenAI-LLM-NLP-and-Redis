import os
import shutil
from openai import OpenAI
from congruent.congruence_model.collaborative_filtering_similarity import (
    collaborative_filtering_similarity,
)
import instructor  # type: ignore
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from congruent.call_llm import call_llm
from congruent.call_llm.call_tts import generate_audio_stream
from congruent.call_llm.call_stt import call_sst
from congruent.call_llm.call_llm import llm_messages
from congruent.chat_history.redis import (
    retrieve_dialogue,
)
from congruent.interview_main.prompt_formatters import (
    format_company_attributes_assessment,
    get_interview_prompt,
)
from database import (
    get_company_values,
    get_interview,
    set_interview,
    update_company_interview,
)
from models import AttributeScores, CompanyAttributes, InterviewStatus

router = APIRouter()

api_key = os.getenv("OPENAI_API_KEY")
client = instructor.from_openai(OpenAI(api_key=api_key))

prompt = """
given this conversation conversion, please assess the following attributes and return a score for each attribute, you should be critical but fair in your assessment, dont be too nice:

{attributes}
"""


def get_conversation_assessment(
    chat_history, company_attributes: CompanyAttributes
) -> AttributeScores:
    formatted_attributes = format_company_attributes_assessment(company_attributes)
    messages = llm_messages(
        chat_history=chat_history,
        prompt=prompt.format(
            attributes=formatted_attributes,
        ),
        user_message="assess the candidate",
    )
    assessment_result = client.chat.completions.create(
        model="gpt-4o",
        response_model=AttributeScores,
        messages=messages,
    )
    return assessment_result


@router.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...), interview_id: str = Form(...)):
    try:
        upload_dir = "./uploads"
        os.makedirs(upload_dir, exist_ok=True)
        print("Received file:", audio.filename)

        file_path = os.path.join(upload_dir, audio.filename)  # type: ignore
        print("interview_data:", interview_id)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        transcribed_text = call_sst(file_path)
        interview_data = get_interview(interview_id)
        if interview_data is None:
            return JSONResponse(
                status_code=404,
                content={
                    "message": "Interview not found",
                    "error": "Interview not found",
                },
            )
        company_attributes = get_company_values(interview_data.company_data.id)
        if company_attributes is None:
            return JSONResponse(
                status_code=404,
                content={
                    "message": "Company attributes not found",
                    "error": "Company attributes not found",
                },
            )
        session_id = f"{interview_id}--{interview_data.company_data.id}"
        print("\n\n\nsession_id", session_id, "\n\n\n")
        previous_messages = retrieve_dialogue(session_id)

        should_end_conversation = len(previous_messages) > 3
        if should_end_conversation:
            interview_data.status = InterviewStatus.completed
            set_interview(interview_data)
            company_attributes_scores = [
                attribute.company_score
                for attribute in company_attributes.company_attributes
            ]
            assessment_scores = get_conversation_assessment(
                previous_messages, company_attributes
            )
            company_attributes_scores = [
                attribute.company_score
                for attribute in company_attributes.company_attributes
            ]
            candidate_attributes_scores = [
                attribute.score for attribute in assessment_scores.assessment
            ]
            congruence_score = collaborative_filtering_similarity(
                company_attributes=company_attributes_scores,
                candidate_attributes=candidate_attributes_scores,
            )
            print("\n\n\nassessment_scores", assessment_scores, "\n\n\n")
            interview_data.assessment_results = assessment_scores
            interview_data.congruence_score = congruence_score
            update_company_interview(interview_data.company_data.id, interview_data)

        # print("\n\n\n NEW interview_dict", interview_data, "\n\n\n")
        prompt = get_interview_prompt(
            interview_data, company_attributes, should_end_conversation
        )
        # print("\n\n\nprompt", prompt, "\n\n\n")
        audio_stream = generate_audio_stream(
            prompt,
            transcribed_text,
            session_id,
        )

        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to process audio", "error": str(e)},
        )
