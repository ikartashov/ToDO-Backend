import uvicorn

from pydantic_settings import BaseSettings
from fastapi import FastAPI
from resources import EntryManager, Entry
from pathlib import Path
from typing import ClassVar
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ToDo Backend",
              description="Бэк-энд списка дел")

origins = [
    "http://localhost:8000"  # адрес на котором запускаете бэк-энд
]

app.add_middleware(
    CORSMiddleware,
    allow_origins='https://wexler.io',  # Список разрешенных доменов
    allow_credentials=True,  # Разрешить Cookies и Headers
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все хедеры
)


class Settings(BaseSettings):
    # base_dir: ClassVar[Path] = Path(__file__).resolve().parent
    # data_folder: str = str(base_dir / "data")
    data_folder: str = "data"


settings = Settings()


@app.get('/api/get_data_folder/')
async def get_data_folder():
    return {'folder': settings.data_folder}


@app.get("/")
async def hello_world():
    """
    Здороваемся с Миром.
    """
    return {"Hello": "World"}


@app.get('/api/entries/')
async def get_entries():
    entry_manager = EntryManager(settings.data_folder)
    entry_manager.load()
    entries_list = []
    for entry in entry_manager.entries:
        entries_list.append(entry.json())
    return entries_list


@app.post('/api/save_entries/')
async def save_entries(data):
    entry_manager = EntryManager(settings.data_folder)
    for i in data:
        entry_manager.entries.append(Entry.from_json(i))
    entry_manager.save()
    return {'status': 'success'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
