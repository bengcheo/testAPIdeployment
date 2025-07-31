from flask import Flask, request, jsonify, render_template
import re
import pickle
import os
from datetime import datetime

app = Flask(__name__)


# Simple sentiment analysis using keyword-based approach
# In a real app, you'd use scikit-learn, transformers, etc.

class SimpleSentimentAnalyzer:
    def __init__(self):
        # Positive and negative word lists
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'awesome', 'brilliant', 'perfect', 'outstanding', 'love', 'like',
            'happy', 'pleased', 'satisfied', 'delighted', 'thrilled', 'excited',
            'beautiful', 'nice', 'sweet', 'cool', 'best', 'incredible', 'superb'
        }

        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'dislike',
            'angry', 'frustrated', 'disappointed', 'sad', 'upset', 'annoyed',
            'worst', 'pathetic', 'useless', 'broken', 'failed', 'wrong', 'poor',
            'weak', 'slow', 'boring', 'stupid', 'ridiculous', 'waste'
        }

        self.model_version = "1.0"
        self.last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def preprocess_text(self, text):
        """Clean and prepare text for analysis"""
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        words = text.split()
        return words

    def predict(self, text):
        """Predict sentiment of text"""
        words = self.preprocess_text(text)

        positive_score = sum(1 for word in words if word in self.positive_words)
        negative_score = sum(1 for word in words if word in self.negative_words)

        # Calculate confidence based on word count
        total_sentiment_words = positive_score + negative_score
        confidence = min(0.9, total_sentiment_words / max(len(words), 1) + 0.1)

        if positive_score > negative_score:
            return {
                'sentiment': 'positive',
                'confidence': round(confidence, 2),
                'positive_score': positive_score,
                'negative_score': negative_score
            }
        elif negative_score > positive_score:
            return {
                'sentiment': 'negative',
                'confidence': round(confidence, 2),
                'positive_score': positive_score,
                'negative_score': negative_score
            }
        else:
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'positive_score': positive_score,
                'negative_score': negative_score
            }


# Initialize model
analyzer = SimpleSentimentAnalyzer()


@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Sentiment Analysis ML API</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: white;
            }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { text-align: center; margin-bottom: 30px; font-size: 2.5em; }
            .card { 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px; 
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; font-weight: 600; }
            textarea { 
                width: 100%; 
                padding: 15px; 
                border: none; 
                border-radius: 8px; 
                font-size: 16px;
                resize: vertical;
                min-height: 120px;
            }
            button { 
                background: #ff6b6b; 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 8px; 
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                transition: background 0.3s;
            }
            button:hover { background: #ff5252; }
            #result { 
                margin-top: 20px; 
                padding: 20px; 
                border-radius: 8px;
                display: none;
            }
            .positive { background: rgba(76, 175, 80, 0.3); }
            .negative { background: rgba(244, 67, 54, 0.3); }
            .neutral { background: rgba(158, 158, 158, 0.3); }
            .examples { margin-top: 20px; }
            .example-btn { 
                display: inline-block; 
                margin: 5px; 
                padding: 8px 15px; 
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                color: white; 
                text-decoration: none; 
                border-radius: 20px; 
                font-size: 14px;
                cursor: pointer;
            }
            .api-info { 
                font-size: 14px; 
                opacity: 0.9; 
                margin-top: 20px; 
                padding: 15px;
                background: rgba(0,0,0,0.2);
                border-radius: 8px;
            }
            .model-info {
                text-align: center;
                opacity: 0.8;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Sentiment Analysis ML API</h1>

            <div class="model-info">
                <p>Model Version: ''' + analyzer.model_version + ''' | Last Updated: ''' + analyzer.last_updated + '''</p>
            </div>

            <div class="card">
                <h2>Analyze Text Sentiment</h2>
                <form id="sentiment-form">
                    <div class="form-group">
                        <label for="text">Enter text to analyze:</label>
                        <textarea id="text" name="text" placeholder="Type or paste your text here..." required></textarea>
                    </div>
                    <button type="submit">🔍 Analyze Sentiment</button>
                </form>

                <div class="examples">
                    <strong>Try these examples:</strong><br>
                    <span class="example-btn" onclick="setText('I love this product! It works amazingly well.')">Positive Example</span>
                    <span class="example-btn" onclick="setText('This is terrible. I hate it and want my money back.')">Negative Example</span>
                    <span class="example-btn" onclick="setText('The weather is okay today.')">Neutral Example</span>
                </div>

                <div id="result"></div>
            </div>

            <div class="card api-info">
                <h3>📡 API Endpoints</h3>
                <p><strong>POST /api/predict</strong> - Analyze sentiment</p>
                <p><strong>GET /api/health</strong> - Check API status</p>
                <p><strong>GET /api/model-info</strong> - Get model information</p>
                <br>
                <p><strong>Example:</strong></p>
                <code>curl -X POST -H "Content-Type: application/json" -d '{"text":"I love this!"}' /api/predict</code>
            </div>
        </div>

        <script>
            function setText(text) {
                document.getElementById('text').value = text;
            }

            document.getElementById('sentiment-form').addEventListener('submit', function(e) {
                e.preventDefault();

                const text = document.getElementById('text').value;
                const resultDiv = document.getElementById('result');

                // Show loading
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<p>🤔 Analyzing sentiment...</p>';

                fetch('/api/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({text: text})
                })
                .then(response => response.json())
                .then(data => {
                    const sentiment = data.sentiment;
                    const confidence = data.confidence;
                    const emoji = sentiment === 'positive' ? '😊' : sentiment === 'negative' ? '😞' : '😐';

                    resultDiv.className = sentiment;
                    resultDiv.innerHTML = `
                        <h3>${emoji} Sentiment: ${sentiment.toUpperCase()}</h3>
                        <p><strong>Confidence:</strong> ${(confidence * 100).toFixed(1)}%</p>
                        <p><strong>Positive words found:</strong> ${data.positive_score}</p>
                        <p><strong>Negative words found:</strong> ${data.negative_score}</p>
                    `;
                })
                .catch(error => {
                    resultDiv.innerHTML = '<p>❌ Error analyzing sentiment. Please try again.</p>';
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>
    '''


@app.route('/api/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({'error': 'Please provide text field'}), 400

        text = data['text']
        if not text or not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400

        # Get prediction
        result = analyzer.predict(text)

        # Add metadata
        result.update({
            'text': text,
            'model_version': analyzer.model_version,
            'timestamp': datetime.now().isoformat(),
            'processing_time_ms': 1  # Placeholder for actual timing
        })

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint for CI/CD monitoring"""
    return jsonify({
        'status': 'healthy',
        'model_version': analyzer.model_version,
        'timestamp': datetime.now().isoformat(),
        'uptime': 'running'
    })


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        'model_name': 'Simple Sentiment Analyzer',
        'version': analyzer.model_version,
        'last_updated': analyzer.last_updated,
        'model_type': 'keyword-based',
        'supported_languages': ['english'],
        'categories': ['positive', 'negative', 'neutral']
    })


@app.route('/api/batch', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint"""
    try:
        data = request.get_json()

        if not data or 'texts' not in data:
            return jsonify({'error': 'Please provide texts field as array'}), 400

        texts = data['texts']
        if not isinstance(texts, list):
            return jsonify({'error': 'texts must be an array'}), 400

        if len(texts) > 100:  # Limit batch size
            return jsonify({'error': 'Maximum 100 texts per batch'}), 400

        results = []
        for i, text in enumerate(texts):
            if text and text.strip():
                result = analyzer.predict(text)
                result['text'] = text
                result['index'] = i
                results.append(result)

        return jsonify({
            'results': results,
            'batch_size': len(results),
            'model_version': analyzer.model_version,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)