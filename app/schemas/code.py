from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubmittedCode(BaseModel):
    program : str

class BugsResponse(BaseModel):
    Line_number : Optional[int] = None 
    Problem : Optional[str] = None
    Severity : Optional[str] = None
    Category : Optional[str] = None
    Fix : Optional[str] = None
    
    class Config:
        orm_mode = True


class CodeResponse(BaseModel):
    submission_id : int
    language : str
    bugs : list[BugsResponse] = []
    summary : str
    positive_aspects : Optional[list] = None
    learning_tags : Optional[list] = None
    suggestions : Optional[list] = None

    class Config:
        orm_mode = True 


class HistoryResponse(BaseModel):
    id : int
    code : str
    language : str
    created_at : datetime