import datetime
import logging

import jwt
import requests
from dotenv import dotenv_values
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

config = dotenv_values("/.env")

###############################
#        Google Auth          #
###############################]
GOOGLE_CLIENT_ID = config["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = config["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = "http://localhost:8901/auth"
JWT_SECRET = config["JWT_SECRET"]
JWT_ALGORITHM = "HS256"


@app.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@app.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_info = user_info.json()

    token = jwt.encode(
        {
            "sub": user_info["id"],
            "name": user_info["name"],
            "email": user_info["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return {"access_token": token, "token_type": "bearer"}


@app.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

###############################
#         Endpoints           #
###############################


@app.get("/hotels/reservations", tags=["Hotel"])
async def get_hotels_reservations(token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    return None


@app.post("/hotels/reserve", tags=["Hotel"])
async def add_hotels_reservation(
    hotel: str,
    token: str = Depends(oauth2_scheme),
):
    user = get_current_user(token)
    return None


@app.post("/flies/reservations", tags=["Fly"])
async def get_flies_reservations(token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    return None


@app.post("/flies/reserve", tags=["Fly"])
async def add_flies_reservation(
    fly: str,
    token: str = Depends(oauth2_scheme),
):
    user = get_current_user(token)
    return None
