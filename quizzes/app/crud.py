from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

import models
import schemas


# ---------- TEST ----------

async def create_test(session: AsyncSession, data: schemas.TestCreate) -> models.Test:
    test = models.Test(title=data.title, description=data.description)
    session.add(test)
    await session.commit()
    await session.refresh(test)
    return test


async def get_test(session: AsyncSession, test_id: UUID) -> models.Test | None:
    stmt = (
        select(models.Test)
        .where(models.Test.id == test_id)
        .options(
            selectinload(models.Test.questions)
            .selectinload(models.Question.options)
        )
    )
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def list_tests(session: AsyncSession) -> list[models.Test]:
    stmt = select(models.Test).order_by(models.Test.id.desc())
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def update_test(session: AsyncSession, test: models.Test, data: schemas.TestUpdate) -> models.Test:
    if data.title is not None:
        test.title = data.title
    if data.description is not None:
        test.description = data.description
    await session.commit()
    await session.refresh(test)
    return test


async def delete_test(session: AsyncSession, test: models.Test) -> None:
    await session.delete(test)
    await session.commit()


# ---------- QUESTIONS ----------

async def list_questions_for_test(session: AsyncSession, test_id: UUID) -> list[models.Question]:
    stmt = (
        select(models.Question)
        .where(models.Question.test_id == test_id)
        .options(selectinload(models.Question.options))
        .order_by(models.Question.order)
    )
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def get_question(
    session: AsyncSession,
    test_id: UUID,
    question_id: UUID,
) -> models.Question | None:
    stmt = (
        select(models.Question)
        .where(
            models.Question.id == question_id,
            models.Question.test_id == test_id,
        )
        .options(selectinload(models.Question.options))
    )
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def create_question(
    session: AsyncSession,
    test: models.Test,
    data: schemas.QuestionCreate,
) -> models.Question:
    question = models.Question(
        test_id=test.id,
        text=data.text,
        order=data.order,
        type=models.QuestionType(data.type),
        correct_number=data.correct_number,
    )

    if data.type in (schemas.QuestionType.single, schemas.QuestionType.multiple):
        for opt in data.options:
            question.options.append(
                models.Option(text=opt.text, is_correct=opt.is_correct)
            )

    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


async def update_question(
    session: AsyncSession,
    question: models.Question,
    data: schemas.QuestionUpdate,
) -> models.Question:
    # для простоты: при изменении type/options лучше пересоздавать вопрос,
    # но покажу базовый апдейт

    if data.text is not None:
        question.text = data.text
    if data.order is not None:
        question.order = data.order
    if data.type is not None:
        question.type = models.QuestionType(data.type)
    if data.correct_number is not None or data.type == schemas.QuestionType.numeric:
        question.correct_number = data.correct_number

    # если пришёл options — пересоздадим варианты
    if data.options is not None:
        # очистим старые варианты
        for opt in list(question.options):
            await session.delete(opt)
        question.options.clear()

        if data.type in (schemas.QuestionType.single, schemas.QuestionType.multiple):
            for opt in data.options:
                question.options.append(
                    models.Option(text=opt.text, is_correct=opt.is_correct)
                )

    await session.commit()
    await session.refresh(question)
    return question


async def delete_question(session: AsyncSession, question: models.Question) -> None:
    await session.delete(question)
    await session.commit()