from flask import Flask, render_template, request
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string

app = Flask(__name__)

def summarize_text(text, no_sentences=3, format_type="paragraph"):
    if not text or not text.strip():
        return ""
    try:
        try:
            sentences = sent_tokenize(text)
        except LookupError:
            sentences = text.split('. ')
        if len(sentences) <= no_sentences:
            return text
        stop_words = set(stopwords.words('english') + list(string.punctuation))
        word_frequencies = {}
        for word in word_tokenize(text.lower()):
            if word not in stop_words:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1
        sentence_scores = {}
        for sent in sentences:
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]
        summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:no_sentences]
        if format_type == "bullets":
            summary = "\n• " + "\n• ".join(summarized_sentences)
        elif format_type == "numbered":
            summary = "\n".join(f"{i+1}. {sent}" for i, sent in enumerate(summarized_sentences))
        else:
            summary = ' '.join(summarized_sentences)
        return summary
    except Exception as e:
        print(f"Error in summarization: {str(e)}")
        return "Error: Could not generate summary. Please try with different text."

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ''
    input_text = ''
    no_sentences = 3
    format_type = 'paragraph'
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        no_sentences = int(request.form.get('no_sentences', 3))
        format_type = request.form.get('format_type', 'paragraph')
        if input_text:
            summary = summarize_text(input_text, no_sentences, format_type)
    return render_template('index.html', 
                          summary=summary, 
                          input_text=input_text,
                          no_sentences=no_sentences,
                          format_type=format_type)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
