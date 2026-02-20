from fastapi import APIRouter
from app.services.question_generator import generate_questions
from app.services.answer_evaluator import evaluate_answer
from app.database import SessionLocal
from app.models import InterviewAttempt
import re

router = APIRouter(prefix="/interview")


@router.get("/questions")
def get_questions(role: str, difficulty: str):
    questions = generate_questions(role, difficulty)
    return {"questions": questions}


@router.post("/evaluate")
def evaluate_interview(data: dict):

    role = data.get("role")
    difficulty = data.get("difficulty")
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return {"feedback": "Question and answer required."}

    feedback = evaluate_answer(question, answer)

    # Extract score (works for both "4/10" and "Score out of 10: 4")
    match = re.search(r'(\d+)\s*(?:\/10|out of 10)', feedback)
    score = int(match.group(1)) if match else 0

    # Save to database
    db = SessionLocal()
    attempt = InterviewAttempt(
        role=role,
        difficulty=difficulty,
        score=score,
        feedback=feedback
    )
    db.add(attempt)
    db.commit()
    db.close()

    return {
        "feedback": feedback,
        "score": score
    }


@router.get("/analytics")
def analytics():
    db = SessionLocal()
    attempts = db.query(InterviewAttempt).all()

    total = len(attempts)
    avg_score = (
        sum(a.score for a in attempts) / total
        if total > 0 else 0
    )

    history = [
        {
            "role": a.role,
            "difficulty": a.difficulty,
            "score": a.score
        }
        for a in attempts
    ]

    db.close()

    return {
        "total_attempts": total,
        "average_score": round(avg_score, 2),
        "history": history
    }
@router.get("/analytics")
def get_analytics():
    db = SessionLocal()

    attempts = db.query(InterviewAttempt).all()

    total_attempts = len(attempts)

    average_score = (
        sum(a.score for a in attempts) / total_attempts
        if total_attempts > 0 else 0
    )

    history = [
        {
            "role": a.role,
            "difficulty": a.difficulty,
            "score": a.score
        }
        for a in attempts
    ]

    db.close()

    return {
        "total_attempts": total_attempts,
        "average_score": round(average_score, 2),
        "history": history
    }