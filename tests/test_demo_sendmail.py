import requests
import json

API_URI = 'http://localhost:5000'


def test_demo_sendmail():

    data = {
        "account": {
            "email": "n.hung19920@gmail.com",
            "name": "name"
        },
        "info": {
            "description": "Chao, day la tin nhan he thong"
        }
    }

    url = r"/demo/send_mail"

    resp = requests.post(API_URI + url, json=data)
    assert resp.status_code == 200

    resp_body = resp.json()

    assert ("id" in resp_body.keys())




