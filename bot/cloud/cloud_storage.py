import os
from urllib.parse import quote_plus
from google.auth.transport.requests import AuthorizedSession

from . import scoped_credentials

def upload_to_cloud_storage(stream, cloud_file):
    authed_session = AuthorizedSession(scoped_credentials)

    req_body = {
        "name": cloud_file,
    }

    headers = {
        "X-Upload-Content-Type": "application/actet-stream",
        "X-Upload-Content-Length": str(len(stream)),
        "Content-Type": "application/json; charset=UTF-8",
        "Content-Length": str(len(req_body)),
    }

    response = authed_session.post(
        "https://www.googleapis.com/upload/storage/v1/b/telegram-majyobot-photo/o?uploadType=resumable", 
        headers=headers,
        json=req_body
    )

    if response.status_code == 200:
        print("Upload initiated!")
        loc = response.headers.get("Location")
        response_2 = authed_session.post(
            loc,
            data=stream
        )
        return response_2.json().get("selfLink")
    else:
        return None
