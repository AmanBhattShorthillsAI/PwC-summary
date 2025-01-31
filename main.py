import re
from pypdf import PdfReader
from helper import summary_structure
from langchain_text_splitters import TokenTextSplitter
import tiktoken
import time

# https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.azure.AzureChatOpenAI.html#Structured%20output

text = ""
reader = PdfReader("court_ruling/trumpVsUnitedState.pdf")

for page in reader.pages:
    text += page.extract_text() + "\n"

text = re.sub(r"\\u([0-9A-Fa-f]{4})", r"\1", text)
text = re.sub(r'\s+', ' ', text).strip()

def count_tokens(prompt: str, model: str = "gpt-4o-2024-08-06"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(prompt)
    token_count = len(tokens)
    return token_count




# -------word count---------    --
# words = text.split()
# print(len(words))






# print(text)







# # ---------------------------summary prompt------------------------------
# SUMMARY_PROMPT = f"""
# Court ruling: {text}
# --------------------
# Summarize this court ruling into the following sections:"
#                     1. Overall short summary
#                     2. Background
#                     3. Contention of taxpayer
#                     4. Contention of Revenue authorities
#                     5. Court verdict (with reasons)
#                 In the summary, capture all important references to the relevant legal provisions (example sections, sub-sections, rules). Also capture other important court rulings, circular, clarifications,  etc relied upon by the court to conclude on the issues involve.
#                 In the summary,  also capture any side issue addressed by the court,  or any other important principles laid down by the court to interpret law.
#                 It is fine if the output generated is a bit detailed.
#                 Avoid any extra commentary and directly give the answer.

#                 # Instructions:
#                 1. Refer strictly to the provided document for generating the response. Do not include any information or examples not explicitly mentioned in the document.
#                 2. If no relevant information is found in the text for a particular sub-section (e.g., Background), explicitly mention "N/A" for the field.

#                 # Formatting instructions:
#                 1. For the section-headings like - Overall short summary), strictly use '###' characters for formatting.
#                 2. Strictly use single-line spacing between section-heading (Overall short summary) and the generted output.
#                    Example: ### 1. Overall Short Summary
#                             summary information...........

#                 # Example:
#                 1. Overall short summary
#                     Summary Text (if available, else mention N/A)
#                 2. Background
#                     Background Information Text (if available, else mention N/A)
#                 3. Contention of taxpayer
#                     Contention Text (if available, else mention N/A)
#                 4. Contention of Revenue authorities
#                     Contention Text (if available, else mention N/A)
#                 5. Court verdict (with reasons)
#                     Verdict Text (if available, else mention N/A)"""



# SUMMARY_PROMPT = f"""


# Summarize this court ruling into the following sections:

# - overall_short_summary (str): Provide a concise yet detailed summary of the case, highlighting the main issues and decisions made by the court. Include only details explicitly mentioned in the document.
# - background (str): Provide the background of the case, detailing the events leading up to the case, the people involved (such as petitioners, respondents, appellants, etc.), and any relevant historical or procedural context.
# - contention_of_taxpayer (str): Summarize the arguments, disagreements, or claims made by the taxpayer, as explicitly mentioned in the document.
# - contention_of_revenue_authorities (str): Summarize the arguments, disagreements, or claims made by the revenue authorities, as explicitly mentioned in the document.
# - court_verdict (str): Provide a detailed description of the court's ruling, including any key legal provisions, sections, sub-sections, rules, important court rulings, circulars, clarifications, or precedents relied upon by the court. Capture all issues addressed by the court, side issues, or principles laid down to interpret the law.

# In the summary, capture all important references to the relevant legal provisions (example sections, sub-sections, rules). Also capture other important court rulings, circular, clarifications,  etc relied upon by the court to conclude on the issues involve.
# In the summary,  also capture any side issue addressed by the court,  or any other important principles laid down by the court to interpret law.
# It is fine if the output generated is a bit detailed.
# Avoid any extra commentary and directly give the answer.

# Instruction: 
# 1. Avoid introducing additional legal provisions, rulings, or clarifications that are not explicitly stated in the document. If a legal provision, case law, or ruling is mentioned, only include those directly cited in the document. If no such references are provided, use "N/A" in the respective field.
# 2. Do not give any extra text (like this ```json), and directly give the json output.
                                                        
                                                        
                                                        
# """


'''In the summary, capture all important references to the relevant legal provisions (example sections, sub-sections, rules). Also capture other important court rulings, circular, clarifications,  etc relied upon by the court to conclude on the issues involve.
In the summary,  also capture any side issue addressed by the court,  or any other important principles laid down by the court to interpret law.
It is fine if the output generated is a bit detailed.
Avoid any extra commentary and directly give the answer.'''




SUMMARY_PROMPT = f"""

This is the court ruling pdf text extracted from the file.\n

Court ruling text --> {text}

**
Summarize this court ruling into the following sections within json:

- overall_short_summary (str): Provide a concise yet detailed summary of the case, highlighting the main issues and decisions made by the court. Include only details explicitly mentioned in the document.
- background (str): Provide the background of the case, detailing the events leading up to the case, the people involved (such as petitioners, respondents, appellants, etc.), and any relevant historical or procedural context.
- contention_of_taxpayer (str): Summarize the arguments, disagreements, or claims made by the taxpayer, as explicitly mentioned in the document.
- contention_of_revenue_authorities (str): Summarize the arguments, disagreements, or claims made by the revenue authorities, as explicitly mentioned in the document.
- court_verdict (str): Provide a detailed description of the court's ruling, including any key legal provisions, sections, sub-sections, rules, important court rulings, circulars, clarifications, or precedents relied upon by the court. Capture all issues addressed by the court, side issues, or principles laid down to interpret the law.

- references - It is a dictionary which generates the references with indexes with following format for each reference, 
        case_<number> : 
            output_text: "<Generated Text> *clean this text if has multiple lines or next line or extra spaces, and also find this output_text inside the text provided above.*",
            reasoning: "<Explanation>",
            indexes: [
                "start_index": <the index where the output_text started>, "end_index": <the index where the output_text ended>
            ],
            sliced_output_text: extracted_court_ruling_text[start_index : end_index] - this is for proving that the index is correctly mentioning the output_text.

Instruction: 
1. Avoid introducing additional legal provisions, rulings, or clarifications that are not explicitly stated in the document. If a legal provision, case law, or ruling is mentioned, only include those directly cited in the document. If no such references are provided, use "N/A" in the respective field.
2. If there is no reference then give empty dictionary mentioning "No references found".
3. Do not give any extra text (like this ```json), and directly give the json output.  
4. The 'output_text' inside the reference section is the reference whose starting and ending index I want. Search for the index of this reference inside - this court ruling text.

"""




# SUMMARY_PROMPT = re.sub(r"\s+", " ", SUMMARY_PROMPT).encode().decode("unicode-escape").strip()


# prompt = text




# ----------------------------------Other information prompt------------------------------
# CASELAWSTUFFINFORMATION4O = f"""Case Law: {text}
#                 --------------------
#                 Read the provided case law and provide the detailed response on the following:
#                     1) Title of the Case: Provide the full title of the case.
#                     2) Citation of the Case: Provide the citation of the case.
#                     3) Court/ order issuing authority: Specify the court that heard the case or the authority that issued the order.
#                     4) Date of Order: Mention the date on which the decision was rendered.
#                     5) Previous Case details: Provide the details of the case against which the appeal was filed in this case.
#                         Do not include any cases that were merely referenced or cited for arguments. Include only if mentioned in the document
#                         Use the following format:
#                         - Case Name:
#                         - Citation:
#                         - Court/authority:
#                         - Date of judgment:
#                     6) Parties involved: List the names of all parties involved in the case. (Respondent, Appellant, Petitioner, and Appellee example)
#                     7) Name of taxpayer: List the names of the taxpayer(s) involved in the case.
#                     8) Counsel for taxpayer: List the names of counsel(s) involved in the case for taxpayer(s)
#                     9) Counsel for revenue: List the names of counsel(s) involved in the case for revenue
#                     10) Judge: Provide the full name of the judge who presided over the case.
#                     11) Case outcome: Whether court verdict was in the favor of “taxpayer” or “revenue authority” or “Both” or “None”
#                     12) Relevant Law: Identify the relevant laws or statutes that are applicable to the case.
#                     13) Amount in Dispute: Indicate the amount of money or value at stake in the dispute.<Any amount mentioned in the case linking to anyone mentioned explicity>
#                     14) Period relevant to dispute: Specify the period for dispute.
#                     15) Summarize all the issues considered by the court and the verdict of the court. Use the following format:
#                         - Issue <Number>: Briefly describe the issue.
#                         - Conclusion <Number> : Summarize the court's conclusion or verdict on the issue.
#                         - Outcome <Issue Number>: In favor of “Taxpayer” or “Revenue” or “Both” or “None”
#                     16) Summarize the important principles laid down by the court in this ruling. These principles may not necessarily relate to the main issue being discussed.

#                 # Instructions:
#                 1. Refer strictly to the provided document for generating the response. Do not include any information or examples not explicitly mentioned in the document.
#                 2. If no relevant information is found in the text for a particular sub-section (e.g., Background), explicitly mention "N/A" for the field.
#                 3. **If there is insufficient text, mention "N/A" against each field**.
               
#                 # Formatting Instructions:
#                 1. For the headings (like - Title of the Case), strictly use '**' characters for formatting.
#                 2. Strictly use single-line spacing between section-heading (Title of the Case) and the generted output.
#                    Example: **1. Title of the Case**
#                             Party A v/s Party B
 
#                 # Example:
#                     1. Title of the Case:
#                     Title text (If available, else mention N/A)
#                     2. Citation of the Case:
#                     Citation Text (If available, else mention N/A)
#                     3. Court/Order Issuing Authority:
#                     Court Name (If available, else mention N/A)
#                     ...
#                     ...
#                     16. Important Principles:
# #                     Principles Text (If avilable, else mention N/A)"""



# Provide the details of the case against which the appeal was filed in this case.







# (including a more detailed structure to accommodate specific roles 



CASELAWSTUFFINFORMATION4O = """


Read the provided case law and provide the detailed json response on the following:

-- title_of_case: Provide the full title of the case.
-- citation_of_case: Provide the citation of the case.
-- court_or_order_issuing_authority: Specify the court that heard the case or the authority that issued the order.
-- date_of_order: Mention the date on which the decision was rendered.
-- previous_case_details: Provide the list of previous cases in detailed format of the case against which the appeal was filed in this case.
    Do not include any cases that were merely referenced or cited for arguments. Include only if mentioned in the document
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

-- parties_involved: -- parties_involved: Provide a list of parties involved with the following structure:
    [{
        "appellants": [...], 
        "respondents": [...], 
        "petitioners": [...], 
        "appellees": [...]
    }]

    and if some of them is missing then use N/A inside list like this 
    ----
        [{
            "appellants": ["N/A"],                  **if this is not found**
            "respondents": ["N/A"],                 **if this is not found**
            "petitioners": ["N/A"],                 **if this is not found**
            "appellees": ["N/A"]                    **if this is not found**
        }]
    ----

-- names_of_taxpayer(list[str]): Provide the list of string of names of the taxpayers involved in the case. If there is no taxpayers then also provide a list of string mentioning "N/A"
-- counsels_for_taxpayer: Provide the list of string containing names of counsel involved in the case for taxpayers. If the output is null then also provide a list of string mentioning "N/A"
-- counsels_for_revenue: Provide the list of string containing names of counsel(s) involved in the case for revenue. If the output is null then also provide a list of string mentioning "N/A"
-- judge: Provide the list of full names of the judges who presided over the case.
-- case_outcome: Provide the outcome of the case; whether the court verdict was in the favor of “taxpayer” or “revenue authority”. Mention like "in favor of" <to whomever it is in favor>(<Name of authority>). If it is None then mention None simply.
-- relevant_law: Identify the relevant laws or statutes that are applicable to the case and provide a list of strings of it.
-- amount_in_dispute(str): Indicate the amount of money or value at stake in the dispute.<Any amount mentioned in the case linking to anyone mentioned explicity>
-- period_relevant_to_dispute: Specify the period of dispute.
-- summarize_issues_and_verdicts: Summarize all the issues considered by the court and the verdict of the court in the list format.
    Use the following format:
    -- if there is any issue present inside the file
    [
        {
            "issue_": **Briefly describe the issue**
            "issue_conclusion": **Summarize the court's conclusion or verdict on the issue**
            "issue_outcome": **In favor of “taxpayer” or “revenue” or “both” or “none”**
        }
    ]
    and if some of the issue present inside the file is not found then, 
    [
        {
            "issue_": "na",             **if this is not found**
            "issue_conclusion": "na",  **if this is not found**
            "issue_outcome": "na"      **if this is not found**
        }
    ]

-- important_principles: Summarize the important principles laid down by the court in this ruling inside al list of string. These principles may not necessarily relate to the main issue being discussed.

## Instructions:
1. Refer strictly to the provided document for generating the response. Do not include any information or examples not explicitly mentioned in the document.
2. If no relevant information is found in the text for a particular sub-section (e.g., Background), explicitly mention "N/A" for the field.
3. If there is insufficient text, mention "N/A" against each field.
4. Do not give any extra text (like this ```json), and directly give the json output.


            
"""





# --------------------- reference prompt-------------------------------------
REFERENCEINFORMATION = f"""Case Law: {text}
            ----------------------------------------------------------------------------------
            Read the provided case law and provide a detailed response in the following format:
 
            17) Case laws referred in this case by taxpayer, revenue authorities and court. (Case laws means external cases that have been referred. DO NOT mention references to Acts, sections as a separate entry or by yourself) Use below format:
                  There can be multiple references so include each of them carefully
                    - Case <Number>
                        - Case Name
                        - Case Citation
                        - Referred by taxpayer (with reasons)
                        - Referred by revenue authorities (with reasons)
                        - Referred by court (whether distinguished or relied upon with reasons)

            # Instructions:
            1. Refer strictly to the provided document for generating the response. Do not include any information or examples not explicitly mentioned in the document.
            2. If no relevant information is found for a particular sub-section (e.g., Case Name), explicitly mention "N/A" for the field.
            3. For the headings (like:- 17) Case laws referred in this case), strictly use '**' characters for formatting.
            4. Strictly use single-line spacing between section-heading (Case laws referred in this case) and the generated output.
            5. If no Case Laws are found, simply mention "No Case Laws were referred in the case"
            6. If the case is not referred by 'X', simply mention: "Not referred by X". 'X' can be Taxpayer, Revenue Authorities or Court.

            Example 1: (When Case Laws are found)
            17) Case laws referred in this case
                - Case <Number>
                    - Case Name: ABC
                    - Case Citation: DEF
                    - Referred by Taxpayer (with reasons): Not Referred by Taxpayer
                    - Referred by Revenue Authorities (with reasons): Relied upon with reasons PQR
                    - Referred by Court (whether distinguished or relied upon with reasons): Relied upon with reasons XYZ

            Example 2: (When Case Laws are found and case citation is nor found)
            17) Case laws referred in this case
                - Case <Number>
                    - Case Name: ABC
                    - Case Citation: N/A
                    - Referred by Taxpayer (with reasons): Relied upon with reasons XYZ
                    - Referred by Revenue Authorities (with reasons): Not Referred by Revenue Authorities
                    - Referred by Court (whether distinguished or relied upon with reasons): Relied upon with reasons PQR
 
            Example 3: (When Case Laws are not found)
            17) Case laws referred in this case
                - No Case Laws were referred in the case"""





REFERENCEINFORMATION = f"""



Read the provided case law and provide a detailed json response in the following format:

case_laws_referred_in_this_case(Case laws referred in this case by taxpayer, revenue authorities and court. (Case laws means external cases that have been referred.

This is the dictionaries of dictionaries of a class with these fields, 

for example..
""case_laws_referred_in_this_case"": 
    "case_1": 
        "case_name":"abc",
        "case_citation":"def",
        "referred_by_taxpayer":"ghi",
        "referred_by_revenue_authorities":"jkl ",
        "referred_by_court:"mno",
    "case_2": 
        "case_name":"pqr",
        "case_citation":"stu",
        "referred_by_taxpayer":"vwx",
        "referred_by_revenue_authorities":"yz ",
        "referred_by_court:"aabc",

Format:
case_<number>
    - case_name
    - case_citation
    - referred_by_taxpayer (with reasons) - references took by taxpayer
    - referred_by_revenue_authorities (with reasons) - references took by revenue authorities
    - referred_by_court (whether distinguished or relied upon with reasons) - references took by court

# Instructions:
1. Refer strictly to the provided document for generating the response. Do not include any information or examples not explicitly mentioned in the document.
2. If no relevant information is found for a particular sub-section (e.g., case_name), explicitly mention "N/A" for the field.
3. If no case laws are found, simply mention "No case laws were referred in the case."
4. If the case is not referred by 'X', simply mention: "Not referred by X". 'X' can be taxpayer, revenue authorities, or court.
5. Do not give any extra text (like this ```json), and directly give the json output.
6. DONOT mention by yourself anything outside of the case.



"""


# # ------ printing tokens for each prompt-------------w
# print("The number of tokens")
# tokens=count_tokens(prompt)
# print(tokens)
# print("------------------------------------------------------------------------------")
# # --------calculate cost-------------------------
# print("Cost for running this prompt in dollars")
# print(round(tokens * 0.0000025, 7))

# print("--------------------------Information------------------------------------------")



# -------- prompt word count-------
# words = prompt.split()
# print(len(words))




# text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_text(text=text)
# print(len(texts))


# start_time = time.time()
# summary_structure(SUMMARY_PROMPT)
# print("--- %s seconds ---" % (time.time() - start_time))

