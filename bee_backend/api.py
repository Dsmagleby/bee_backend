from datetime import date
from ninja import NinjaAPI, Schema, Field
from typing import List
from .models import Hive, Observation, GlobalNote
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


class GlobalNoteSchema(Schema):
    noteid: int = Field(None, alias="id")
    note: str


# check if service is up
@api.get("/status")
def check_status(request):
    return {"status": "ok"}


# get all hives for a user
@api.get("/hives/{userid}", response=List[HiveSchema], auth=AuthBearer())
def get_hives(request, userid: str):
    hives = Hive.objects.filter(userid=userid)
    return hives


# create new hive or update existing
@api.post("/hive", response=HiveSchema, auth=AuthBearer())
def create_hive(request, payload: HiveSchema):
    hive, _ = Hive.objects.get_or_create(**payload.dict())
    return hive


# get all observations for a user
# limit: max allowed observations per hive
@api.get("/obs/{userid}/{limit}", response=List[ObservationSchema], auth=AuthBearer())
def get_observations(request, userid: str, limit: int):
    obs = Observation.objects.filter(userid=userid)
    # limit observations per hive
    
    return obs


# create new observation
@api.post("/obs", response=ObservationSchema, auth=AuthBearer())
def create_observation(request, payload: ObservationSchema):
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


# get all global notes for a user
@api.get("/notes/{userid}", response=List[GlobalNoteSchema], auth=AuthBearer())
def get_notes(request, userid: str):
    notes = GlobalNote.objects.filter(userid=userid)
    return notes


# create new global note
@api.post("/note", response=GlobalNoteSchema, auth=AuthBearer())
def create_note(request, payload: GlobalNoteSchema):
    note, _ = GlobalNote.objects.get_or_create(**payload.dict())
    return note


