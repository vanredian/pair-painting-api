from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from uuid import UUID, uuid4

app = FastAPI()

# Настройка CORS
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
#! Здесь
class RoomCreateRequest(BaseModel):
    name: str

class RoomJoinRequest(BaseModel):
    uid: UUID
    name: str

class Room(BaseModel):
    uid: UUID
    participants: List[str] = []

# Хранилище комнат
rooms: Dict[UUID, Room] = {}

@app.post("/join-or-create-room")
async def join_or_create_room(request: RoomCreateRequest):
    room_uid = uuid4()
    new_room = Room(uid=room_uid, participants=[request.name])
    rooms[room_uid] = new_room
    return {"uid": room_uid, "participants": new_room.participants}

@app.post("/join-room")
async def join_room(request: RoomJoinRequest):
    room = rooms.get(request.uid)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    room.participants.append(request.name)
    return {"uid": room.uid, "participants": room.participants}

@app.get("/room/{uid}")
async def get_room(uid: UUID):
    room = rooms.get(uid)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"uid": room.uid, "participants": room.participants}

@app.get("/rooms")
async def get_all_rooms():
    return rooms
