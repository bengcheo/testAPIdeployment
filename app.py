from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>✅ App is working!</h1><p>Railway deployment successful</p>"


@app.route('/test-ocr')
def test_ocr():
    try:
        import pytesseract
        from PIL import Image

        # Test tesseract version
        version = pytesseract.get_tesseract_version()
        return f"<h2>🎉 OCR Working!</h2><p>Tesseract version: {version}</p>"

    except ImportError as e:
        return f"<h2>❌ Import Error:</h2><p>{str(e)}</p>"
    except Exception as e:
        return f"<h2>⚠️ OCR Error:</h2><p>{str(e)}</p>"


@app.route('/health')
def health():
    return "OK"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)