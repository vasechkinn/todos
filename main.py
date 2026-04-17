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
from utils import(search_task_by_id,
                  create_new_task,
                  delete_task_by_id)

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

@app.get('/todos/{task_id}')
async def get_todo_by_id(task_id: Annotated[int, Path(ge=1)]) -> dict:
    task = search_task_by_id(task_id)
    if task is not None:
        return {'task': asdict(task)}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')

@app.post('/todos')
async def create_task(task: CreateTask) -> dict:
    new_task = create_new_task(task.title, task.description, task.is_completed)

    return {'new task': asdict(new_task)}

@app.put('/todos/{task_id}')
async def replace_task(task_id: Annotated[int, Path(ge=1)],
                       task_rep: ReplaceTask):
    task = search_task_by_id(task_id)
    if task is not None:

        task.title=task_rep.title
        task.description= task_rep.description
        task.is_completed= task_rep.is_completed
            
        return {'task': asdict(task)}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')

@app.patch('/todos/{task_id}')
async def update_task(task_id: Annotated[int, Path(ge=1)],
                       task_upd: UpdateTask):
    task = search_task_by_id(task_id)

    if task is not None:
        if task_upd.title is not None:
            task.title=task_upd.title

        if task_upd.description is not None:
            task.description= task_upd.description
            
        if task_upd.is_completed is not None:
            task.is_completed= task_upd.is_completed
            
        return {'task': asdict(task)}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')

@app.delete('/todos/{task_id}')
async def delete_task(task_id: Annotated[int, Path(ge=1)]) -> dict:
    deleted  = delete_task_by_id(task_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')
    
    return {'del task': asdict(delete_task)}

@app.post('/create_task')
async def create_task_form(title: str = Form(...),
                          description: str = Form('description'),
                          is_completed: bool = Form(False)):
    desc = description if description else None
    create_new_task(title, desc, is_completed)
    return RedirectResponse(url='/welcome', status_code=status.HTTP_303_SEE_OTHER)

@app.post('/delete_task')
async def delete_task_form(id: int = Form(...)):
    deleted = delete_task_by_id(id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'task not found')
    
    return RedirectResponse(url='/welcome', status_code=status.HTTP_303_SEE_OTHER)
