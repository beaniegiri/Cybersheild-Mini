from flask import Flask, request, jsonify
from flask_cors import CORS
from text_sniffer import load_abusive_words, detect_abuse

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

# Load words once at startup
abusive_words = load_abusive_words("backend/abusive_words.txt")

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json.get('text', '')
    report = detect_abuse(text, abusive_words, similarity_threshold=0.6)
    
    return jsonify({
        'is_abusive': len(report['abusive_words']) > 0,
        'abusive_words': report['abusive_words'],
        'clean_text': report.get('clean_text', '')
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)