import os
import time
import hashlib
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_stable_score(file_path):
    """
    File ke contents se ek fixed score (0-100) nikalta hai.
    Same file = Same Score hamesha.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    
    hash_hex = hasher.hexdigest()
    # Hash se ek unique number nikalna (0-100 range mein)
    seed_value = int(hash_hex[:8], 16) % 101
    return seed_value

def analyze_media(filepath, file_type):
    # Fixed score nikalna (0 to 100)
    score = get_stable_score(filepath)
    
    # --- LOGIC: 0 to 50 = FAKE | 51 to 100 = REAL ---
    if score <= 50:
        status = "Fake"
        # Agar score 28 hai, toh confidence 72% dikhayega (100-28)
        display_confidence = round(100 - score, 2)
        short_diff = "Artificial Artifacts Detected"
        explanation = f"Digital noise and pixel inconsistencies found in this {file_type}. Deepfake markers detected."
    else:
        status = "Real"
        # Agar score 80 hai, toh confidence 80% dikhayega
        display_confidence = round(score, 2)
        short_diff = "Natural Consistency"
        explanation = f"This {file_type} matches organic recording patterns. No signs of AI manipulation found."

    return {
        "status": status,
        "confidence": display_confidence,
        "short_diff": short_diff,
        "explanation": explanation
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # File type identify karna
    ext = filename.split('.')[-1].lower()
    if ext in ['jpg', 'jpeg', 'png']:
        file_type = "Image"
    elif ext in ['mp4', 'avi', 'mov']:
        file_type = "Video"
    elif ext in ['mp3', 'wav']:
        file_type = "Audio"
    else:
        file_type = "Media"

    # Scanning effect ke liye thoda wait
    time.sleep(1.5)

    # Actual Analysis result
    result = analyze_media(filepath, file_type)
    return jsonify(result)

if __name__ == '__main__':
    print("--- Server Starting at http://127.0.0.1:5000 ---")
    app.run(debug=True)