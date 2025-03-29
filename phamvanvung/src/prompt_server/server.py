from flask import Flask, request, jsonify
from prompt import process_prompt 
app = Flask(__name__)

@app.route('/process_prompt', methods=['POST'])
def handle_prompt():
    data = request.json
    text_input = data.get('prompt', '')
    if text_input.lower() == 'exit':
        return jsonify({"result": "exit"})
    result = process_prompt(text_input)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)