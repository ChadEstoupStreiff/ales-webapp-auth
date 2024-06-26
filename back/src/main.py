import datetime
import logging

import grpc
import jwt
import main_pb2 as reservation_pb2
import main_pb2_grpc as reservation_pb2_grpc
import requests
from dotenv import dotenv_values
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

logging.basicConfig(level=logging.DEBUG)
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

JWT_SECRET = config["JWT_SECRET"]
JWT_ALGORITHM = config["JWT_ALGORITHM"]
###############################
#        Google Auth          #
###############################
GOOGLE_CLIENT_ID = config["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = config["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = "http://localhost:8901/auth/google"


@app.get("/login/google", tags=["Google"])
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@app.get("/auth/google", tags=["Google"])
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

###############################
#          KEYCLOAK           #
###############################
KEYCLOAK_SERVER_URL = config["KEYCLOAK_SERVER_URL"]
KEYCLOAK_REALM = config["KEYCLOAK_REALM"]
KEYCLOAK_CLIENT_ID = config["KEYCLOAK_CLIENT_ID"]
KEYCLOAK_CLIENT_SECRET = config["KEYCLOAK_CLIENT_SECRET"]
KEYCLOAK_REDIRECT_URI = "http://localhost:8901/auth/keycloak"

@app.get("/login/keycloak", tags=["Keycloak"])
async def login_keycloak():
    return {
        "url": f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth?response_type=code&client_id={KEYCLOAK_CLIENT_ID}&redirect_uri={KEYCLOAK_REDIRECT_URI}&scope=openid%20profile%20email"
    }

@app.get("/auth/keycloak", tags=["Keycloak"])
async def auth_keycloak(code: str):
    token_url = f"http://keycloak:8080/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "code": code,
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "redirect_uri": KEYCLOAK_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    response_data = response.json()
    access_token = response_data.get("access_token")
    logging.critical(access_token)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_info = requests.get(
        f"http://keycloak:8080/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    logging.critical(user_info)
    user_info = user_info.json()

    token = jwt.encode(
        {
            "sub": user_info["sub"],
            "name": user_info["name"],
            "email": user_info["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return {"access_token": token, "token_type": "bearer"}


###############################
#            Auth             #
###############################

@app.get("/token", tags=["User"])
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


def get_current_user(token: str):
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


###############################
#         Endpoints           #
###############################


@app.get("/hotels/reservations", tags=["Hotel"])
async def get_hotels_reservations(token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)

    with grpc.insecure_channel("resa_grpc:8080") as channel:
        hotel_stub = reservation_pb2_grpc.HotelReservationStub(channel)

        hotel_request = reservation_pb2.ListHotelsRequest(
            user_id=user["sub"],
        )
        hotels_response = hotel_stub.ListReservedHotels(hotel_request)

        hotels = [
            {
                "hotel_id": hotel.hotel_id,
                "user_id": hotel.user_id,
                "check_in_date": hotel.check_in_date,
                "check_out_date": hotel.check_out_date,
                "number_of_rooms": hotel.number_of_rooms,
            }
            for hotel in hotels_response.hotels
        ]
        return hotels
    return None


@app.post("/hotels/reserve", tags=["Hotel"])
async def add_hotels_reservation(
    hotel: str,
    token: str = Depends(oauth2_scheme),
):
    user = get_current_user(token)

    with grpc.insecure_channel("resa_grpc:8080") as channel:
        hotel_stub = reservation_pb2_grpc.HotelReservationStub(channel)

        hotel_request = reservation_pb2.HotelRequest(
            hotel_id=hotel,
            user_id=user["sub"],
        )

        hotel_stub.ReserveHotel(hotel_request)
    return True


@app.get("/flights/reservations", tags=["Flight"])
async def get_flights_reservations(token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)

    with grpc.insecure_channel("resa_grpc:8080") as channel:
        flight_stub = reservation_pb2_grpc.FlightReservationStub(channel)

        flight_request = reservation_pb2.ListFlightsRequest(
            user_id=user["sub"],
        )
        flights_response = flight_stub.ListReservedFlights(flight_request)

        flights = [
            {
                "flight_id": flight.flight_id,
                "departure_date": flight.departure_date,
                "return_date": flight.return_date,
                "number_of_tickets": flight.number_of_tickets,
            }
            for flight in flights_response.flights
        ]
        return flights
    return None


@app.post("/flights/reserve", tags=["Flight"])
async def add_flights_reservation(
    flight: str,
    token: str = Depends(oauth2_scheme),
):
    user = get_current_user(token)

    with grpc.insecure_channel("resa_grpc:8080") as channel:
        flight_stub = reservation_pb2_grpc.FlightReservationStub(channel)

        flight_request = reservation_pb2.FlightRequest(
            flight_id=flight,
            user_id=user["sub"],
        )

        flight_stub.ReserveFlight(flight_request)
    return True
