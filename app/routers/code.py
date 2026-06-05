from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import session
from ..db.database import get_db
from ..db import models
from ..schemas import code
from ..core.security import get_current_user
from ..services import ai_service
import json

router = APIRouter()

@router.post("/Code", status_code=status.HTTP_201_CREATED)
def submit_code(UserCode : code.SubmittedCode, db:session = Depends(get_db), current_user = Depends(get_current_user)):
    prompt = ai_service.create_prompt(UserCode.program)
    response = ai_service.ask_groq(prompt)
    print("GROQ RESPONSE:", response)  
    result = json.loads(response)
    print("JSON PARSED:", result)  
    print("TYPE:", type(result))   

    error = result.get("error")
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    Language = result.get("language", None)
    Line_Number = result.get("line_number",None)
    Bug = result.get("bugs", [])
    Summary = result.get("summary", None)
    Positive_Aspects = result.get("positive_aspects", [])
    Learning_tags = result.get("learning_tags", [])
    Suggestions = result.get("suggestions", [])


    try:
        # 1. Save Submission
        db_submission = models.CodeSubmission(
            user_id=current_user.id,
            code=UserCode.program,
            language=Language
        )
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)

        # 2. Save Review
        db_review = models.Review(
            submission_id=db_submission.id,
            Summary=Summary,
            Positive_aspects=Positive_Aspects,
            Learning_tags=Learning_tags,
            Suggestions=Suggestions
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)

        # 3. Save Bugs
        for bug in Bug:
            db_bug = models.Bugs(
                review_id=db_review.id,
                Line_Number=bug.get("line_number"),
                Problem=bug.get("problem"),
                Severity=bug.get("severity"),
                Category=bug.get("category"),
                Fix=bug.get("fix")
            )
            db.add(db_bug)
        db.commit()

        # 4. Return response
        return {
            "submission_id": db_submission.id,
            "language": Language,
            "bugs": Bug,
            "summary": Summary,
            "positive_aspects": Positive_Aspects,
            "learning_tags": Learning_tags,
            "suggestions": Suggestions
        }    
    except Exception as e:
        import traceback
        traceback.print_exc()    #traceback.print_exc() will force the full error into  terminal
        raise HTTPException(status_code=500, detail=str(e)) 