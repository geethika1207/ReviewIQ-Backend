from sqlalchemy.orm import Session
from ..db import models
from ..schemas import chat
from ..core.security import get_current_user
from fastapi import HTTPException, status, APIRouter, Depends
from ..db.database import get_db
from ..services import chat_service

router = APIRouter()

def get_id(id:int, db:Session):
    submission = db.query(models.CodeSubmission).filter(models.CodeSubmission.id==id).first()
    
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    code = submission.code
    submission_user_id = submission.user_id

    return code, submission_user_id

def get_reviews_bugs(id:int, db:Session):
    submissions = db.query(models.CodeSubmission).filter(models.CodeSubmission.id==id).first()

    if not submissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    reviews = submissions.Reviews
    bugs = submissions.Reviews.bugs

    result = []
    for bug in bugs:
        result.append({
            "line_number": bug.Line_Number,
            "problem": bug.Problem,
            "severity": bug.Severity,
            "category": bug.Category,
            "fix": bug.Fix
        })

    return{
        "submission_id" :submissions.id,
        "language": submissions.language,
        "bugs" : result,
        "summary" : reviews.Summary,
        "positive_aspects" : reviews.Positive_aspects,
        "learning_tags" : reviews.Learning_tags,
        "suggestions" : reviews.Suggestions
    }


@router.post("/submission/{id}/chat")
def get_chat(id:int, user_question : chat.ChatRequest, db:Session=Depends(get_db), current_user = Depends(get_current_user)):

    code , submission_user_id = get_id(id,db)

    if submission_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    result = get_reviews_bugs(id,db)

    prompt = chat_service.get_prompt(code, result, user_question.question)
    response = chat_service.ask_groq(prompt)

    new_message = models.Message(
                submission_id = id,
                question = user_question.question,
                answer = response
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return response