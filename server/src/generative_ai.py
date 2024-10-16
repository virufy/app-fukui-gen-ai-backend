import sys
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
from vertexai.generative_models._generative_models import ResponseValidationError
from PyPDF2 import PdfReader


def init_vertex_ai():
    print('Initialize Vertex AI...', file=sys.stderr)
    project_id = "app-fukui-gen-ai"
    location = "asia-east1"
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name="gemini-1.5-pro")
    # chat = model.start_chat()
    print('Initialization done', file=sys.stderr)
    return model

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

def generate_response(chat, prompt):
    try:
        response = get_chat_response(chat, prompt)
        print(response, file=sys.stderr)
        return response
    except ResponseValidationError as e:
        # Specific handling for validation errors
        print(f"Validation Error: {e}", file=sys.stderr)
        return "The response failed validation. Please try again with a different input."
    except Exception as e:
        # General exception handling for other issues
        print(f"Error during response generation: {e}", file=sys.stderr)
        return "There was an error generating the response. Please try again later."


def load_fukui_data():
    # with open('fukui_survey_2022_2024.pdf', 'rb') as file:
    #     reader = PdfReader(file)
    print('Loading Fukui data...1', file=sys.stderr)
    survey_2022 = pd.read_excel('data/20220428~0310 survey.xlsx')
    print('Loading Fukui data...2', file=sys.stderr)
    survey_2023 = pd.read_excel('data/20230428~0331 survey.xlsx')
    print('Loading Fukui data...3', file=sys.stderr)
    survey_2024 = pd.read_excel('data/20240401~0531 survey.xlsx')
    print('Loading done', file=sys.stderr)
    return survey_2022, survey_2023, survey_2024
