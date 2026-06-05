from sqlalchemy import Column, String, INTEGER, ForeignKey, JSON
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class USER(Base):
    __tablename__ = "Users"

    id = Column(INTEGER, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

class CodeSubmission(Base):
    __tablename__ = "Codes"

    id = Column(INTEGER, primary_key = True)
    code = Column(String, unique = False, nullable = False)
    language = Column(String, nullable=True)
    user_id = Column(INTEGER, ForeignKey("Users.id", ondelete = "CASCADE"), nullable = False)  
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    Reviews = relationship("Review", uselist=False, back_populates="submission", cascade="all, delete-orphan")
class Review(Base):
    __tablename__ = "reviews"

    id = Column(INTEGER, primary_key=True)
    Summary = Column(String, nullable=True)
    Positive_aspects = Column(JSON, nullable=True)
    Learning_tags = Column(JSON, nullable=True)
    Suggestions = Column(JSON, nullable=True)
    submission_id = Column(INTEGER, ForeignKey("Codes.id", ondelete="CASCADE"), nullable=False)
    
    submission = relationship("CodeSubmission", back_populates="Reviews")
    bugs = relationship("Bugs", back_populates="review", cascade="all, delete-orphan")

class Bugs(Base):
    __tablename__ = "errors"

    id = Column(INTEGER, primary_key = True)
    Line_Number = Column(INTEGER, unique = False, nullable = True)
    Problem = Column(String, unique = False, nullable = True)
    Severity = Column(String, unique = False, nullable = True)
    Category = Column(String, unique = False, nullable = True)
    Fix = Column(String, unique = False, nullable = True)
    review_id = Column(INTEGER, ForeignKey("reviews.id", ondelete = "CASCADE"), nullable = False)  
    review = relationship("Review", back_populates="bugs")
