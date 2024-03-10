BASE_URL = 'http://localhost:8000'
CREDENTIALS = {'username': 'alice', 'password': 'password'}

def auth_header(token):
    return { 'Authorization': f'Bearer {token}' }
