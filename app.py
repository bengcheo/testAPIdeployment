from flask import Flask, render_template, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# Collection of motivational quotes
QUOTES = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"text": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
    {"text": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon"},
    {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"text": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle"},
    {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins"},
    {"text": "In the end, we will remember not the words of our enemies, but the silence of our friends.",
     "author": "Martin Luther King Jr."},
    {"text": "The way to get started is to quit talking and begin doing.", "author": "Walt Disney"},
    {"text": "Don't let yesterday take up too much of today.", "author": "Will Rogers"},
    {"text": "You learn more from failure than from success. Don't let it stop you. Failure builds character.",
     "author": "Unknown"},
    {
        "text": "If you are working on something that you really care about, you don't have to be pushed. The vision pulls you.",
        "author": "Steve Jobs"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
     "author": "Winston Churchill"},
    {"text": "The only person you are destined to become is the person you decide to be.",
     "author": "Ralph Waldo Emerson"},
    {"text": "Your time is limited, so don't waste it living someone else's life.", "author": "Steve Jobs"},
    {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {
        "text": "The only thing standing between you and your goal is the story you keep telling yourself as to why you can't achieve it.",
        "author": "Jordan Belfort"},
    {"text": "Don't be afraid to give yourself everything you've ever wanted in life.", "author": "Unknown"},
    {"text": "If you want to live a happy life, tie it to a goal, not to people or things.",
     "author": "Albert Einstein"},
    {"text": "What lies behind us and what lies before us are tiny matters compared to what lies within us.",
     "author": "Ralph Waldo Emerson"},
    {"text": "The best time to plant a tree was 20 years ago. The second best time is now.",
     "author": "Chinese Proverb"},
    {"text": "Your limitation—it's only your imagination.", "author": "Unknown"},
    {"text": "Push yourself, because no one else is going to do it for you.", "author": "Unknown"},
    {"text": "Great things never come from comfort zones.", "author": "Unknown"},
    {"text": "Dream it. Wish it. Do it.", "author": "Unknown"},
    {"text": "Success doesn't just find you. You have to go out and get it.", "author": "Unknown"},
    {"text": "The harder you work for something, the greater you'll feel when you achieve it.", "author": "Unknown"},
    {"text": "Dream bigger. Do bigger.", "author": "Unknown"},
    {"text": "Don't stop when you're tired. Stop when you're done.", "author": "Unknown"},
    {"text": "Wake up with determination. Go to bed with satisfaction.", "author": "Unknown"},
    {"text": "Do something today that your future self will thank you for.", "author": "Sean Patrick Flanery"},
    {"text": "Little things make big days.", "author": "Unknown"},
    {"text": "It's going to be hard, but hard does not mean impossible.", "author": "Unknown"},
    {"text": "Don't wait for opportunity. Create it.", "author": "Unknown"},
    {"text": "Sometimes we're tested not to show our weaknesses, but to discover our strengths.", "author": "Unknown"},
    {"text": "The key to success is to focus on goals, not obstacles.", "author": "Unknown"},
    {"text": "Dream it. Believe it. Build it.", "author": "Unknown"}
]


def get_random_quote():
    """Get a random motivational quote"""
    return random.choice(QUOTES)


def get_daily_quote():
    """Get a consistent quote for today (same quote all day)"""
    # Use today's date as seed for consistent daily quote
    today = datetime.now().strftime('%Y-%m-%d')
    random.seed(today)
    quote = random.choice(QUOTES)
    random.seed()  # Reset seed
    return quote


@app.route('/')
def home():
    daily_quote = get_daily_quote()
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>💪 Daily Motivation</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Georgia', serif;
                background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                padding: 20px;
            }}

            @keyframes gradientShift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}

            .container {{
                max-width: 800px;
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 60px 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }}

            h1 {{
                font-size: 3em;
                margin-bottom: 40px;
                font-weight: 300;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }}

            .quote-container {{
                margin: 40px 0;
                padding: 40px 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                border-left: 5px solid rgba(255, 255, 255, 0.5);
                transition: transform 0.3s ease;
            }}

            .quote-container:hover {{
                transform: translateY(-5px);
            }}

            .quote-text {{
                font-size: 1.8em;
                line-height: 1.4;
                margin-bottom: 20px;
                font-style: italic;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }}

            .quote-author {{
                font-size: 1.2em;
                opacity: 0.9;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            .buttons {{
                margin-top: 40px;
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }}

            .btn {{
                padding: 15px 30px;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-size: 1.1em;
                font-weight: 600;
                border: 2px solid rgba(255, 255, 255, 0.3);
                transition: all 0.3s ease;
                cursor: pointer;
                display: inline-block;
            }}

            .btn:hover {{
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }}

            .btn-primary {{
                background: rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.5);
            }}

            .daily-label {{
                display: inline-block;
                background: rgba(255, 255, 255, 0.2);
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9em;
                margin-bottom: 20px;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }}

            .footer {{
                margin-top: 40px;
                opacity: 0.8;
                font-size: 0.9em;
            }}

            @media (max-width: 768px) {{
                .container {{ padding: 40px 20px; }}
                h1 {{ font-size: 2.2em; }}
                .quote-text {{ font-size: 1.4em; }}
                .buttons {{ flex-direction: column; align-items: center; }}
                .btn {{ width: 200px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💪 Daily Motivation</h1>

            <div class="daily-label">✨ Quote of the Day</div>

            <div class="quote-container" id="quote-container">
                <div class="quote-text" id="quote-text">"{daily_quote['text']}"</div>
                <div class="quote-author" id="quote-author">— {daily_quote['author']}</div>
            </div>

            <div class="buttons">
                <button class="btn btn-primary" onclick="getNewQuote()">🎲 Random Quote</button>
                <a href="/daily" class="btn">📅 Daily Quote</a>
                <a href="/api/quote" class="btn">🔗 API</a>
            </div>

            <div class="footer">
                <p>Start your day with inspiration • Share the motivation</p>
            </div>
        </div>

        <script>
            function getNewQuote() {{
                fetch('/api/random')
                .then(response => response.json())
                .then(quote => {{
                    document.getElementById('quote-text').innerHTML = `"${{quote.text}}"`;
                    document.getElementById('quote-author').innerHTML = `— ${{quote.author}}`;

                    // Add a little animation
                    const container = document.getElementById('quote-container');
                    container.style.opacity = '0.5';
                    container.style.transform = 'scale(0.95)';

                    setTimeout(() => {{
                        container.style.opacity = '1';
                        container.style.transform = 'scale(1)';
                    }}, 150);
                }})
                .catch(error => console.error('Error:', error));
            }}

            // Optional: Get new quote every 30 seconds
            // setInterval(getNewQuote, 30000);
        </script>
    </body>
    </html>
    '''


@app.route('/daily')
def daily():
    """Show the consistent daily quote"""
    return home()


@app.route('/api/quote')
def api_quote():
    """API endpoint that returns the daily quote"""
    return jsonify(get_daily_quote())


@app.route('/api/random')
def api_random():
    """API endpoint that returns a random quote"""
    return jsonify(get_random_quote())


@app.route('/api/all')
def api_all():
    """API endpoint that returns all quotes"""
    return jsonify(QUOTES)


if __name__ == '__main__':
    app.run(debug=True)