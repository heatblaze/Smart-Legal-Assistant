from ibm_watson import NaturalLanguageUnderstandingV1, AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions, CategoriesOptions

# --- Watson NLU Setup ---
NLU_API_KEY = "your_nlu_api_key"
NLU_URL = "your_nlu_url"

nlu_authenticator = IAMAuthenticator(NLU_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=nlu_authenticator
)
nlu.set_service_url(NLU_URL)

def analyze_text(text):
    response = nlu.analyze(
        text=text,
        features=Features(
            keywords=KeywordsOptions(limit=10),
            entities=EntitiesOptions(limit=10),
            categories=CategoriesOptions(limit=3)
        )
    ).get_result()
    return response

# --- Watson Assistant Setup ---
ASSISTANT_API_KEY = "your_assistant_api_key"
ASSISTANT_URL = "your_assistant_url"
ASSISTANT_ID = "your_assistant_id"

assistant_authenticator = IAMAuthenticator(ASSISTANT_API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=assistant_authenticator
)
assistant.set_service_url(ASSISTANT_URL)

def ask_watson(question, session_id):
    response = assistant.message(
        assistant_id=ASSISTANT_ID,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': question
        }
    ).get_result()
    return response
