# SECURITY CORS SETTINGS
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True  # !also uncomment next 3 lines

CORS_ALLOW_HEADERS = (
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Credentials',
)
CORS_EXPOSE_HEADERS = ['Content-Type', 'api_key', 'X-CSRFToken', 'Authorization']
#CORS_ALLOW_CREDENTIALS = True
"""
CORS_ORIGIN_WHITELIST = (
       'localhost: 3000',  # URL для клиентской части 
)
"""
CORS_URLS_REGEX = r'^/api/.*$'

# SECURITY CSRF SETTINGS
# ------------------------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1']
