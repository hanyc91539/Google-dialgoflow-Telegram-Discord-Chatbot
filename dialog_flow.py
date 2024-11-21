import os
import dialogflow 
from google.api_core.exceptions import InvalidArgument
from google.protobuf.json_format import MessageToJson
import uuid
import json

def dialog_flow(text_to_be_analyzed):
    DIALOGFLOW_PROJECT_ID = 'coin-exchangev-extension-d-lcks'

    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = str(uuid.uuid4())

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "coin-exchange-extension-d-lcks-58cf24687bc3.json"
    # Initialize the Dialogflow session client
    session_client = dialogflow.SessionsClient()

    # Define the session path
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)

    # Define the query input
    query_input = dialogflow.types.QueryInput(text=text_input)

    jsonData = {}
    # Detect intent
    tokenName = None
    intent = None
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        jsonData = json.loads(MessageToJson(response))
        tokenName = jsonData["queryResult"]["outputContexts"][0]["parameters"]["crypto_assets.original"]
        intent = jsonData["queryResult"]["intent"]["displayName"].replace("assetInfo.", "")
    except:
        pass
    return tokenName, intent
