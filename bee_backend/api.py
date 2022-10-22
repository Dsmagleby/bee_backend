from datetime import date
from ninja import NinjaAPI, Schema, Field
from typing import List
from bee_backend.settings import SECRET_CRED
from .models import Hive, Observation, GlobalNote
from ninja.security import HttpBearer


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == SECRET_CRED:
            return token


api = NinjaAPI()


class HiveSchema(Schema):
    id: int = Field(None, alias="id")
    userid: str
    number: str
    colour: str
    place: str
    frames: int
    archived: bool


class ObservationSchema(Schema):
    id: int = Field(None, alias="id")
    hive: int = Field(None, alias="hive.id")
    observation_date: date
    observation: str = None
    userid: str
    queen: int
    larva: int
    egg: int
    mood: int
    size: int
    varroa: int


class GlobalNoteSchema(Schema):
    id: int = Field(None, alias="id")
    note: str


# check if service is up
@api.get("/status")
def check_status(request):
    return {"status": "ok"}


# get all hives for a user
@api.get("/hives/{userid}/{status}", response=List[HiveSchema], auth=AuthBearer())
def get_hives(request, userid: str, status: str):
    if status == "deleted":
        return Hive.objects.filter(userid=userid, deleted=True)
    elif status == "archived":
        return Hive.objects.filter(userid=userid, archived=True)
    else:
        return Hive.objects.filter(userid=userid, archived=False, deleted=False)


# create new hive or update existing
@api.post("/hive", response=HiveSchema, auth=AuthBearer())
def create_hive(request, payload: HiveSchema):
    hive, _ = Hive.objects.get_or_create(
        id=payload.id,
        userid=payload.userid,
        defaults={
            "number": payload.number,
            "colour": payload.colour,
            "place": payload.place,
            "frames": payload.frames,
            "archived": payload.archived,
        }
    )
    return hive


# delete hive (soft delete)
@api.delete("/hive", response=HiveSchema, auth=AuthBearer())
def delete_hive(request, payload: HiveSchema):
    hive = Hive.objects.get(id=payload.id)
    hive.deleted = True
    hive.save()
    return hive


# get all observations for a user
# limit: max allowed observations per hive
@api.get("/obs/{userid}/{limit}", response=List[ObservationSchema], auth=AuthBearer())
def get_observations(request, userid: str, limit: int):
    hives = Hive.objects.filter(userid=userid, deleted=False)
    obs = Observation.objects.none()
    for hive in hives:
        obs = obs | Observation.objects.filter(hive__id=hive.id, deleted=False).order_by('observation_date')[:limit]
    return obs


# create new observation
@api.post("/obs", response=ObservationSchema, auth=AuthBearer())
def create_observation(request, payload: ObservationSchema):
    hive = Hive.objects.get(id=payload.hive)
    obs = Observation.objects.get_or_create(
        id=payload.id,
        hive=hive,
        userid=payload.userid,
        defaults={
            "observation_date": payload.observation_date,
            "observation": payload.observation,
            "queen": payload.queen,
            "larva": payload.larva,
            "egg": payload.egg,
            "mood": payload.mood,
            "size": payload.size,
            "varroa": payload.varroa,
        }
    )
    return obs


# delete observation (soft delete)
@api.delete("/obs", response=ObservationSchema, auth=AuthBearer())
def delete_observation(request, payload: ObservationSchema):
    obs = Observation.objects.get(id=payload.id)
    obs.deleted = True
    obs.save()
    return obs


# get all global notes for a user
@api.get("/notes/{userid}", response=List[GlobalNoteSchema], auth=AuthBearer())
def get_notes(request, userid: str):
    return GlobalNote.objects.filter(userid=userid, deleted=False)


# create new global note
@api.post("/note", response=GlobalNoteSchema, auth=AuthBearer())
def create_note(request, payload: GlobalNoteSchema):
    note, _ = GlobalNote.objects.get_or_create(
        id = payload.id,
        defaults={
            "note": payload.note,
        }
    )
    return note


# delete global note (soft delete)
@api.delete("/note", response=GlobalNoteSchema, auth=AuthBearer())
def delete_note(request, payload: GlobalNoteSchema):
    note = GlobalNote.objects.get(id=payload.id)
    note.deleted = True
    note.save()
    return note


