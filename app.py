from flask import Flask, render_template, request
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def summarize_text(text, model_name="finiteautomata/bertweet-base-sentiment-analysis"):
    summarization_pipeline = pipeline("sentiment-analysis", model=model_name)
    summarized_text = summarization_pipeline(inputs=text)
    label = summarized_text[0]['label']
    return label

def label_to_emoji(label,size):
    # Define a mapping between sentiment labels and emojis
    emoji_map = {
        'NEG': '😡',  # Negative sentiment
        'NEU': '😐',  # Neutral sentiment
        'POS': '😊',  # Positive sentiment
    }
    #return emoji_map.get(label, '❓')
    return emoji_map[label] * size   

@app.route('/')
def inputs():
    return render_template('inputs.html')

@app.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
        text = request.form.get("text")  # Get text from text box
        summary = summarize_text(text)
        size = 3
        emoji = label_to_emoji(summary,size)  
        return render_template("inputs.html", news=text, summary=emoji)
    return render_template("inputs.html")

if __name__ == "__main__":
    app.run(debug=True)