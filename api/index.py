import sys
import os

# Add the root directory to the Python path
root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

# Add the backend directory itself just in case
backend_path = os.path.join(root_path, 'backend')
sys.path.append(backend_path)

# Import the actual Flask app
from backend.app import app
