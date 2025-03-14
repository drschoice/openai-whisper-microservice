from fastapi import Request, HTTPException
import base64
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from starlette.responses import Response
from typing import Optional, Tuple
from src.config import is_valid_api_key, API_KEY_REQUIRED, API_KEY

# API key header name
API_KEY_HEADER = "X-API-Key"
# Basic auth constants
BASIC_AUTH_USERNAME = "whisper"

class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check for valid API key in request headers or basic authentication.
    Only applies to paths starting with /api/
    """
    
    def __init__(self, app):
        super().__init__(app)
    
    def _decode_basic_auth(self, auth_header: str) -> Tuple[str, str]:
        """
        Decode the basic authentication header to extract username and password
        Returns a tuple of (username, password)
        """
        try:
            auth_type, credentials = auth_header.split(' ', 1)
            if auth_type.lower() != 'basic':
                return None, None
                
            decoded = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded.split(':', 1)
            return username, password
        except Exception:
            return None, None
    
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for non-api paths
        if not request.url.path.startswith("/api/"):
            return await call_next(request)
        
        # Skip API key validation if not required
        if not API_KEY_REQUIRED:
            return await call_next(request)
        
        # Authentication successful flag
        auth_success = False
        
        # Check API Key header first
        api_key: Optional[str] = request.headers.get(API_KEY_HEADER)
        if api_key and is_valid_api_key(api_key):
            auth_success = True
        
        # If API key failed or not provided, try basic auth
        if not auth_success:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                username, password = self._decode_basic_auth(auth_header)
                
                # Check if username is 'whisper' and password matches API_KEY
                if username == BASIC_AUTH_USERNAME and password == API_KEY:
                    auth_success = True
        
        # If authentication is still not successful, deny access
        if not auth_success:
            # Return 401 Unauthorized for basic auth failure
            if request.headers.get('Authorization'):
                response = Response(
                    content="Unauthorized",
                    status_code=HTTP_401_UNAUTHORIZED,
                    headers={"WWW-Authenticate": "Basic"}
                )
                return response
            # Return 403 Forbidden for API key failures
            else:
                return Response(
                    content='{"detail": "Invalid or missing API key"}',
                    status_code=HTTP_403_FORBIDDEN,
                    media_type="application/json"
                )
            
        # Continue with request if authentication is successful
        response = await call_next(request)
        return response