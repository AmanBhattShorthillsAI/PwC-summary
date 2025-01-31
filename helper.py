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


class Reference(BaseModel):
    output_text: str
    reasoning: str
    indexes: list
    sliced_output_text: str


class Summary(BaseModel):
    overall_short_summary: str
    background: str
    contention_of_taxpayer: str
    contention_of_revenue_authorities: str
    court_verdict: str
    references: Dict[str, Reference]


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


class PreviousCaseDetails(BaseModel):
    case_name: str
    citation: str
    court_or_authority: str
    date_of_judgement: str


class PartiesInvolved(BaseModel):
    appellants: List[str]
    respondents: List[str]
    petitioners: List[str]
    appellees: List[str]


class SummarizeIssueAndVerdicts(BaseModel):
    issue_: str = Field(description="This is issue number with format issue_<number>")
    issue_conclusion: str
    issue_outcome: str


class OtherInformation(BaseModel):
    title_of_case: str = Field(description="Provide the full title of the case.")
    citation_of_case: str = Field(description="Provide the citation of the case.")
    court_or_order_issuing_authority: str = Field(
        description="Specify the court that heard the case or the authority that issued the order."
    )
    date_of_order: str = Field(
        description="Mention the date on which the decision was rendered."
    )
    previous_case_details: List[PreviousCaseDetails] = Field(
        description=(
            """ 
                Provide the details of one or more cases against which the appeal was filed. 
                Do not include merely referenced cases. Only include cases that are mentioned in the document.
                    Use the following format if you found any relevant details.
                    {
                        "case_name": "abc", 
                        "citation": "def", 
                        "court_or_authority": "ghi", 
                        "date_of_judgement": "jkl"
                    }
                        and if some of them is missing then use N/A inside list like this
                    {
                        "case_name": "N/A",                     **if this is not found**
                        "citation": "N/A",                      **if this is not found**
                        "court_or_authority": "N/A",            **if this is not found**
                        "date_of_judgement": "N/A"               **if this is not found**
                    }
            """
        )
    )
    parties_involved: List[PartiesInvolved] = Field(
        description=(
            """
                List all parties involved in the case, categorized by their roles. 
                Format: 
                {
                    'Appellants': [...], 
                    'Respondents': [...], 
                    'Petitioners': [...], 
                    'Appellees': [...]
                }.
            """
        )
    )
    names_of_taxpayer: List[str] = Field(
        description="Provide the list of string containing names of the taxpayers involved in the case."
    )
    counsels_for_taxpayer: List[str] = Field(
        description="List the names of counsel(s) involved in the case for taxpayer(s)."
    )
    counsels_for_revenue: List[str] = Field(
        description="List the names of counsel(s) involved in the case for revenue."
    )
    judge: List[str] = Field(
        description="Provide the full name of the judge who presided over the case."
    )
    case_outcome: str = Field(
        description="Whether the court verdict was in favor of ‘taxpayer’, ‘revenue authority’, ‘both’, or ‘none.’"
    )
    relevant_law: List[str] = Field(
        description="Identify the relevant laws or statutes that are applicable to the case."
    )
    amount_in_dispute: str = Field(
        description="Indicate the amount of money or value at stake in the dispute."
    )
    period_relevant_to_dispute: str = Field(
        description="Specify the period for dispute."
    )
    summarize_issues_and_verdicts: List[SummarizeIssueAndVerdicts] = Field(
        description=(
            """
            
                Summarize all the issues considered by the court and the verdict of the court in the list format.
                Use the following format:
                -- if there is any issue present inside the file
                [
                    {
                        "issue_number": **Briefly describe the issue**
                        "issue_number_conclusion": **Summarize the court's conclusion or verdict on the issue**
                        "issue_number_outcome": **In favor of “taxpayer” or “revenue” or “both” or “none”**
                    }
                ]
                and if some of the issue present inside the file is not found then, 
                [
                    {
                        "issue_number": "na",             **if this is not found**
                        "issue_number_conclusion": "na",  **if this is not found**
                        "issue_number_outcome": "na"      **if this is not found**
                    }
                ]
                
            """
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


class CustomAzureChatOpenAI:
    def __init__(self, max_tokens, temperature):
        # Retrieve user ID and password from environment variables
        load_dotenv()
        # self.max_tokens = max_tokens
        # self.temperature = temperature
        # self.pwc_guid=os.getenv("USERNAME")
        # self.pwc_pass=os.getenv("PASSWORD")
        # self.pwc_apikey=os.getenv("API_KEY")
        # self.pwc_api_version=os.getenv("AZURE_API_VERSION")
        # self.llm = PwCAzureChatOpenAI(
        #         guid=self.pwc_guid,
        #         password=self.pwc_pass,
        #         apikey=self.pwc_apikey,
        #         mode='sync',
        #         api_version=self.pwc_api_version,
        #         model="gpt-4o",
        #         max_tokens = self.max_tokens,
        #         temperature = self.temperature
        # )
        self.api_version = os.getenv("AZURE_API_VERSION")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")

        self.llm = AzureChatOpenAI(
            default_headers={"User-Id": os.getenv("AZURE_USER_ID")},
            temperature=temperature,
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            model=os.getenv("AZURE_MODEL_NAME"),
            timeout=100,
            api_version=os.getenv("AZURE_API_VERSION"),
            max_tokens=max_tokens,
        )


llm = CustomAzureChatOpenAI(3000, 0.0).llm


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
