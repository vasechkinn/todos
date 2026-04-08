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
async def get_todos(limit: Annotated[int | None, Query(ge=1)] = None, is_completed: Annotated[bool | None, Query()] = None, search: Annotated[str | None, Query(min_length=2)] = None):
    tasks = TODOS

    if search is not None:
        tasks = [task for task in tasks if search.lower() in task.title.lower()]

    if is_completed is not None:
        tasks = [task for task in tasks if task.is_completed == is_completed]
    
    if limit is not None and limit <= len(tasks):
        tasks = tasks[:limit]

    res = {'tasks': create_dict(tasks)}
    
    if not tasks:
        res['message'] = 'not found'
    
    return res

@app.get('/todos/{todo_id}')
async def get_todo_by_id(todo_id: Annotated[int, Path(ge=1)]) -> dict:
    for task in TODOS:
        if task.id == todo_id:
            return {'task': asdict(task)}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')