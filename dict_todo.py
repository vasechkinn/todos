from dataclasses import dataclass, asdict
from pydantic import BaseModel
TODOS = [

]

class CreateTask(BaseModel):
    title: str
    description: str | None
    is_completed: bool = False

@dataclass
class Taska:
    id: int
    title: str
    description: str | None
    is_completed: bool

ID = 1