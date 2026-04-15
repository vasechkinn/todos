from fastapi import (FastAPI,
                     Path,
                     Query,
                     HTTPException,
                     status,
                     Request,
                     Form)
from typing import Annotated
from fastapi.responses import RedirectResponse # перенаправимся обратно в велком чтобы посмотреть онобления
from dict_todo import (TODOS,
                       ID,
                       Taska,
                       CreateTask,
                       ReplaceTask,
                       UpdateTask)
from dataclasses import dataclass, asdict
from fastapi.templating import Jinja2Templates

def create_dict(list_tasks: list[Taska]):
    return [asdict(task) for task in list_tasks]

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def welcome() -> dict:
    return {'hello': 'hello'}

@app.get('/welcome')
async def todos_page(request: Request):
    tasks = TODOS

    return templates.TemplateResponse(request,
        'index.html',
        {'tasks': tasks,
         'title': 'TODOS'}      
    )

@app.get('/todos')
async def get_todos(limit: Annotated[int | None, Query(ge=1)] = None,
                    is_completed: Annotated[bool | None, Query()] = None,
                    search: Annotated[str | None, Query(min_length=2)] = None):
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

@app.post('/todos')
async def create_task(task: CreateTask) -> dict:
    global ID

    new_task = Taska(
        id= ID,
        title=task.title,
        description= task.description,
        is_completed= task.is_completed
    )

    TODOS.append(new_task)
    ID +=1

    return {'new task': asdict(new_task)}

@app.put('/todos/{todo_id}')
async def replace_task(todo_id: Annotated[int, Path(ge=1)],
                       task: ReplaceTask):
    for task_r in TODOS:
        if task_r.id == todo_id:

            task_r.title=task.title
            task_r.description= task.description
            task_r.is_completed= task.is_completed
            
            return {'task': asdict(task_r)}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')

@app.patch('/todos/{todo_id}')
async def update_task(todo_id: Annotated[int, Path(ge=1)],
                       task: UpdateTask):
    for task_u in TODOS:
        if task_u.id == todo_id:
            if task.title is not None:
                task_u.title=task.title

            if task.description is not None:
                task_u.description= task.description
            
            if task.is_completed is not None:
                task_u.is_completed= task.is_completed
            
            return {'task': asdict(task_u)}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')

@app.delete('/todos/{todo_id}')
async def delete_task(todo_id: Annotated[int, Path(ge=1)]) -> dict:
    global ID

    for i, task in enumerate(TODOS):
        if task.id == todo_id:
            res = TODOS.pop(i)
            return {'del task': asdict(res)}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')

@app.post('/create_task')
async def create_task_form(title: str = Form(...),
                          description: str = Form('description'),
                          is_completed: bool = Form(False)):
    global ID

    new_task = Taska(
        id= ID,
        title=title,
        description= description,
        is_completed= is_completed
    )

    TODOS.append(new_task)
    ID +=1

    return RedirectResponse(url='/welcome', status_code=status.HTTP_303_SEE_OTHER)

@app.post('/delete_task')
async def delete_task_form(id: int = Form(...)):
    for i, task in enumerate(TODOS):
        if task.id == id:
            TODOS.pop(i)
            return RedirectResponse(url='/welcome', status_code=status.HTTP_303_SEE_OTHER)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')