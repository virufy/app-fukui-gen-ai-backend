from flask import Flask, render_template, request, jsonify  
import os, sys
from flask_cors import CORS # for React frontend compatibility
from generative_ai import generate_response, init_vertex_ai, load_fukui_data

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

chat = init_vertex_ai()  # Initialize Vertex AI client for chatbot
survey_2022, survey_2023, survey_2024 = load_fukui_data() # Load Fukui survey data

# print('s1={s1}, s2={s2}, s3={s3}...'.format(s1=survey_2022, s2=survey_2023, s3=survey_2024), file=sys.stderr)

response = generate_response(chat, "Say a joke about GCP")
print(response, file=sys.stderr)

@app.route('/')
def index():
    # app.logger.info("Rendering index.html")
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    global chat
    age = request.form['age']
    hobby = request.form['hobby']

    # Give chatbot fukui survey data and instruct not to output anything
    prompt = f"""Learn this data and note that rows with same 会員ID are the same person. Don't output anything.\n{[survey_2022, survey_2023, survey_2024]}"""
    response = generate_response(chat, prompt)  # Use chatbot to generate response for given prompt
    print(response, file=sys.stderr)

    # Generate prompt for chatbot based on user input
    prompt = 'この方にあった観光ルートを提案してください\n' \
             '現在の年齢: {age}, 趣味: {hobby}'.format(age=age, hobby=hobby)
    print('Prompt={}'.format(prompt), file=sys.stderr)
    response = generate_response(chat, prompt)  # Use chatbot to generate response for given prompt   
                                 
    return "<b>Generated Response:</b><br/>" + response

@app.route('/api/prompt', methods=['POST'])
def handle_prompt():
    global chat
    data = request.get_json()  # Get the JSON data sent from the frontend
    age = data.get('age', 'N/A')
    hobby = data.get('hobby', 'N/A')

    # Give chatbot Fukui survey data and instruct it not to output anything
    prompt = f"""Learn this data and note that rows with the same 会員ID are the same person. Don't output anything.\n{[survey_2022, survey_2023, survey_2024]}"""
    _ = generate_response(chat, prompt)  # Load survey data into the chatbot

    # Generate prompt for chatbot based on user input (age and hobby)
    user_prompt = f'この方にあった観光ルートを提案してください\n' \
                  f'現在の年齢: {age}, 趣味: {hobby}'
    print('Prompt={}'.format(user_prompt), file=sys.stderr)

    # Get the response from the chatbot
    response = generate_response(chat, user_prompt)
    print('Generated Response: {}'.format(response), file=sys.stderr)

    # Return the chatbot response as JSON
    return jsonify({"message": response})

if __name__ == '__main__':
    print('Starting Flask server...', file=sys.stderr)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))



# Building using Dockerfile and deploying container to Cloud Run service [flask-simple-server] in project [flask-simple-904e7] region [asia-east1]

