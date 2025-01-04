import json
from typing import List, Optional
from redis import Redis
from models import Company, CompanyAttributes, Interview

redis_client = Redis(host="localhost", port=6379, db=0)


def get_company(company_id: str) -> Optional[Company]:
    company_data = redis_client.get(f"company:{company_id}")
    return Company(**json.loads(company_data)) if company_data else None


def set_company(company: Company):
    redis_client.set(f"company:{company.id}", json.dumps(company.dict()))


def set_company_values(company_id: str, company_attributes: CompanyAttributes):
    redis_client.set(
        f"companyAttributes:{company_id}", json.dumps(company_attributes.dict())
    )


def set_attributes_updating(
    company_id: str, is_updating: bool
) -> Optional[CompanyAttributes]:
    redis_client.setex(
        f"isCompanyAttributesUpdating:{company_id}", 3600, f"{is_updating}"
    )


def get_attributes_updating(company_id: str) -> bool:
    res = redis_client.get(f"isCompanyAttributesUpdating:{company_id}")
    print("att res -->>", res == b"True")
    return res == b"True"


def get_company_values(company_id: str) -> Optional[CompanyAttributes]:
    company_attributes_data = redis_client.get(f"companyAttributes:{company_id}")
    return (
        CompanyAttributes(**json.loads(company_attributes_data))
        if company_attributes_data
        else None
    )


def update_company_interview(company_id: str, updated_interview: Interview):
    company = get_company(company_id)
    if not company:
        raise ValueError(f"Company with id {company_id} not found")

    interview_updated = False
    for i, interview in enumerate(company.interviews):
        if interview.id == updated_interview.id:
            company.interviews[i] = updated_interview
            interview_updated = True
            break

    if not interview_updated:
        raise ValueError(
            f"Interview with id {updated_interview.id} not found in company data"
        )

    set_company(company)
    return company


def delete_company(company_id: str):
    redis_client.delete(f"company:{company_id}")


def get_interview(interview_id: str) -> Optional[Interview]:
    interview_data = redis_client.get(f"interview:{interview_id}")
    return Interview(**json.loads(interview_data)) if interview_data else None


def set_interview(interview: Interview):
    redis_client.set(f"interview:{interview.id}", json.dumps(interview.dict()))


def delete_interview(interview_id: str):
    redis_client.delete(f"interview:{interview_id}")


def get_all_interviews(company_id: str) -> List[Interview]:
    company = get_company(company_id)
    if not company:
        return []
    interviews = company.interviews
    return interviews
