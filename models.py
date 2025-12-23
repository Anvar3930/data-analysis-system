from dataclasses import dataclass

@dataclass
class Record:
    id: int
    category: str
    value: int
    text: str
