from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
# from openai import AzureOpenAI
import json
from typing import List, Dict

load_dotenv()

# class Summary(BaseModel):
#     overall_short_summary: str = Field(
#         description="A concise summary of the case that captures the main issues, decisions, and facts."
#     )
#     background: str = Field(
#         description="A detailed explanation of the case's background, including events leading to the case, involved individuals, and procedural context."
#     )
#     contention_of_taxpayer: str = Field(
#         description="A description of the taxpayer's arguments, disagreements, or claims made in the case."
#     )
#     contention_of_revenue_authorities: str = Field(
#         description="A description of the revenue authorities' arguments, disagreements, or claims made in the case."
#     )
#     court_verdict: str = Field(
#         description="A detailed explanation of the court's decision, including any rulings, legal provisions, precedents, and principles involved."
#     )



class Summary(BaseModel):
    overall_short_summary: str
    background: str
    contention_of_taxpayer: str
    contention_of_revenue_authorities: str
    court_verdict: str

# class PreviousCaseDetails(BaseModel):
#     case_name: str
#     citation: str
#     court_or_authority: str
#     date_of_judgment: str

# class OtherInformation(BaseModel):
#     title_of_case: str
#     citation_of_case: str
#     court_or_order_issuing_authority: str
#     date_of_order: str
#     previous_case_details: list[str]
#     parties_involved: list[str]
#     names_of_taxpayer: list[str]
#     counsels_for_taxpayer: list[str]
#     counsels_for_revenue: list[str]
#     judge: list[str]
#     case_outcome: str
#     relevant_law: list[str]
#     amount_in_dispute: str
#     period_relevant_to_dispute: str
#     summarize_issues_and_verdicts: list[str]
#     important_principles: list[str]

    
    
# class OtherInformation(BaseModel):
#     title_of_the_case: str
#     parties_involved: list[str]
#     court_or_issuing_authority: str
#     judges: list[str]
#     date: str
#     relevant_law: list[str]
#     amount_in_dispute: str
#     period_relevant_to_dispute: str
#     issues_summarization: list[str]
#     important_principles: list[str]
#     case_laws_referred_by_taxpayer: list[str]
#     case_laws_referred_by_revenue_authorities: list[str]
#     case_laws_referred_by_court: list[str]




class OtherInformation(BaseModel):
    title_of_case: str = Field(description="Provide the full title of the case.")
    citation_of_case: str = Field(description="Provide the citation of the case.")
    court_or_order_issuing_authority: str = Field(description="Specify the court that heard the case or the authority that issued the order.")
    date_of_order: str = Field(description="Mention the date on which the decision was rendered.")
    previous_case_details: List[Dict[str, str]] = Field(
        description=(
            "Provide the details of one or more cases against which the appeal was filed. "
            "Do not include merely referenced cases. Only include cases that are mentioned in the document."
            "Each dictionary should follow the format: "
            "{'case_name': '...', 'citation': '...', 'court_or_authority': '...', 'date_of_judgment': '...'}."
        )
    )
    parties_involved: Dict[str, List[str]] = Field(
        description=(
            "List all parties involved in the case, categorized by their roles. "
            "Format: {'Appellants': [...], 'Respondents': [...], 'Petitioners': [...], 'Appellees': [...]}."
        )
    )
    names_of_taxpayer: list[str] = Field(description="Provide the list of string containing names of the taxpayers involved in the case.")
    counsels_for_taxpayer: List[str] = Field(description="List the names of counsel(s) involved in the case for taxpayer(s).")
    counsels_for_revenue: List[str] = Field(description="List the names of counsel(s) involved in the case for revenue.")
    judge: str = Field(description="Provide the full name of the judge who presided over the case.")
    case_outcome: str = Field(description="Whether the court verdict was in favor of ‘taxpayer’, ‘revenue authority’, ‘both’, or ‘none.’")
    relevant_law: List[str] = Field(description="Identify the relevant laws or statutes that are applicable to the case.")
    amount_in_dispute: str = Field(description="Indicate the amount of money or value at stake in the dispute.")
    period_relevant_to_dispute: str = Field(description="Specify the period for dispute.")
    summarize_issues_and_verdicts: List[Dict[str, str]] = Field(
        description=(
            "Summarize all the issues considered by the court and the verdict of the court. "
            "Each dictionary should follow the format: "
            "{'issue_<Number>': 'Briefly describe the issue', 'issue_<Number>_conclusion': 'Summarize the court's conclusion or verdict on the issue', "
            "'issue_<Number>_outcome': 'In favor of taxpayer, revenue, both, or none'}."
        )
    )
    important_principles: List[str] = Field(
        description="Summarize the important principles laid down by the court in this ruling. These principles may not necessarily relate to the main issue being discussed."
    )

class CaseLawDetails(BaseModel):
    case_name: str
    case_citation: str
    referred_by_taxpayer: str
    referred_by_revenue_authorities: str
    referred_by_court: str

class ReferredCases(BaseModel):
    case_laws_referred_in_this_case: Dict[str, CaseLawDetails]

llm = AzureChatOpenAI(
    default_headers={"User-Id": os.getenv("AZURE_USER_ID")},
    temperature=0.0,
    azure_deployment=os.getenv('AZURE_DEPLOYMENT_NAME'),
    model=os.getenv('AZURE_MODEL_NAME'),
    timeout=100,
    api_version=os.getenv('AZURE_API_VERSION')
)

def summary_structure(prompt):
    pass

    # structured_output = llm.bind_tools([Summary])
    # print(structured_output.invoke(prompt).content)

    # structured_output = llm.bind_tools([OtherInformation])
    # print(structured_output.invoke(prompt).content)
    
    # structured_output = llm.bind_tools([CaseLawDetails])
    # print(structured_output.invoke(prompt))

    # structured_output = llm.with_structured_output(SimplifiedSummary, method='json_schema', include_raw=True)
    # print(structured_output.invoke(prompt)['raw'].content)

    # structured_output = llm.with_structured_output(OtherInformationSummary, method="function_calling", include_raw=True)
    # print(structured_output.invoke(prompt)['raw'].content)

    # print(llm.invoke(prompt).content)

