import requests
import json
API_URI = 'http://localhost:5000'


def test_demo_sendmail_en():

    url = "/demo/send_mail"

    payload = json.dumps({
        "account": {
            "email": "n.hung19920@gmail.com",
            "name": "HungNguyen"
        },
        "info": {
            "description": "sendmail demo with celery worker"
        }
    })

    languages = ["en", "vi"]

    for language in languages:

        headers = {
            'Accept-Language': language,
            'Content-Type': 'application/json'
        }

        resp = requests.request("POST", API_URI + url, headers=headers, data=payload)
        assert resp.status_code == 200

        resp_body = resp.json()
        assert ("id" in resp_body.keys())


