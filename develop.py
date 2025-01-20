import json

from pydantic import ValidationError
from main import SUMMARY_PROMPT, CASELAWSTUFFINFORMATION4O, text, REFERENCEINFORMATION
from helper import llm, Summary, OtherInformation, ReferredCases

def get_payload(query):        
    payload = json.dumps({
        "max_tokens": 3000,
        "temperature": 0.0,
        "top_p": 1,
        "n": 1,
        "messages": [{
                        "role":"system",
                        "content":SUMMARY_PROMPT
                    },
                    {
                        "role":"user",
                        "content":f"{query}"
                    }
                ]
            })
    return payload

def get_payload_references(query):        
    payload = json.dumps({
        "max_tokens": 3000,
        "temperature": 0.0,
        "top_p": 1,
        "n": 1,
        "messages": [{
                        "role":"system",
                        "content":REFERENCEINFORMATION
                    },
                    {
                        "role":"user",
                        "content":f"{query}"
                    }
                ]
            })
    return payload

def get_payload_other_information(query):        
    payload = json.dumps({
        "max_tokens": 3000,
        "temperature": 0.0,
        "top_p": 1,
        "n": 1,
        "messages": [{
                        "role":"system",
                        "content":CASELAWSTUFFINFORMATION4O
                    },
                    {
                        "role":"user",
                        "content":f"{query}"
                    }
                ]
            })
    return payload


# class CustomAzureChatOpenAI():
#     def __init__(self,max_tokens,temperature):
#         # Retrieve user ID and password from environment variables
#         load_dotenv()
#         self.max_tokens = max_tokens
#         self.temperature = temperature
#         self.pwc_guid=os.getenv("USERNAME")
#         self.pwc_pass=os.getenv("PASSWORD")
#         self.pwc_apikey=os.getenv("API_KEY")
#         self.pwc_api_version=os.getenv("API_VERSION")
#         # self.llm = PwCAzureChatOpenAI(
#         #         guid=self.pwc_guid,
#         #         password=self.pwc_pass,
#         #         apikey=self.pwc_apikey,
#         #         mode='sync',
#         #         api_version=self.pwc_api_version,
#         #         model="gpt-4o",
#         #         max_tokens = self.max_tokens,
#         #         temperature = self.temperature
#         # )
#         self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
#         self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
#         self.llm = AzureChatOpenAI(
#               deployment_name="azure.gpt-4o",
#               api_version=self.api_version,
#               temperature=self.temperature
#         )

def json_resp(text):
    print(text)
    print
    # query = "Give a short summary about a dog"
    # print(query)

    messages = get_payload(text)
    # llm = CustomAzureChatOpenAI(max_tokens=3000, temperature=0).llm

    ai_message = llm(messages=messages, response_format=Summary)

    messages_other_info = get_payload_other_information(text)
    ai_message_other_info = llm(messages=messages_other_info, response_format=OtherInformation)

    messages_references_info = get_payload_references(text)
    ai_messages_references_info = llm(messages=messages_references_info, response_format=ReferredCases)
    
    # print("printing references information")
    # print(ai_messages_references_info.content)


    # print("printing other information")
    # print(ai_message_other_info.content)
    
    # print("printing summary")
    # print(ai_message.content)

    return ai_message.content, ai_message_other_info.content, ai_messages_references_info.content
