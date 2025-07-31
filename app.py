from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def text_extractor(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return {
            'success': True,
            'text': text.strip(),
            'message': 'Text extracted successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'text': '',
            'message': f'Error: {str(e)}'
        }


@app.route('/')
def home():
    return '''
    <h1>📄 OCR Text Extractor</h1>
    <form action="/extract" method="POST" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required><br><br>
        <button type="submit">Extract Text</button>
    </form>
    <br>
    <a href="/test-ocr">Test OCR</a>
    '''


@app.route('/extract', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return "No image uploaded", 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return "Invalid file", 400

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        file.save(temp_file.name)
        result = text_extractor(temp_file.name)
        os.unlink(temp_file.name)  # Clean up

    if result['success']:
        return f"<h2>Extracted Text:</h2><pre>{result['text']}</pre><br><a href='/'>Try Another</a>"
    else:
        return f"<h2>Error:</h2><p>{result['message']}</p><br><a href='/'>Try Again</a>"


@app.route('/test-ocr')
def test_ocr():
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        return f"<h2>🎉 OCR Working!</h2><p>Tesseract version: {version}</p>"
    except Exception as e:
        return f"<h2>❌ OCR Error:</h2><p>{str(e)}</p>"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)