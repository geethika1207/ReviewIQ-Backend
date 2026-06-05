from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import models
from ..schemas import code
from ..core.security import get_current_user

router = APIRouter()

@router.get("/history/submission/{id}", response_model=code.CodeResponse)
def get_submission(id:int, db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    submitted_code = db.query(models.CodeSubmission).filter(models.CodeSubmission.user_id==current_user.id, models.CodeSubmission.id == id).first()
    
    if submitted_code is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data  not found")      
     
    my_review = submitted_code.Reviews
    some_bugs = submitted_code.Reviews.bugs
    return {
               "submission_id" : submitted_code.id,
               "language" : submitted_code.language,
               "bugs" : some_bugs,
               "summary" : my_review.Summary,
               "positive_aspects" : my_review.Positive_aspects,
               "learning_tags" : my_review.Learning_tags,
               "suggestions" : my_review.Suggestions 
    }

@router.get("/history")
def get_history(limit:int=10, offset:int = 0, db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    all_codes = db.query(models.CodeSubmission).filter(models.CodeSubmission.user_id==current_user.id).limit(limit).offset(offset)

    if all_codes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data  not found")

    result = []

    for submit_code in all_codes:
        if len(submit_code.code)>150:
            code_preview = submit_code.code[:151] + "..."
        else:
            code_preview = submit_code.code
        result.append({
            "id" : submit_code.id,
            "code" : code_preview,
            "language" : submit_code.language,
        }
        )
    return result

@router.delete("/history/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_code(id:int, db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    DeleteCode = db.query(models.CodeSubmission).filter(models.CodeSubmission.user_id==current_user.id, models.CodeSubmission.id == id).first()

    if DeleteCode is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    db.delete(DeleteCode)
    db.commit()