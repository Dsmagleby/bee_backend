from django.db.models import Count

from datetime import date
from ninja import NinjaAPI, Schema, Field
from typing import List
from .models import Hive, Observation
from ninja.security import HttpBearer


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaAPI()


class HiveSchema(Schema):
    userid: str
    number: int
    colour: str
    place: str
    frames: int


class ObservationSchema(Schema):
    hive: int = Field(None, alias="hive.id")
    observation_date: date
    observation: str = None
    userid: str
    queen: int
    larva: int
    egg: int
    mood: int
    size: int


class Error(Schema):
    message: str


# check if service is up
@api.get("/status")
def check_status(request):
    return {"status": "ok"}


# get all hives for a user
@api.get("/hives/{userid}", response=List[HiveSchema], auth=AuthBearer())
def hello(request, userid: str):
    hives = Hive.objects.filter(userid=userid)
    return hives


# create new hive or update existing
@api.post("/hive", response={200: HiveSchema, 403: Error}, auth=AuthBearer())
def create_hive(request, payload: HiveSchema):
    hive, _ = Hive.objects.get_or_create(**payload.dict())
    return hive


# get all observations for a user
# limit: max allowed observations per hive
@api.get("/obs/{userid}/{limit}", response=List[ObservationSchema], auth=AuthBearer())
def hello(request, userid: str, limit: int):
    obs = Observation.objects.filter(userid=userid)
    # limit observations per hive
    
    return obs


# create new observation
@api.post("/obs", response={200: ObservationSchema, 403: Error}, auth=AuthBearer())
def create_hive(request, payload: ObservationSchema):
    hive = Hive.objects.get(id=payload.hive)
    obs = Observation.objects.create(
        hive=hive,
        observation_date=payload.observation_date,
        observation=payload.observation,
        userid=payload.userid,
        queen=payload.queen,
        larva=payload.larva,
        egg=payload.egg,
        mood=payload.mood,
        size=payload.size
    )
    return obs


