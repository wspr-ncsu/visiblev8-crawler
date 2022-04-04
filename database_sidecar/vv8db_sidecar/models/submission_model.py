from pydantic import BaseModel
from pydantic.dataclasses import dataclass

@dataclass
class SubmissionModel:
    url: str
