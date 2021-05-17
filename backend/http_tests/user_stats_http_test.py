import requests
import json
from src import config
from src.auth import create_token

def test_http_success_user_stats():
    user_info = {"email": "erwurbt@gml.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    user = requests.post(config.url + 'auth/register/v2', json = user_info)    
    user_dict = user.json()
    params = {'token': user_dict['token']}
    ret = requests.get(config.url + 'user/stats/v1', params = params)
    assert ret.status_code == 200

def test_invalid_auth_id_user_stats():
    bad_token = create_token(-5, 1)
    params = {'token': bad_token}
    assert requests.get(config.url + 'user/stats/v1', params = params).status_code == 403   