import pytest
import requests
from globals import BASE_URL, CREDENTIALS

@pytest.mark.order('first')
def test_signup():
    res = requests.post(f'{BASE_URL}/auth/signup', data=CREDENTIALS)
    assert res.status_code == 200, res.json()

def test_signup_duplicate_user():
    res = requests.post(f'{BASE_URL}/auth/signup', data=CREDENTIALS)
    assert res.status_code == 400, res.json()

def test_login():
    res = requests.post(f'{BASE_URL}/auth/login', data=CREDENTIALS)
    assert res.status_code == 200, res.json()
