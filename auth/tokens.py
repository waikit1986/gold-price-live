from authlib.jose import JsonWebEncryption
from datetime import datetime, timedelta, timezone
import json
import os
import base64

jwe = JsonWebEncryption()
JWE_SECRET_KEY = base64.b64decode(os.getenv("JWE_SECRET_KEY"))
JWE_HEADER = {"alg": "dir", "enc": "A256GCM"}

def create_access_token(user, expires_delta: timedelta = timedelta(days=1)):
    expires_at = datetime.now(timezone.utc) + expires_delta
    payload = {
        "exp": int(expires_at.timestamp()),
        "user_id": str(user.id),
        "type": "access_token",
    }
    token = jwe.serialize_compact(JWE_HEADER, json.dumps(payload).encode(), JWE_SECRET_KEY)
    print("Access Token Expiry:", expires_at.timestamp())
    return token, expires_at.timestamp()

def create_refresh_token(user, expires_delta: timedelta = timedelta(days=30)):
    expires_at = datetime.now(timezone.utc) + expires_delta
    payload = {
        "exp": int(expires_at.timestamp()),
        "user_id": str(user.id),
        "type": "refresh_token",
    }
    token = jwe.serialize_compact(JWE_HEADER, json.dumps(payload).encode(), JWE_SECRET_KEY)
    print("Refresh Token Expiry:", expires_at.timestamp())
    return token, expires_at.timestamp()

def decrypt_token(token: str):
    decrypted = jwe.deserialize_compact(token, JWE_SECRET_KEY)
    return json.loads(decrypted["payload"])

