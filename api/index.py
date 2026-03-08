import sys
import os

# Add the backend directory to the Python path so Vercel can find the modules
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.append(backend_path)

# Import the actual Flask app
from app import app

# Vercel serverless expects the app object
