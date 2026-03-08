from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import sqlite3
import os
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import ocr_scanner
import phishing_detector
import url_checker
import db_utils
import auth_utils
import chatbot_engine

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app) # Enable CORS for frontend interactions

# Ensure database and upload folders exist relative to the backend directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize SQLite database
db_utils.init_db()

# OAuth Placeholders
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'mock-google-client-id')
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', 'mock-github-client-id')

# Ensure upload directory exists
if os.environ.get('VERCEL'):
    UPLOAD_FOLDER = '/tmp/uploads'
else:
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to generate generic response structure
def format_response(analysis_result, extracted_text=None):
    response = {
        "risk_level": analysis_result["risk_level"],
        "trust_score": analysis_result["trust_score"],
        "confidence": analysis_result.get("confidence", 85), # Default confidence if not provided by module
        "reasons": analysis_result["reasons"],
        "safety_suggestions": analysis_result["safety_suggestions"],
        "detailed_explanation": analysis_result.get("detailed_explanation", "")
    }
    if extracted_text is not None:
        response["extracted_text"] = extracted_text
    
    # Pass along URL components for dynamic anatomy rendering if available
    if "url_components" in analysis_result:
        response["url_components"] = analysis_result["url_components"]
        
    return response

# --- Auth Endpoints ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'error': 'Missing fields'}), 400

    hashed_pw = generate_password_hash(password)

    conn = db_utils.get_db_connection()
    try:
        conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already exists'}), 409
    
    # Fetch new user to generate token
    user = conn.execute('SELECT id, name, email FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    token = auth_utils.generate_jwt(user['id'], user['email'], user['name'])
    return jsonify({'token': token, 'user': {'name': user['name'], 'email': user['email']}})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Missing fields'}), 400

    conn = db_utils.get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        token = auth_utils.generate_jwt(user['id'], user['email'], user['name'])
        return jsonify({'token': token, 'user': {'name': user['name'], 'email': user['email']}})
    
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    conn = db_utils.get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
    
    if user:
        reset_code = auth_utils.generate_reset_code()
        conn.execute('UPDATE users SET reset_code = ? WHERE id = ?', (reset_code, user['id']))
        conn.commit()
        # Mock or send real email based on environment
        auth_utils.send_reset_email(email, reset_code)

    conn.close()
    # Always return success to prevent email enumeration
    return jsonify({'message': 'If that email exists, a reset code has been sent.'})

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    new_password = data.get('new_password')

    if not all([email, code, new_password]):
        return jsonify({'error': 'Missing fields'}), 400

    conn = db_utils.get_db_connection()
    user = conn.execute('SELECT id, reset_code FROM users WHERE email = ?', (email,)).fetchone()

    if user and user['reset_code'] == code:
        hashed_pw = generate_password_hash(new_password)
        conn.execute('UPDATE users SET password = ?, reset_code = NULL WHERE id = ?', (hashed_pw, user['id']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Password successfully reset'})
    
    conn.close()
    return jsonify({'error': 'Invalid or expired reset code'}), 400

# --- OAuth Endpoints (Mocked for Demo) ---
@app.route('/api/auth/google', methods=['GET'])
def auth_google():
    return redirect(f"/api/auth/google/callback?mock_token=123")

@app.route('/api/auth/google/callback', methods=['GET'])
def auth_google_callback():
    # In real prod, you exchange code for token via Google API. Here we mock:
    mock_email = "google_user@gmail.com"
    mock_name = "Google User"
    
    conn = db_utils.get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (mock_email,)).fetchone()
    
    if not user:
        # Create user
        hashed_pw = generate_password_hash("oauth_no_password")
        conn.execute('INSERT INTO users (name, email, password, provider) VALUES (?, ?, ?, ?)', 
                     (mock_name, mock_email, hashed_pw, 'google'))
        conn.commit()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (mock_email,)).fetchone()
        
    token = auth_utils.generate_jwt(user['id'], user['email'], user['name'])
    conn.close()
    
    # Redirect to frontend with token in URL (simple hackathon approach)
    return redirect(f"/dashboard.html?token={token}&name={mock_name}")

@app.route('/api/auth/github', methods=['GET'])
def auth_github():
    return redirect(f"/api/auth/github/callback?mock_token=456")

@app.route('/api/auth/github/callback', methods=['GET'])
def auth_github_callback():
    mock_email = "github_user@github.com"
    mock_name = "GitHub User"
    
    conn = db_utils.get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (mock_email,)).fetchone()
    
    if not user:
        hashed_pw = generate_password_hash("oauth_no_password")
        conn.execute('INSERT INTO users (name, email, password, provider) VALUES (?, ?, ?, ?)', 
                     (mock_name, mock_email, hashed_pw, 'github'))
        conn.commit()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (mock_email,)).fetchone()
        
    token = auth_utils.generate_jwt(user['id'], user['email'], user['name'])
    conn.close()
    
    return redirect(f"/dashboard.html?token={token}&name={mock_name}")


# --- Scanner API Endpoints ---

@app.route('/api/scan-image', methods=['POST'])
def scan_image():
    # Attempt to extract user_id from optional Authorization header
    user_email = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_jwt(token)
        if isinstance(payload, dict):
            user_id = payload.get('sub')
            user_email = payload.get('email')

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        extracted_text = ocr_scanner.extract_text_from_image(file_path)
        analysis_result = phishing_detector.analyze_text(extracted_text)
        
        os.remove(file_path)
        
        response = format_response(analysis_result, extracted_text)
        
        # Save to history if logged in
        if user_email:
            conn = db_utils.get_db_connection()
            conn.execute('INSERT INTO scan_history (user_email, scan_type, content, risk_level, trust_score) VALUES (?, ?, ?, ?, ?)',
                         (user_email, 'Image', extracted_text[:200], response['risk_level'], response['trust_score']))
            conn.commit()
            conn.close()
            
            # Send Email Report natively
            if user_email:
                auth_utils.send_scan_report_email(
                    user_email, 
                    'Image (OCR)', 
                    response['risk_level'], 
                    response['trust_score'], 
                    response['reasons']
                )
            
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scan-text', methods=['POST'])
def scan_text():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
        
    user_email = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_jwt(token)
        if isinstance(payload, dict):
            user_id = payload.get('sub')
            user_email = payload.get('email')

    text = data['text']
    analysis_result = phishing_detector.analyze_text(text)
    response = format_response(analysis_result, text)
    
    if user_email:
        conn = db_utils.get_db_connection()
        conn.execute('INSERT INTO scan_history (user_email, scan_type, content, risk_level, trust_score) VALUES (?, ?, ?, ?, ?)',
                     (user_email, 'Text', text[:200], response['risk_level'], response['trust_score']))
        conn.commit()
        conn.close()
        
        # Send Email Report natively
        if user_email:
            auth_utils.send_scan_report_email(
                user_email, 
                'Text Content', 
                response['risk_level'], 
                response['trust_score'], 
                response['reasons']
            )
            
    return jsonify(response)

@app.route('/api/scan-url', methods=['POST'])
def scan_url():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'No url provided'}), 400
        
    user_email = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_jwt(token)
        if isinstance(payload, dict):
            user_id = payload.get('sub')
            user_email = payload.get('email')

    url = data['url']
    analysis_result = url_checker.analyze_url(url)
    response = format_response(analysis_result)
    
    if user_email:
        conn = db_utils.get_db_connection()
        conn.execute('INSERT INTO scan_history (user_email, scan_type, content, risk_level, trust_score) VALUES (?, ?, ?, ?, ?)',
                     (user_email, 'URL', url[:200], response['risk_level'], response['trust_score']))
        conn.commit()
        conn.close()
        
        # Send Email Report natively
        if user_email:
            auth_utils.send_scan_report_email(
                user_email, 
                'Suspicious Link', 
                response['risk_level'], 
                response['trust_score'], 
                response['reasons']
            )
        
    return jsonify(response)

# --- History & Dashboard Endpoints ---

@app.route('/api/history', methods=['GET'])
def get_user_history():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
        
    token = auth_header.split(' ')[1]
    payload = auth_utils.verify_jwt(token)
    if not isinstance(payload, dict):
        return jsonify({'error': payload}), 401
        
    user_id = payload.get('sub')
    user_email = payload.get('email')
    
    conn = db_utils.get_db_connection()
    # Get user score (using EMAIL)
    user = conn.execute('SELECT score FROM users WHERE email = ?', (user_email,)).fetchone()
    # Get recent history (using EMAIL)
    history = conn.execute('SELECT scan_type, content, risk_level, timestamp FROM scan_history WHERE user_email = ? ORDER BY timestamp DESC LIMIT 5', (user_email,)).fetchall()
    conn.close()
    
    return jsonify({
        'score': user['score'] if user else 0,
        'history': [dict(h) for h in history]
    })

# --- Chatbot Endpoint ---

@app.route('/api/chatbot', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    if not message:
        return jsonify({'reply': "I didn't catch that. Could you ask again?"})
        
    reply = chatbot_engine.get_chatbot_response(message)
    return jsonify({'reply': reply})

# --- Serve Frontend Files ---

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Run the server
    print("Starting Cyber Safety Platform API on http://localhost:5000")
    app.run(debug=True, port=5000)
