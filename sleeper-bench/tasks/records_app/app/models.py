from dataclasses import dataclass


@dataclass
class Record:
    id: int
    owner_id: str
    title: str
    body: str
    status: str = "active"
    version: int = 1
