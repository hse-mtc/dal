from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    DateTime,
    Integer,
    UniqueConstraint,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from utils import utcnow


class QuestionType(StrEnum):
    single = "single"
    multiple = "multiple"
    numeric = "numeric"


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    questions: Mapped[list["Question"]] = relationship(
        back_populates="test",
        cascade="all, delete-orphan",
        order_by="Question.order",
    )


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        UniqueConstraint("test_id", "order", name="uq_questions_test_order"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType, name="question_type", native_enum=False),
        nullable=False,
    )

    # Для numeric-вопросов
    correct_number: Mapped[float | None]

    test: Mapped["Test"] = relationship(back_populates="questions")
    options: Mapped[list["Option"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )


class Option(Base):
    __tablename__ = "options"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(default=False)

    question: Mapped["Question"] = relationship(back_populates="options")


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id", ondelete="CASCADE"))
    user_id: Mapped[UUID]

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    score: Mapped[int | None]
    max_score: Mapped[int | None]

    answers: Mapped[list["AttemptAnswer"]] = relationship(
        back_populates="attempt",
        cascade="all, delete-orphan",
    )


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    attempt_id: Mapped[UUID] = mapped_column(ForeignKey("attempts.id", ondelete="CASCADE"))
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))

    # Для single/multiple
    option_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("options.id", ondelete="CASCADE")
    )

    # Для numeric
    numeric_answer: Mapped[float | None]

    is_correct: Mapped[bool] = mapped_column(default=False)

    attempt: Mapped["Attempt"] = relationship(back_populates="answers")
