from pydantic import BaseModel
from app.utils.enums import PerformanceTypes, SearchTypes

class QuestionInput(BaseModel):
    question: str
    performance: PerformanceTypes = PerformanceTypes.fast
    searchType: SearchTypes = SearchTypes.youtube
