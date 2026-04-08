from fastapi import FastAPI, Path, Query
from typing import Annotated
from dict_todo import TODOS, ID, Taska
from dataclasses import dataclass, asdict


app = FastAPI()

@app.get('/')
async def welcome() -> dict:
    return {'hello': 'hello'}

@app.get('/todos')
async def get_todos(limit: Annotated[int | None, Query(ge=1)] = None, is_completed: Annotated[bool | None, Query()] = None):
    tasks = TODOS
    
    if is_completed is not None:
        tasks = [task for task in tasks if task.is_completed == is_completed]
    
    if limit is not None and limit <= len(tasks):
        tasks = tasks[:limit]
    
    return {'tasks': [asdict(task) for task in tasks]}