from typing import Tuple
from models import CompanyAttributes, Interview
from .prompt import interview_prompt


def format_interview_for_prompt(interview: Interview) -> Tuple[str, str]:
    company_details = f"""
Company Information:
Name: {interview.company_data.name}
Mission: {interview.company_data.mission}
Vision: {interview.company_data.vision}
Values: {interview.company_data.values}
Working Environment: {interview.company_data.working_environment}
"""

    candidate_details = f"""
Candidate Information:
Name: {interview.candidate_data.name}

Education:
"""
    for edu in interview.candidate_data.education:
        candidate_details += f"""
- Degree: {edu.name}
  Institution: {edu.institution}
  Start Date: {edu.start_date}
  End Date: {edu.end_date or 'Present'}
  Description: {edu.description or 'N/A'}
"""

    candidate_details += "\nWork Experience:"
    for exp in interview.candidate_data.work_experience:
        candidate_details += f"""
- Title: {exp.title}
  Company: {exp.company}
  Start Date: {exp.start_date}
  End Date: {exp.end_date or 'Present'}
  Description: {exp.description or 'N/A'}
"""

    candidate_details += f"\nOther Details:\n{interview.candidate_data.other_details}"

    return company_details, candidate_details


def format_company_attributes(company_attributes: CompanyAttributes) -> str:
    summary = "Company Attributes Summary:\n\n"

    for attr in company_attributes.company_attributes:
        summary += f"Attribute: {attr.name}\n"
        summary += f"Description: {attr.description}\n\n"

    return summary.strip()


def format_company_attributes_assessment(company_attributes: CompanyAttributes) -> str:
    summary = "Attributes:\n\n"

    for index, attr in enumerate(company_attributes.company_attributes):
        summary += f"id: {index}\n"
        summary += f"Attribute: {attr.name}\n"
        summary += f"Description: {attr.description}\n\n"

    return summary.strip()


def get_interview_prompt(
    interview_data: Interview,
    company_attributes: CompanyAttributes,
    should_end_conversation: bool,
) -> str:
    company_details, candidate_details = format_interview_for_prompt(interview_data)
    company_attributes_str = format_company_attributes(company_attributes)
    prompt = interview_prompt.format(
        company_name=interview_data.company_data.name,
        company_details=company_details,
        candidate_details=candidate_details,
        company_attributes=company_attributes_str,
        should_end_conversation=should_end_conversation,
    )

    return prompt
