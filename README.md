# Cyber Safety Platform

This is a full-stack web application designed to help users identify and prevent online scams, harassment, and social engineering attacks. 

## What Was Done

We developed a comprehensive web platform consisting of a Python (Flask) backend and a responsive HTML/CSS/JS frontend. Key technical implementations include:
- **Authentication & Dashboard**: Built a secure login/registration system with JWT (JSON Web Tokens) to track user reports and past scans, saved efficiently in a local SQLite database.
- **Multimodal Scanning Features**:
  - **URL Scanner**: Added logic to verify the trustworthiness of domains based on a scoring algorithm.
  - **Text Scanner**: Implemented text analysis to detect phishing keywords or abusive language.
  - **Image Scanner (OCR)**: Integrated Tesseract OCR to extract text from uploaded images and check for malicious content.
- **Learning Center & Chatbot**: Built educational modules and an interactive, rule-based AI chatbot to answer cyber safety questions on the fly.
- **Structured Packaging**: Segregated code properly into `frontend` and `backend` directories and provided convenient run-scripts (`run_all.bat`) for immediate offline usage.

## Why It Was Done

The primary goal of this project is to create an accessible, user-friendly tool to directly empower individuals against rising cyber threats. 
- **Education First**: By combining active scanning tools with a dedicated Learning Center and Chatbot, the platform doesn't just block threats—it explains *why* something is dangerous.
- **Accountability & Tracking**: Integrating a personalized dashboard ensures users can review their scan history and track their learning progress over time.
- **Open Source Readiness**: The code was specifically structured, cleaned of temporary database and cache files, and packaged with clear instructions so anyone can download, run, and learn from the platform locally without complex setups.

---

## Project Structure

```
cyber-safety-platform/
│
├── backend/              # Python Flask application
│   ├── app.py            # Main entry point for the API
│   ├── auth_utils.py     # JWT Authentication utilities
│   ├── chatbot_engine.py # AI Chatbot logic 
│   ├── database/         # SQLite database folder (DB auto-generates on run)
│   ├── db_utils.py       # Database connection and queries
│   ├── ocr_scanner.py    # Image text extraction (requires Tesseract)
│   ├── phishing_detector.py # Text scanning logic
│   ├── url_checker.py    # URL reputation logic
│   └── uploads/          # Temporary storage for uploaded images
│
├── frontend/             # HTML, CSS, Vanilla JS 
│   ├── index.html        # Landing page
│   ├── dashboard.html    # User dashboard
│   ├── style.css         # Clean, modern UI styling
│   └── ...               
│
├── requirements.txt      # Python dependencies
├── start_backend.bat     # Windows script to run the backend API
├── start_frontend.bat    # Windows script to run frontend web server
└── run_all.bat           # Master script to run both servers simultaneously
```

## Prerequisites

1. **Python 3.8+**: Make sure Python is installed and added to your system PATH.
2. **Tesseract OCR (Required for Image Scan)**: 
   - Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install it (usually to `C:\Program Files\Tesseract-OCR\tesseract.exe`).

## Setup Instructions

1. **Install Dependencies**:
   Open a terminal in the project directory and run:
   ```cmd
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   - Simply double-click `run_all.bat`. This will start the backend on port 5000, start the frontend on port 8000, and automatically open your default web browser to the application.

3. **Usage**:
   - Register a new account.
   - Start scanning URLs, text, or images directly from the dashboard!
