from pydantic import BaseModel
from typing import List, Optional

class ResponseModel(BaseModel):
    question: Optional[str]
    modified_question: Optional[List[str]]
    answer: Optional[List[str]]
    sources: Optional[List[List[str]]]
