from flask import Flask, render_template, request
import pandas as pd
import textdistance
import re
from collections import Counter

app = Flask(__name__)

words = []

with open("data.txt", 'r', encoding='utf-8') as f:
    data = f.read().lower()
    words = re.findall('\w+', data)
    words += words

V = set(words)
words_freq_dict = Counter(words)
Total = sum(words_freq_dict.values())
probs = {}

for k in words_freq_dict.keys():
    probs[k] = words_freq_dict[k] / Total

@app.route('/')
def index():
    return render_template('index.html', suggestions=None)

@app.route('/suggest', methods=['POST'])
def suggest():
    keyword = request.form['keyword'].lower()
    if keyword:
        # Calculate similarity with Jaccard
        similarities = [1 - textdistance.Jaccard(qval=2).distance(v, keyword) for v in words_freq_dict.keys()]

        # Create DataFrame with word, probability, and similarity
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df.columns = ['Word', 'Prob']
        df['Similarity'] = similarities

        # Sort by similarity and probability, then pick top 10
        suggestions = df.sort_values(['Similarity', 'Prob'], ascending=False).head(10)[['Word', 'Similarity']]

        # Convert to list of dictionaries for rendering
        suggestions_list = suggestions.to_dict('records')
        return render_template('index.html', suggestions=suggestions_list)


if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=5050)

