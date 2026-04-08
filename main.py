from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Annotated
from dict_todo import TODOS, ID, Taska
from dataclasses import dataclass, asdict

def create_dict(list_tasks: list[Taska]):
    return [asdict(task) for task in list_tasks]

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
    
    return {'tasks': create_dict(tasks)}

@app.get('/todos/{todo_id}')
async def get_todo_by_id(todo_id: Annotated[int, Path(ge=1)]) -> dict:
    for task in TODOS:
        if task.id == todo_id:
            return {'task': asdict(task)}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')