from dataclasses import dataclass, asdict
from pydantic import BaseModel
TODOS = [

]

class CreateTask(BaseModel):
    title: str
    description: str | None
    is_completed: bool = False

class ReplaceTask(BaseModel):
    title: str
    description: str | None
    is_completed: bool

class UpdateTask(BaseModel):
    title: str | None= None
    description: str | None = None
    is_completed: bool | None = None

@dataclass
class Taska:
    id: int
    title: str
    description: str | None
    is_completed: bool

ID = 1