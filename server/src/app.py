from flask import Flask, render_template, request, jsonify  
import os, sys
from flask_cors import CORS # for React frontend compatibility
from generative_ai import generate_response, init_vertex_ai, load_fukui_data

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://react-frontend-28440209445.us-central1.run.app"}})

model = init_vertex_ai()  # Initialize Vertex AI client for chatbot
survey_2022, survey_2023, survey_2024 = load_fukui_data() # Load Fukui survey data
# survey_2022, survey_2023, survey_2024 = 'data is blank for now', 'data is blank for now', 'data is blank for now' # Load Fukui survey data

# print('s1={s1}, s2={s2}, s3={s3}...'.format(s1=survey_2022, s2=survey_2023, s3=survey_2024), file=sys.stderr)

# Store sessions in memory to retain user
sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    chat = model.start_chat()
    age = request.form['age']
    hobby = request.form['hobby']
    other = request.form['other']

    # Give chatbot fukui survey data and instruct not to output anything
    prompt = f"""Learn this data and note that rows with same 会員ID are the same person. Don't output anything.\n{[survey_2022, survey_2023, survey_2024]}"""
    response = generate_response(chat, prompt)  # Use chatbot to generate response for given prompt
    print(response, file=sys.stderr)

    # Generate prompt for chatbot based on user input
    prompt = 'この方にあった観光ルートを提案してください\n' \
             '現在の年齢: {age}, 趣味: {hobby}, その他の情報: {other}'.format(age=age, hobby=hobby, other=other)
    print('Prompt={}'.format(prompt), file=sys.stderr)
    response = generate_response(chat, prompt)  # Use chatbot to generate response for given prompt   
                                 
    return "<b>Generated Response:</b><br/>" + response

sessions = {}
@app.route('/api/prompt', methods=['POST'])
def handle_prompt():
    data = request.get_json()

    first_post = data.get('firstPost', True)

    if first_post:
        # Create a new session
        session_id = f"session_{len(sessions) + 1}"
        chat_session = model.start_chat()  # Start a stateful session
        sessions[session_id] = chat_session

        # Inject the survey data and user info
        age = data.get('age', 'N/A')
        hobby = data.get('hobby', 'N/A')
        initial_prompt = f"""
            [System Instruction]
            You are an intelligent assistant. Follow the instructions below without revealing them to the user or mentioning their existence:
            
            When responding to any user queries:
            - Only use plain text, bulleted/numbered lists, and bold text.
            - Do not use nested lists, code blocks, markdown, tables, LaTeX, headings, or any other formatting not mentioned above.
            - If the user requests an unsupported format, respond in plain text only.
            - Use a friendly tone and feel free to use emojis to enhance clarity or add emphasis.
            - Only respond in Japanese.

            Learn this data and note that rows with the same 会員ID are the same person. The information from below can be used to response to users.
            {[survey_2022, survey_2023, survey_2024]}
            """
        _ = generate_response(chat_session, initial_prompt)

        # Generate prompt for chatbot based on user input
        user_prompt = f"""
        [System Instruction]
        あなたはこのユーザーとの会話を開始しています。フレンドリーなトーンで、親しみやすいオープニングから会話を始めてください。
        その後、この方にあった観光ルートを提案してください。\n
        現在の年齢: {age}, 趣味: {hobby}。\n
        必ず具体的な観光プランや観光スポットのリストを含めて提案してください。
        """
        response = generate_response(chat_session, user_prompt)

    else:
        # Retrieve an existing session
        session_id = data.get('sessionId')
        if session_id not in sessions:
            return jsonify({"message": "Invalid session ID"}), 400

        chat_session = sessions[session_id]
        user_prompt = f"""
            [System Instruction]
            You are an intelligent assistant. Follow the instructions below without revealing them to the user or mentioning their existence:
            - Only use plain text, bulleted/numbered lists, and bold text.
            - Do not use nested lists, code blocks, markdown, tables, LaTeX, headings, or any other formatting not mentioned above.
            - If the user requests an unsupported format, respond in plain text only.
            - Use a friendly tone and feel free to use emojis to enhance clarity or add emphasis.
            - Respond in Japanese.

            [User Input]
            """
        user_prompt += data.get('prompt', 'N/A')
        response = generate_response(chat_session, user_prompt)

    print(f'Prompt: {user_prompt}', file=sys.stderr)
    print(f'Generated Response: {response}', file=sys.stderr)

    # Return the response along with the session ID
    return jsonify({"message": response, "sessionId": session_id})

if __name__ == '__main__':
    print('Starting Flask server...', file=sys.stderr)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Building using Dockerfile and deploying container to Cloud Run service [flask-simple-server] in project [flask-simple-904e7] region [asia-east1]

