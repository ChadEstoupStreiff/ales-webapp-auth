import datetime
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://path/to/realm/protocol/openid-connect/token",
    authorizationUrl="http://path/to/realm/protocol/openid-connect/auth",
    refreshUrl="http://path/to/realm/protocol/openid-connect/token",
)


async def valid_access_token(access_token: Annotated[str, Depends(oauth_2_scheme)]):
    url = "http://path/to/realm/protocol/openid-connect/certs"
    optional_custom_headers = {"User-agent": "custom-user-agent"}
    jwks_client = PyJWKClient(url, headers=optional_custom_headers)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="api",
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.get(
    "/hotels/reservations", tags=["Hotel"], dependencies=[Depends(valid_access_token)]
)
async def get_hotels_reservations(user: str):
    return None


@app.post("/hotels/reserve", tags=["Hotel"], dependencies=[Depends(valid_access_token)])
async def add_hotels_reservation(
    user: str,
    hotel: str,
    check_in: datetime.datetime,
    check_out: datetime.datetime,
    nbr_room: int,
    nbr_people: int,
):
    return None


@app.post(
    "/flies/reservations", tags=["Fly"], dependencies=[Depends(valid_access_token)]
)
async def get_flies_reservations(user: str):
    return None


@app.post("/flies/reserve", tags=["Fly"], dependencies=[Depends(valid_access_token)])
async def add_flies_reservation(
    user: str, fly: str, departure: datetime.datetime, nbr_tickets: int
):
    return None
