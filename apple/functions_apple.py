from fastapi import HTTPException
import os
from dotenv import load_dotenv
from typing import Optional
import httpx
import hashlib
import base64
from jose import jwt, JWTError
from cryptography.hazmat.primitives.asymmetric import rsa

load_dotenv()

APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID")


def construct_apple_public_key(key_data: dict):
    n = int.from_bytes(base64.urlsafe_b64decode(key_data['n'] + '=='), byteorder='big')
    e = int.from_bytes(base64.urlsafe_b64decode(key_data['e'] + '=='), byteorder='big')
    public_numbers = rsa.RSAPublicNumbers(e, n)
    return public_numbers.public_key()

async def get_apple_public_key(kid: str) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://appleid.apple.com/auth/keys")
        keys = response.json().get("keys", [])
        return next((k for k in keys if k["kid"] == kid), None)

async def verify_apple_token(id_token: str, nonce: str) -> dict:
    try:
        header = jwt.get_unverified_header(id_token)
        kid = header.get("kid")
        if not kid:
            raise HTTPException(400, detail="Invalid Apple token header: missing 'kid'")

        public_key_data = await get_apple_public_key(kid)
        if not public_key_data:
            raise HTTPException(400, detail="Apple public key not found")

        public_key = construct_apple_public_key(public_key_data)

        decoded = jwt.decode(
            id_token,
            key=public_key,
            algorithms=["RS256"],
            audience=APPLE_CLIENT_ID,
            issuer="https://appleid.apple.com",
            options={"verify_nonce": False}
        )

        expected_nonce_hash = hashlib.sha256(nonce.encode()).hexdigest()
        token_nonce = decoded.get("nonce")

        if not token_nonce or token_nonce.lower() != expected_nonce_hash.lower():
            raise HTTPException(400, detail="Nonce mismatch")

        return decoded

    except jwt.ExpiredSignatureError:
        raise HTTPException(400, detail="Apple ID token has expired")
    except JWTError as e:
        raise HTTPException(400, detail=f"Invalid Apple ID token: {e}")
    except Exception as e:
        raise HTTPException(400, detail=f"Apple token verification failed: {e}")
