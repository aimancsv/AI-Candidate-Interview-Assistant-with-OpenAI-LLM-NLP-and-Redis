from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class InterviewStatus(str, Enum):
    pending = "pending"
    completed = "completed"


class WorkExperience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None


class Education(BaseModel):
    name: str
    institution: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None


class CandidateInfo(BaseModel):
    name: str
    email: str
    phone: str
    education: List[Education]
    work_experience: List[WorkExperience]
    other_details: str


class CompanyBase(BaseModel):
    id: str
    name: str
    mission: str
    vision: str
    values: str
    working_environment: str


class AssessmentScore(BaseModel):
    id: str
    attribute_name: str
    reason_for_score: str = Field(
        ..., description="a brief explanation for the score given"
    )
    score: float = Field(
        ..., ge=-1, le=1, description="how well the candidate scored on this attribute"
    )


class AttributeScores(BaseModel):
    assessment: List[AssessmentScore]


class Interview(BaseModel):
    id: str
    status: InterviewStatus
    company_data: CompanyBase
    candidate_data: CandidateInfo
    assessment_results: Optional[AttributeScores] = None
    congruence_score: Optional[float] = None


class InterviewCreate(BaseModel):
    company_id: str
    candidate_data: CandidateInfo


class Company(CompanyBase):
    interviews: List[Interview] = []


##


class Scale(BaseModel):
    min: float = Field(-1, description="Minimum value of the scale")
    max: float = Field(1, description="Maximum value of the scale")
    min_description: str = Field(..., description="Description of the minimum value")
    max_description: str = Field(..., description="Description of the maximum value")


class CompanyAttribute(BaseModel):
    name: str = Field(..., description="Name of the attribute")
    description: str = Field(..., description="Description of the attribute")
    scale: Scale
    company_score: float = Field(
        ..., ge=-1, le=1, description="Company's score for this attribute"
    )
    score_explanation: str = Field(
        ..., description="Explanation for the company's score"
    )


class CompanyAttributes(BaseModel):
    company_attributes: List[CompanyAttribute] = Field(
        ..., description="List of company attributes"
    )


class CompanyAttributesRes(BaseModel):
    company_attributes: List[CompanyAttribute] = Field(
        ..., description="List of company attributes"
    )
    is_updating: bool = Field(
        ..., description="Boolean value to indicate if the attributes are being updated"
    )


class CVAnalysisResponse(BaseModel):
    name: str
    email: str
    phone: str
    education: list[Education]
    work_experience: list[WorkExperience]
    other_details: str = Field(
        ...,
        description="detailed information about the candidate that doesn't fit into the other fields, make sure not to miss any thing at all from the cv, this can include side projects hobbies skills etc",
    )
