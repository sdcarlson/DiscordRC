import json
import os
import requests
from globals import BASE_URL, CREDENTIALS, auth_header
import models

CONFIG_DIR = './configs'
filenames = [os.path.join(CONFIG_DIR, f) for f
    in os.listdir(CONFIG_DIR)
    if os.path.isfile(os.path.join(CONFIG_DIR, f))
]
configs = []
for filename in filenames:
    with open(filename, 'r', encoding='utf-8') as fp:
        server_json = json.load(fp)
        configs.append(models.ServerConfig.model_validate(server_json).model_dump())

def test_import_export():
    login_res = requests.post(f'{BASE_URL}/auth/login', data=CREDENTIALS)
    access_token = login_res.json()['access_token']

    for config in configs:
        import_res = requests.post(
            f'{BASE_URL}/config/import',
            json=config,
            headers=auth_header(access_token)
        )
        assert import_res.status_code == 200, import_res.json()

        export_res = requests.get(
            f'{BASE_URL}/config/export?server_name={config["name"]}',
            headers=auth_header(access_token)
        )
        assert export_res.status_code == 200, export_res.json()
        assert export_res.json() == config, export_res.json()
