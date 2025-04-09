from flask import Flask, request, render_template
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load model and tokenizer
model_dir = 'C:/Users/Binisa/OneDrive/Documents/Offensive-Model/model_save'

# C:\Users\Binisa\OneDrive\Documents\Offensive-Model
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertForSequenceClassification.from_pretrained(model_dir)

# Move model to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

app = Flask(__name__)

# Function for offensive language detection
def detect_offensive_language(input_text):
    inputs = tokenizer.encode_plus(
        input_text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    predictions = torch.argmax(outputs.logits, dim=1)

    return "Offensive language detected." if predictions.item() == 1 else "No offensive language detected."

# Route for home page
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        user_input = request.form["comment"]
        result = detect_offensive_language(user_input)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
