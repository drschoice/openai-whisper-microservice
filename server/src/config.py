import os
from dotenv import load_dotenv, find_dotenv

# Debug to show which file is being loaded
env_path = find_dotenv()
print(f"Looking for .env file at: {env_path}")

# Load environment variables from .env file
result = load_dotenv()
print(f".env file loaded successfully: {result}")


# Environment settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "production").lower()
IS_DEVELOPMENT = ENVIRONMENT == "development"

print(f"Environment: {ENVIRONMENT}")
print(f"Is development mode: {IS_DEVELOPMENT}")
print(f"API key: {not not os.getenv('API_KEY')}")

# API security settings
API_KEY = os.getenv("API_KEY", "")
API_KEY_REQUIRED = not IS_DEVELOPMENT and API_KEY != ""

# Function to validate API key
def is_valid_api_key(api_key: str) -> bool:
    """
    Validate the API key from request against the configured API key.
    Returns True if valid or if API key is not required.
    """
    if not API_KEY_REQUIRED:
        return True
    
    return api_key == API_KEY