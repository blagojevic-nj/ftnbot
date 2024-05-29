from dataclasses import dataclass
from typing import List

@dataclass
class ResponseDTO:
    question: str
    answer: str
    contexts: List[str]

@dataclass
class ResultDTO:
    id: str
    context: str
    score: str
