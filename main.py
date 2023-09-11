from fastapi import FastAPI, HTTPException, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from peewee import DoesNotExist
from pydantic import BaseModel
from typing import List, Dict, Union
import models
from database import db
from peewee import IntegrityError

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/questions/")
async def create_questions(question: QuestionBase):
    try:
        with db.atomic():
            db_question = models.Questions.create(question_text=question.question_text)
            for choice in question.choices:
                models.Choices.create(
                    choice_text=choice.choice_text,
                    is_correct=choice.is_correct,
                    question=db_question
                )
                db.commit()  # Commit inside the 'with db.atomic()' block
        return {"message": "Question and choices added successfully!"}
    except IntegrityError as e:
        # Log the exception and handle it appropriately
        print("Database error:", str(e))
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/questions/{question_id}")
async def read_question(question_id: int):
    try:
        result = models.Questions.get(models.Questions.id == question_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail='Question is not found')
    return result

@app.get("/choices/{question_id}")
async def read_choices(question_id: int):
    result = models.Choices.select().where(models.Choices.question_id == question_id)
    if not result:
        raise HTTPException(status_code=404, detail='Choices not found')
    return list(result)


@app.get("/all_questions/", response_class=HTMLResponse)
async def get_all_questions(request: Request):
    questions = models.Questions.select()
    question_choices = {}
    for question in questions:
        choices = models.Choices.select().where(models.Choices.question_id == question.id)
        question_choices[question] = choices
    return templates.TemplateResponse("all_questions.html", {"request": request, "questions": question_choices})