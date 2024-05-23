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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class RoomCreateRequest(BaseModel):
    name: str  # Имя пользователя для создания комнаты

class RoomJoinRequest(BaseModel):
    uid: UUID  # UID комнаты для присоединения
    name: str  # Имя пользователя для присоединения

class Room(BaseModel):
    uid: UUID  # UID комнаты
    participants: List[str] = []  # Список участников комнаты

# Хранилище комнат
rooms: Dict[UUID, Room] = {}

@app.post("/join-or-create-room")
async def join_or_create_room(request: RoomCreateRequest):
    """
    Создание новой комнаты или присоединение к существующей.
    Возвращает UID комнаты и список участников.
    """
    room_uid = uuid4()  # Создание уникального идентификатора для новой комнаты
    new_room = Room(uid=room_uid, participants=[request.name])  # Создание объекта комнаты
    rooms[room_uid] = new_room  # Сохранение комнаты в хранилище
    return {"uid": room_uid, "participants": new_room.participants}  # Возвращаем UID и участников

@app.post("/join-room")
async def join_room(request: RoomJoinRequest):
    """
    Присоединение к существующей комнате.
    Возвращает UID комнаты и список участников.
    """
    room = rooms.get(request.uid)  # Поиск комнаты по UID
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")  # Ошибка, если комната не найдена
    room.participants.append(request.name)  # Добавление участника в комнату
    return {"uid": room.uid, "participants": room.participants}  # Возвращаем UID и участников

@app.get("/room/{uid}")
async def get_room(uid: UUID):
    """
    Получение информации о комнате по UID.
    Возвращает UID комнаты и список участников.
    """
    room = rooms.get(uid)  # Поиск комнаты по UID
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")  # Ошибка, если комната не найдена
    return {"uid": room.uid, "participants": room.participants}  # Возвращаем UID и участников

@app.get("/rooms")
async def get_all_rooms():
    """
    Получение информации обо всех комнатах.
    Возвращает словарь всех комнат.
    """
    return rooms  # Возвращаем все комнаты

# Пример JSON запросов и ответов

# 1. Создание или присоединение к комнате:
# Запрос:
# {
#   "name": "Alice"
# }
# Ответ:
# {
#   "uid": "some-unique-uuid",
#   "participants": ["Alice"]
# }

# 2. Присоединение к существующей комнате:
# Запрос:
# {
#   "uid": "existing-uuid",
#   "name": "Bob"
# }
# Ответ:
# {
#   "uid": "existing-uuid",
#   "participants": ["Alice", "Bob"]
# }

# 3. Получение информации о комнате:
# Запрос:
# GET /room/existing-uuid
# Ответ:
# {
#   "uid": "existing-uuid",
#   "participants": ["Alice", "Bob"]
# }

# 4. Получение информации обо всех комнатах:
# Запрос:
# GET /rooms
# Ответ:
# {
#   "existing-uuid": {
#     "uid": "existing-uuid",
#     "participants": ["Alice", "Bob"]
#   }
# }

# Этот код обеспечивает базовый функционал для создания и управления комнатами с помощью FastAPI,
# позволяя пользователям создавать комнаты, присоединяться к ним и получать информацию о комнатах.
