import json
import requests
from globals import BASE_URL, CREDENTIALS, auth_header
import models

with open('configs/DefaultServer.json', 'r', encoding='utf-8') as fp:
    server_json = json.load(fp)
    default_server = models.ServerConfig.model_validate(server_json).model_dump()

def test_import_export():
    login_res = requests.post(f'{BASE_URL}/auth/login', data=CREDENTIALS)
    access_token = login_res.json()['access_token']
    import_res = requests.post(f'{BASE_URL}/config/import',
                              json=default_server,
                              headers=auth_header(access_token))
    assert import_res.status_code == 200, import_res.json()

    export_res = requests.get(f'{BASE_URL}/config/export?server_name={default_server["name"]}',
                              headers=auth_header(access_token))
    assert export_res.status_code == 200, export_res.json()
    assert export_res.json() == default_server, export_res.json()
