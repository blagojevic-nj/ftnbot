from flask import Flask, request, jsonify
from flask_cors import CORS
from models import ResponseDTO, ResultDTO
from typing import List
from openai import OpenAI
from database_adapter import DatabaseAdapter

OPENAI_API_KEY = "sk-proj-TDhM0Ll4r46iqiLMuPUAT3BlbkFJ1a4n3r0yAAyQHMuX6l9f"

app = Flask(__name__)
CORS(app)

da = DatabaseAdapter()
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_answer(question: str, contexts: List[str]) -> str:
    content = f'Na osnovu konteksta odgovori na pitanje. Pitanje: {question}. Kontekst: {"|".join(contexts)}'
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )

    return chat_completion.choices[0].message.content

def generate_response(question: str, context) -> ResponseDTO:
    contexts = [con['metadata']['context'] for con in context]
    answer = generate_answer(question, contexts)
    return ResponseDTO(question, answer, contexts)

@app.route('/get-response', methods=['POST'])
def get_response():
    question = request.json.get('user_message')
    context = da.query_database(question, top_k=3)
    print(context)
    return jsonify(generate_response(question, context['matches']))

@app.route('/admin/context', methods=['GET'])
def query_database():
    query = request.args.get('query')
    context = da.query_database(query, top_k=10)
    responses = [ResultDTO(match['id'], match['metadata']['context'], format(match['score'], '.2f')) for match in context['matches']]

    return jsonify(responses)

@app.route('/admin/context', methods=['POST'])
def add_context():
    query = request.json.get('query')
    da.add_context(query)
    context = da.query_database(query, top_k=10)
    responses = [ResultDTO(match['id'], match['metadata']['context'], format(match['score'], '.2f')) for match in context['matches']]

    return jsonify(responses)

@app.route('/admin/context', methods=['PUT'])
def update_context():
    da.update_context(request.json)
    return "", 204

@app.route('/admin/context', methods=['DELETE'])
def delete_context():
    context_id = request.args.get('id')
    da.delete_context(context_id)
    return "", 204

if __name__ == '__main__':
    app.run(debug=False)
