from typing import List
from fastapi import APIRouter, BackgroundTasks, HTTPException
from congruent.ValueEncoder.ValuesEncoder import encode_company_values
from models import (
    Company,
    CompanyAttributes,
    CompanyAttributesRes,
    CompanyBase,
    Interview,
)
from database import (
    get_all_interviews,
    get_attributes_updating,
    get_company,
    get_company_values,
    set_attributes_updating,
    set_company,
    delete_company,
    set_company_values,
)

router = APIRouter()


def encode_and_set_company_values(company_data: Company):
    set_attributes_updating(company_data.id, True)
    encoded_values = encode_company_values(company_data)
    set_company_values(company_data.id, encoded_values)
    set_attributes_updating(company_data.id, False)


@router.post("/companies", response_model=Company)
async def create_company(company: CompanyBase, background_tasks: BackgroundTasks):
    company_data = Company(**company.dict(), interviews=[])
    set_company(company_data)
    background_tasks.add_task(encode_and_set_company_values, company_data)

    return {"company_data": company_data}


@router.get("/companies/{company_id}", response_model=Company)
async def read_company(company_id: str):
    company = get_company(company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/companies/{company_id}", response_model=Company)
async def update_company(
    company_id: str, company: CompanyBase, background_tasks: BackgroundTasks
):
    existing_company = get_company(company_id)
    if not existing_company:
        raise HTTPException(status_code=404, detail="Company not found")
    updated_company = Company(**company.dict(), interviews=existing_company.interviews)
    set_company(updated_company)
    background_tasks.add_task(encode_and_set_company_values, updated_company)
    return updated_company


@router.get("/companies/{company_id}/attributes", response_model=CompanyAttributesRes)
async def get_attributes(company_id: str):
    company_attributes = get_company_values(company_id)
    is_updating = get_attributes_updating(company_id)

    if not company_attributes and not is_updating:
        raise HTTPException(status_code=404, detail="Company attributes not found")
    if not company_attributes and is_updating:
        return CompanyAttributesRes(company_attributes=[], is_updating=is_updating)
    if not company_attributes:
        raise HTTPException(status_code=404, detail="Company attributes not found")
    return CompanyAttributesRes(
        company_attributes=company_attributes.company_attributes,
        is_updating=is_updating,
    )


@router.delete("/companies/{company_id}")
async def delete_company_route(company_id: str):
    if not get_company(company_id):
        raise HTTPException(status_code=404, detail="Company not found")
    delete_company(company_id)
    return {"message": "Company deleted successfully"}


@router.get("/companies/{company_id}/interviews", response_model=List[Interview])
async def get_company_interviews(company_id: str):
    all_interviews = get_all_interviews(company_id)
    return all_interviews
