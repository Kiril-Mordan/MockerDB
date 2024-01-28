from fastapi import FastAPI
from mocker_db import MockerDB
from conf.settings import MOCKER_SETUP_PARAMS

from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    text: str

app = FastAPI()
handler = MockerDB(**MOCKER_SETUP_PARAMS)

@app.get("/")
def read_root():
    return "Still alive!"

@app.post("/initialize")
def initialize_database():
    handler.establish_connection()
    return {"message": "Database initialized"}

@app.post("/insert")
def insert_data(values: List[Item]):
    values_list = [item.dict() for item in values]
    handler.insert_values(values_list, "text")
    return {"message": "Data inserted"}

@app.get("/retrieve")
def retrieve_data(subkey: str, subvalue: str, query: str):
    handler.filter_keys(subkey=subkey, subvalue=subvalue)
    handler.search_database_keys(query=query)
    results = handler.get_dict_results(return_keys_list=[query])
    return results
