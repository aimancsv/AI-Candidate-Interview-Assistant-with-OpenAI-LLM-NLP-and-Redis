import json
from congruent.call_llm.call_llm import call_llm
from models import CompanyAttributes, CompanyBase
from .prompt import values_encoder_prompt


def encode_company_values(company: CompanyBase) -> CompanyAttributes:
    try:
        prompt = values_encoder_prompt.format(
            company_mission=company.mission,
            company_vision=company.vision,
            company_values=company.values,
            company_working_environment=company.working_environment,
        )
        response = call_llm(
            prompt=prompt,
            chat_history=[],
            user_query="encode company values",
            model="gpt-4o",
        )
        if not response:
            raise Exception("No response from call_llm")
        response_dict = json.loads(response)
        company_attributes = CompanyAttributes(**response_dict)

        return company_attributes
    except Exception as e:
        print("Error in encode_company_values: ", e)
        raise e
