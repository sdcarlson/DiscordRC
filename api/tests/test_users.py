import requests
from globals import BASE_URL, CREDENTIALS, auth_header

def test_get_user():
    login_res = requests.post(f'{BASE_URL}/auth/login', data=CREDENTIALS)
    access_token = login_res.json()['access_token']
    res = requests.get(f'{BASE_URL}/users/me', headers=auth_header(access_token))
    assert res.status_code == 200

def test_get_user_unauthenticated():
    res = requests.get(f'{BASE_URL}/users/me')
    assert res.status_code == 401
