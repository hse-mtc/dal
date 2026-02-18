from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator
from uuid import UUID


class QuestionType(str, Enum):
    single = "single"
    multiple = "multiple"
    numeric = "numeric"


class TestCreate(BaseModel):
    title: str
    description: str | None = None


class TestOut(BaseModel):
    id: UUID
    title: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class TestUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class OptionCreate(BaseModel):
    text: str
    is_correct: bool = False


class OptionOut(BaseModel):
    id: UUID
    text: str

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    text: str
    order: int = Field(ge=1)
    type: QuestionType
    options: list[OptionCreate] = []
    correct_number: float | None = None

    @model_validator(mode='before')
    def validate_by_type(cls, values: dict):
        q_type: QuestionType = values.get("type")
        options: list[OptionCreate] = values.get("options") or []
        correct_number = values.get("correct_number")

        if q_type in (QuestionType.single, QuestionType.multiple):
            if correct_number is not None:
                raise ValueError("correct_number must be null for non-numeric questions")
            if len(options) < 2:
                raise ValueError("At least 2 options required for choice questions")
            correct_opts = [o for o in options if o.is_correct]
            if not correct_opts:
                raise ValueError("At least one correct option required")
            if q_type == QuestionType.single and len(correct_opts) != 1:
                raise ValueError("Exactly one correct option required for 'single' questions")

        elif q_type == QuestionType.numeric:
            if options:
                raise ValueError("Options must be empty for numeric questions")
            if correct_number is None:
                raise ValueError("correct_number is required for numeric questions")

        return values


class QuestionUpdate(BaseModel):
    text: str | None = None
    order: int | None = Field(default=None, ge=1)
    type: QuestionType | None = None
    options: list[OptionCreate] | None = None
    correct_number: float | None = None


class QuestionOut(BaseModel):
    id: UUID
    text: str
    order: int
    type: QuestionType
    options: list[OptionOut]
    correct_number: float | None

    class Config:
        from_attributes = True


class SubmitAnswer(BaseModel):
    question_id: UUID
    option_ids: list[int] | None = None
    numeric_answer: float | None = None

    @model_validator(mode='before')
    def check_fields(cls, values: dict):
        option_ids = values.get("option_ids")
        numeric_answer = values.get("numeric_answer")

        if option_ids is None and numeric_answer is None:
            raise ValueError("Either option_ids or numeric_answer must be provided")
        if option_ids is not None and numeric_answer is not None:
            raise ValueError("Provide either option_ids or numeric_answer, not both")
        return values


class SubmitRequest(BaseModel):
    answers: list[SubmitAnswer]


class SubmitResult(BaseModel):
    attempt_id: UUID
    score: int
    max_score: int
    completed_at: datetime
