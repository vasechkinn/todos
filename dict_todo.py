from dataclasses import dataclass, asdict

TODOS = [

]

@dataclass
class Taska:
    id: int
    title: str
    description: str | None
    is_completed: bool

ID = 1