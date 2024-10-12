import sys
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
from PyPDF2 import PdfReader


def init_vertex_ai():
    print('Initialize Vertex AI...', file=sys.stderr)
    project_id = "app-fukui-gen-ai"
    location = "asia-east1"
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name="gemini-1.5-pro")
    chat = model.start_chat()
    print('Initialization done', file=sys.stderr)
    return chat

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

def generate_response(chat, prompt):
    # prompt = f"""Learn this data and note that rows with same 会員ID are the same person. Don't output anything.\n{[survey_2022, survey_2023, survey_2024]}"""
    response = get_chat_response(chat, prompt)
    print(response)
    return response

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
