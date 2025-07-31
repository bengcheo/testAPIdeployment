from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import os
import tempfile
from werkzeug.utils import secure_filename
import base64
from datetime import datetime

app = Flask(__name__)

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def text_extractor(image_path):
    """Extract text from image using pytesseract"""
    try:
        # Open and process the image
        image = Image.open(image_path)

        # Extract text
        text = pytesseract.image_to_string(image)

        return {
            'success': True,
            'text': text.strip(),
            'message': 'Text extracted successfully'
        }
    except FileNotFoundError as e:
        return {
            'success': False,
            'text': '',
            'message': f'File not found: {str(e)}'
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
    <!DOCTYPE html>
    <html>
    <head>
        <title>📄 OCR Text Extractor</title>
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
            .upload-area {
                border: 2px dashed rgba(255,255,255,0.5);
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }
            .upload-area:hover {
                border-color: rgba(255,255,255,0.8);
                background: rgba(255,255,255,0.05);
            }
            .upload-area.dragover {
                border-color: #4CAF50;
                background: rgba(76, 175, 80, 0.1);
            }
            input[type="file"] {
                display: none;
            }
            .upload-btn {
                background: #ff6b6b;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
                margin: 10px;
            }
            .upload-btn:hover {
                background: #ff5252;
            }
            .process-btn {
                background: #4CAF50;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                margin-top: 15px;
                transition: background 0.3s;
            }
            .process-btn:hover {
                background: #45a049;
            }
            .process-btn:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            #result {
                margin-top: 20px;
                padding: 20px;
                border-radius: 8px;
                background: rgba(255,255,255,0.1);
                display: none;
            }
            .result-text {
                background: rgba(0,0,0,0.2);
                padding: 15px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                white-space: pre-wrap;
                max-height: 300px;
                overflow-y: auto;
            }
            .preview {
                max-width: 100%;
                max-height: 300px;
                border-radius: 8px;
                margin: 10px 0;
            }
            .loading {
                text-align: center;
                padding: 20px;
            }
            .spinner {
                border: 4px solid rgba(255,255,255,0.3);
                border-top: 4px solid white;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .copy-btn {
                background: #2196F3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 10px;
                font-size: 14px;
            }
            .copy-btn:hover {
                background: #1976D2;
            }
            .examples {
                font-size: 14px;
                opacity: 0.9;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 OCR Text Extractor</h1>

            <div class="card">
                <h2>Upload Image to Extract Text</h2>
                <div class="upload-area" id="upload-area">
                    <p>📁 Drag & drop your image here or click to select</p>
                    <button class="upload-btn" onclick="document.getElementById('file-input').click()">
                        Choose File
                    </button>
                    <input type="file" id="file-input" accept="image/*" onchange="handleFileSelect(event)">
                    <div class="examples">
                        <strong>Supported formats:</strong> PNG, JPG, JPEG, GIF, BMP, TIFF<br>
                        <strong>Max size:</strong> 16MB
                    </div>
                </div>

                <div id="preview-container" style="display: none;">
                    <h3>Preview:</h3>
                    <img id="preview" class="preview" alt="Preview">
                    <button class="process-btn" id="process-btn" onclick="extractText()">
                        🔍 Extract Text from Image
                    </button>
                </div>

                <div id="result"></div>
            </div>

            <div class="card">
                <h3>📡 API Usage</h3>
                <p><strong>POST /api/extract</strong> - Upload image and extract text</p>
                <pre style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; overflow-x: auto;">
curl -X POST -F "image=@your_image.jpg" /api/extract</pre>
            </div>
        </div>

        <script>
            let selectedFile = null;

            // Drag and drop functionality
            const uploadArea = document.getElementById('upload-area');

            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');

                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            });

            function handleFileSelect(event) {
                const file = event.target.files[0];
                if (file) {
                    handleFile(file);
                }
            }

            function handleFile(file) {
                selectedFile = file;

                // Show preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('preview');
                    preview.src = e.target.result;
                    document.getElementById('preview-container').style.display = 'block';
                };
                reader.readAsDataURL(file);
            }

            function extractText() {
                if (!selectedFile) {
                    alert('Please select an image first');
                    return;
                }

                const formData = new FormData();
                formData.append('image', selectedFile);

                const resultDiv = document.getElementById('result');
                const processBtn = document.getElementById('process-btn');

                // Show loading
                processBtn.disabled = true;
                processBtn.innerHTML = '⏳ Processing...';
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Extracting text from image...</div>';

                fetch('/api/extract', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    processBtn.disabled = false;
                    processBtn.innerHTML = '🔍 Extract Text from Image';

                    if (data.success) {
                        resultDiv.innerHTML = `
                            <h3>✅ Extracted Text:</h3>
                            <div class="result-text">${data.text || 'No text found in image'}</div>
                            <button class="copy-btn" onclick="copyText('${data.text.replace(/'/g, "\\'")}')">📋 Copy Text</button>
                        `;
                    } else {
                        resultDiv.innerHTML = `<h3>❌ Error:</h3><p>${data.message}</p>`;
                    }
                })
                .catch(error => {
                    processBtn.disabled = false;
                    processBtn.innerHTML = '🔍 Extract Text from Image';
                    resultDiv.innerHTML = '<h3>❌ Error:</h3><p>Failed to process image. Please try again.</p>';
                    console.error('Error:', error);
                });
            }

            function copyText(text) {
                navigator.clipboard.writeText(text).then(() => {
                    alert('Text copied to clipboard!');
                }).catch(() => {
                    alert('Failed to copy text');
                });
            }
        </script>
    </body>
    </html>
    '''


@app.route('/api/extract', methods=['POST'])
def extract_text():
    """API endpoint to extract text from uploaded image"""
    try:
        # Check if image was uploaded
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'text': '',
                'message': 'No image file provided'
            }), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({
                'success': False,
                'text': '',
                'message': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'text': '',
                'message': 'Invalid file type. Supported: PNG, JPG, JPEG, GIF, BMP, TIFF'
            }), 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        try:
            # Extract text using our function
            result = text_extractor(temp_path)

            # Add metadata
            result.update({
                'filename': filename,
                'timestamp': datetime.now().isoformat(),
                'file_size': os.path.getsize(temp_path)
            })

            return jsonify(result)

        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except Exception as e:
        return jsonify({
            'success': False,
            'text': '',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Test tesseract
        version = pytesseract.get_tesseract_version()
        return jsonify({
            'status': 'healthy',
            'tesseract_version': str(version),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


if __name__ == '__main__':
    import os

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)