import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
import logging

logger = logging.getLogger()
secret_key = os.environ["jwt_token_secret_key"]
bearer_scheme = HTTPBearer()

async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials

    try:
        header_data = jwt.get_unverified_header(token)
        decoded_token = jwt.decode(token, secret_key, algorithms=[header_data['alg']])
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token',
        )

    return decoded_token