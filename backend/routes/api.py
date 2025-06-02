from flask import Blueprint, request, jsonify
from services.watson import analyze_text, assistant, ASSISTANT_ID, ask_watson

api_blueprint = Blueprint('api', __name__)

# Analyze document text with Watson NLU
@api_blueprint.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    result = analyze_text(text)
    return jsonify(result)

# Q&A using Watson Assistant
@api_blueprint.route('/qa', methods=['POST'])
def qa():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    # Create a new session for each request (production apps should manage sessions better)
    session = assistant.create_session(assistant_id=ASSISTANT_ID).get_result()
    session_id = session['session_id']
    response = ask_watson(question, session_id)
    # Extract answer text
    answer = ""
    if response['output'].get('generic'):
        answer = response['output']['generic'][0].get('text', '')
    # End session
    assistant.delete_session(assistant_id=ASSISTANT_ID, session_id=session_id)
    return jsonify({'answer': answer})
