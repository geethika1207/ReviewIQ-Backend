from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db.database import get_db
from ..core.security import get_current_user
from ..db import models

router = APIRouter()

@router.get("/language")
def get_language(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    languages = db.query(models.CodeSubmission.language, func.count(models.CodeSubmission.id)).filter(models.CodeSubmission.user_id==current_user.id).group_by(models.CodeSubmission.language).all()

    if not languages:
        return []
    
    results = []
    for language in languages:
        results.append({
            "language": language[0],
            "count": language[1]
        })    
    return results 


@router.get("/stats")
def get_stats(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    total_reviews = db.query(func.count(models.Review.id)).join(models.CodeSubmission, models.Review.submission_id==models.CodeSubmission.id).filter(models.CodeSubmission.user_id==current_user.id).scalar()
    total_bugs = db.query(func.count(models.Bugs.id)).join(models.Review, models.Bugs.review_id==models.Review.id).join(models.CodeSubmission, models.Review.submission_id==models.CodeSubmission.id).filter(models.CodeSubmission.user_id==current_user.id).scalar()
    critical_bugs = db.query(func.count(models.Bugs.id)).join(models.Review, models.Bugs.review_id==models.Review.id).join(models.CodeSubmission, models.Review.submission_id==models.CodeSubmission.id).filter(models.Bugs.Severity=="CRITICAL" , models.CodeSubmission.user_id==current_user.id).scalar()   
    major_bugs = db.query(func.count(models.Bugs.id)).join(models.Review, models.Bugs.review_id==models.Review.id).join(models.CodeSubmission, models.Review.submission_id==models.CodeSubmission.id).filter(models.Bugs.Severity=="MAJOR" , models.CodeSubmission.user_id==current_user.id).scalar()   
    languages_used = db.query(func.count(models.CodeSubmission.language.distinct())).filter(models.CodeSubmission.user_id==current_user.id).scalar()                       

    return{
                "Total_Reviews" : total_reviews,
                "Total_Bugs" : total_bugs,
                "Critical_Bugs" : critical_bugs,
                "Major_Bugs" : major_bugs,
                "Languages_Used" : languages_used
    }

@router.get("/category")
def get_category(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    categorical_bugs = db.query(models.Bugs.Category, func.count(models.Bugs.id)).join(models.Review, models.Bugs.review_id==models.Review.id).join(models.CodeSubmission, models.Review.submission_id==models.CodeSubmission.id).filter(models.CodeSubmission.user_id==current_user.id).group_by(models.Bugs.Category)

    result = []
    for category in categorical_bugs:
        result.append({
                            "Category" : category[0],
                            "Count" : category[1]
        })
    return result


@router.get("/severity")
def get_severity(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    sevirity_bugs = db.query(models.Bugs.Severity, func.count(models.Bugs.id)).join(models.Review, models.Bugs.review_id==models.Review.id).join(models.CodeSubmission, models.Review.submission_id==models.CodeSubmission.id).filter(models.CodeSubmission.user_id==current_user.id).group_by(models.Bugs.Severity)

    result = []
    for sevirity in sevirity_bugs:
        result.append({
                            "Sevirity" : sevirity[0],
                            "Count" : sevirity[1]
        })
    return result


@router.get("/recent")
def get_recent(db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    recent_submissions = db.query(models.CodeSubmission).filter(models.CodeSubmission.user_id==current_user.id).order_by(models.CodeSubmission.id.desc()).limit(5).all()

    if not recent_submissions:
        return []
    
    result = []
    for submission in recent_submissions:
        if len(submission.code)>150:
            code_preview = submission.code[:151]+ "..."
        else:
            code_preview = submission.code
        result.append({
                            "id" : submission.id,
                            "code" : code_preview,
                            "language" : submission.language,
       })
    return result