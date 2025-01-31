import json
import re

from pydantic import ValidationError
from main import SUMMARY_PROMPT, CASELAWSTUFFINFORMATION4O, text, REFERENCEINFORMATION
from helper import llm, Summary, OtherInformation, ReferredCases
from prompt_toolkit import prompt

def get_payload(query):
    payload = json.dumps(
        {
            "max_tokens": 3000,
            "temperature": 0.0,
            "top_p": 1,
            "n": 1,
            "messages": [
                {
                    "role": "system", 
                    "content": SUMMARY_PROMPT
                }
            ],
        }
    )
    return payload


def get_payload_references(query):
    payload = json.dumps(
        {
            "max_tokens": 3000,
            "temperature": 0.0,
            "top_p": 1,
            "n": 1,
            "messages": [
                {"role": "system", "content": REFERENCEINFORMATION},
                {"role": "user", "content": f"{query}"},
            ],
        }
    )
    return payload


def get_payload_other_information(query):
    payload = json.dumps(
        {
            "max_tokens": 3000,
            "temperature": 0.0,
            "top_p": 1,
            "n": 1,
            "messages": [
                {"role": "system", "content": CASELAWSTUFFINFORMATION4O},
                {"role": "user", "content": f"{query}"},
            ],
        }
    )
    return payload


def json_resp(text):
    # print(text)
    # query = "Give a short summary about a dog"
    # print(query)

    messages = get_payload(text)

    # print(type(messages))

    # messages = re.sub(r"\s+", " ", messages).encode().decode("unicode-escape").strip()
    # print(messages)

    # print(messages)
    # messages = messages["messages"][1]['content']
    # print(type(messages))

    # llm = CustomAzureChatOpenAI(max_tokens=3000, temperature=0).llm

    # ai_message = llm(messages=messages, response_format=Summary)

    messages_other_info = get_payload_other_information(text)
    ai_message_other_info = llm(messages=messages_other_info, response_format=OtherInformation)

    # messages_references_info = get_payload_references(text)
    # ai_messages_references_info = llm(messages=messages_references_info, response_format=ReferredCases)

    # print("printing references information")
    # print(ai_messages_references_info.content)

    # print("printing other information")
    print(ai_message_other_info.content)

    # print("printing summary")
    # print(ai_message.content)

    # print(ai_message.content)
    # return ai_message.content, ai_message_other_info.content, ai_messages_references_info.content


json_resp(text=text)
