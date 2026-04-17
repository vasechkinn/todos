from dict_todo import (TODOS,
                       ID,
                       Taska,
                       CreateTask,
                       ReplaceTask,
                       UpdateTask)
from typing import Optional

def search_task_by_id(task_id):
    for task in TODOS:
        if task.id == task_id:
            return task
        
def create_new_task(title: str,
                    description: str | None,
                    is_completed: bool) -> Optional[Taska]:
    global ID
    new_task = Taska(id=ID, title=title, description=description, is_completed=is_completed)
    TODOS.append(new_task)
    ID += 1
    return new_task

def delete_task_by_id(task_id: int) -> Optional[Taska]:
    for i, task in enumerate(TODOS):
        if task.id == task_id:
            return TODOS.pop(i)
    return None