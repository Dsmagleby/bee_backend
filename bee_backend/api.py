from datetime import date
from ninja import NinjaAPI, Schema, Field
from ninja.security import HttpBearer
from typing import List
from bee_backend.settings import SECRET_CRED
from .models import Hive, Observation, GlobalNote
from .tools import log_activity


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == SECRET_CRED:
            return token


api = NinjaAPI()


class HiveSchema(Schema):
    # post be called as "id" on post and delete requests 
    sid: int = Field(None, alias="id")
    userid: str
    number: str
    colour: str
    place: str
    frames: int = None
    archived: bool


class ObservationSchema(Schema):
    id: int = Field(None, alias="id")
    # sid must be called as "hive.id" in post and delete requests
    sid: int = Field(None, alias="hive.id") 
    date: date
    comment: str = None
    userid: str
    queen: int
    larva: int
    egg: int
    mood: int
    size: int
    varroa: int


class GlobalNoteSchema(Schema):
    id: int = Field(None, alias="id")
    userid: str
    note: str


# check if service is up
@api.get("/status", auth=AuthBearer())
def check_status(request):
    log_activity("status")
    return {"status": "ok"}


# get all hives for a user
@api.get("/hives/{userid}/{status}", response=List[HiveSchema], auth=AuthBearer())
def get_hives(request, userid: str, status: str):
    log_activity(userid)
    if status == "deleted":
        return Hive.objects.filter(userid=userid, deleted=True)
    elif status == "archived":
        return Hive.objects.filter(userid=userid, archived=True)
    else:
        return Hive.objects.filter(userid=userid, archived=False, deleted=False)


# create new hive or update existing
@api.post("/hive", response=HiveSchema, auth=AuthBearer())
def create_hive(request, payload: HiveSchema):
    log_activity(payload.userid)
    hive, created = Hive.objects.get_or_create(
        id=payload.sid,
        userid=payload.userid,
        defaults={
            "number": payload.number,
            "colour": payload.colour,
            "place": payload.place,
            "frames": payload.frames,
            "archived": payload.archived,
        }
    )
    # if hive already exists, update it
    if not created:
        hive.number = payload.number
        hive.colour = payload.colour
        hive.place = payload.place
        hive.frames = payload.frames
        hive.archived = payload.archived
        hive.save()
    return hive


# delete hive (soft delete)
@api.delete("/hive", response=HiveSchema, auth=AuthBearer())
def delete_hive(request, payload: HiveSchema):
    log_activity(payload.userid)
    hive = Hive.objects.get(id=payload.id)
    hive.deleted = True
    hive.save()
    return hive


# get all observations for a user
# limit: max allowed observations per hive
@api.get("/obs/{userid}/{limit}", response=List[ObservationSchema], auth=AuthBearer())
def get_observations(request, userid: str, limit: int):
    log_activity(userid)
    hives = Hive.objects.filter(userid=userid, deleted=False)
    obs = Observation.objects.none()
    for hive in hives:
        obs = obs | Observation.objects.filter(hive__id=hive.id, deleted=False).order_by('date')[:limit]
    return obs


# create new comment
@api.post("/obs", response=ObservationSchema, auth=AuthBearer())
def create_observation(request, payload: ObservationSchema):
    log_activity(payload.userid)
    print(payload.sid)
    hive = Hive.objects.get(id=payload.sid)
    obs, created = Observation.objects.get_or_create(
        id=payload.id,
        hive=hive,
        userid=payload.userid,
        defaults={
            "date": payload.date,
            "comment": payload.comment,
            "queen": payload.queen,
            "larva": payload.larva,
            "egg": payload.egg,
            "mood": payload.mood,
            "size": payload.size,
            "varroa": payload.varroa,
        }
    )
    # if comment already exists, update it
    if not created:
        obs.date = payload.date
        obs.comment = payload.comment
        obs.queen = payload.queen
        obs.larva = payload.larva
        obs.egg = payload.egg
        obs.mood = payload.mood
        obs.size = payload.size
        obs.varroa = payload.varroa
        obs.save()
    return obs


# delete comment (soft delete)
@api.delete("/obs", response=ObservationSchema, auth=AuthBearer())
def delete_observation(request, payload: ObservationSchema):
    log_activity(payload.userid)
    obs = Observation.objects.get(id=payload.id)
    obs.deleted = True
    obs.save()
    return obs


# get all global notes for a user
@api.get("/notes/{userid}", response=List[GlobalNoteSchema], auth=AuthBearer())
def get_notes(request, userid: str):
    log_activity(userid)
    return GlobalNote.objects.filter(userid=userid, deleted=False)


# create new global note
@api.post("/note", response=GlobalNoteSchema, auth=AuthBearer())
def create_note(request, payload: GlobalNoteSchema):
    log_activity(payload.userid)
    note, created = GlobalNote.objects.get_or_create(
        id = payload.id,
        userid = payload.userid,
        defaults={
            "note": payload.note,
        }
    )
    # if note already exists, update it
    if not created:
        note.note = payload.note
        note.save()
    return note


# delete global note (soft delete)
@api.delete("/note", response=GlobalNoteSchema, auth=AuthBearer())
def delete_note(request, payload: GlobalNoteSchema):
    log_activity(payload.userid)
    note = GlobalNote.objects.get(id=payload.id)
    note.deleted = True
    note.save()
    return note


