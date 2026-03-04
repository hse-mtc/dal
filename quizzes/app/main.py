from datetime import datetime
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

import schemas
import models
import crud
from settings import settings
from db import get_session
from auth import get_principal, require_permission, Principal

app = FastAPI(title="Tests Service")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# ---------- TEST CRUD ----------

@app.post("/tests", response_model=schemas.TestOut)
async def create_test(
    payload: schemas.TestCreate,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(require_permission("marks.post.milfaculty")),
):
    return await crud.create_test(session, payload)


@app.get("/tests", response_model=list[schemas.TestOut])
async def list_tests(
    session: AsyncSession = Depends(get_session),
):
    tests = await crud.list_tests(session)
    return tests


@app.get("/tests/{test_id}", response_model=schemas.TestOut)
async def get_test(
    test_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    test = await crud.get_test(session, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@app.patch("/tests/{test_id}", response_model=schemas.TestOut)
async def update_test(
    test_id: UUID,
    payload: schemas.TestUpdate,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(require_permission("marks.post.milfaculty")),
):
    test = await crud.get_test(session, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return await crud.update_test(session, test, payload)


@app.delete("/tests/{test_id}")
async def delete_test(
    test_id: UUID,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(require_permission("marks.post.milfaculty")),
):
    test = await crud.get_test(session, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    await crud.delete_test(session, test)
    return {"status": "ok"}


# ---------- QUESTION CRUD (привязаны к test_id) ----------

@app.get(
    "/tests/{test_id}/questions",
    response_model=list[schemas.QuestionOut],
)
async def list_questions(
    test_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    # проверим, что тест существует
    test = await crud.get_test(session, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = await crud.list_questions_for_test(session, test_id)
    return questions


@app.post(
    "/tests/{test_id}/questions",
    response_model=schemas.QuestionOut,
)
async def create_question(
    test_id: UUID,
    payload: schemas.QuestionCreate,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(require_permission("marks.post.milfaculty")),
):
    test = await crud.get_test(session, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    question = await crud.create_question(session, test, payload)
    return question


@app.get(
    "/tests/{test_id}/questions/{question_id}",
    response_model=schemas.QuestionOut,
)
async def get_question(
    test_id: UUID,
    question_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    question = await crud.get_question(session, test_id, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@app.patch(
    "/tests/{test_id}/questions/{question_id}",
    response_model=schemas.QuestionOut,
)
async def update_question(
    test_id: UUID,
    question_id: UUID,
    payload: schemas.QuestionUpdate,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(require_permission("marks.post.milfaculty")),
):
    question = await crud.get_question(session, test_id, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question = await crud.update_question(session, question, payload)
    return question


@app.delete("/tests/{test_id}/questions/{question_id}")
async def delete_question(
    test_id: UUID,
    question_id: UUID,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(require_permission("marks.post.milfaculty")),
):
    question = await crud.get_question(session, test_id, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    await crud.delete_question(session, question)
    return {"status": "ok"}


@app.post("/tests/{test_id}/attempts/start", response_model=schemas.AttemptStartResult)
async def start_attempt(
    test_id: UUID,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(get_principal),
):
    test = await crud.get_test(session, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    attempt = await crud.create_attempt(session, test_id=test_id, user_id=principal.user_id)

    return schemas.AttemptStartResult(
        attempt_id=attempt.id,
        started_at=attempt.started_at,
    )


@app.get("/tests/{test_id}/attempts/me", response_model=schemas.AttemptOut)
async def get_my_attempt(
    test_id: UUID,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(get_principal),
):
    test = await crud.get_test(session, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    attempt = await crud.get_attempt_by_test_and_user(
        session,
        test_id=test_id,
        user_id=principal.user_id,
    )
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    return schemas.AttemptOut(
        attempt_id=attempt.id,
        started_at=attempt.started_at,
        completed_at=attempt.completed_at,
        score=attempt.score,
        max_score=attempt.max_score,
    )


# ---------- ПРОХОЖДЕНИЕ ТЕСТА (submit) ----------

@app.post("/tests/{test_id}/submit", response_model=schemas.SubmitResult)
async def submit_test(
    test_id: UUID,
    payload: schemas.SubmitRequest,
    session: AsyncSession = Depends(get_session),
    principal: Principal = Depends(get_principal),
):
    test = await crud.get_test(session, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    # Индексы
    question_map: dict[int, models.Question] = {q.id: q for q in test.questions}
    option_to_question: dict[int, int] = {}
    correct_options_by_question: dict[int, set[int]] = {}

    for q in test.questions:
        correct_set: set[int] = set()
        for opt in q.options:
            option_to_question[opt.id] = q.id
            if opt.is_correct:
                correct_set.add(opt.id)
        if correct_set:
            correct_options_by_question[q.id] = correct_set

    answers_by_question: dict[int, schemas.SubmitAnswer] = {}
    for ans in payload.answers:
        if ans.question_id in answers_by_question:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate answer for question {ans.question_id}",
            )
        if ans.question_id not in question_map:
            raise HTTPException(
                status_code=400,
                detail=f"Question {ans.question_id} not in this test",
            )
        answers_by_question[ans.question_id] = ans

    if not answers_by_question:
        raise HTTPException(
            status_code=400,
            detail="No answers provided",
        )

    attempt = None
    if payload.attempt_id is not None:
        attempt_stmt = select(models.Attempt).where(
            models.Attempt.id == payload.attempt_id,
            models.Attempt.test_id == test_id,
            models.Attempt.user_id == principal.user_id,
        )
        attempt_result = await session.execute(attempt_stmt)
        attempt = attempt_result.scalar_one_or_none()

        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
    else:
        attempt = await crud.get_attempt_by_test_and_user(
            session,
            test_id=test_id,
            user_id=principal.user_id,
        )
        if attempt is None:
            attempt = models.Attempt(test_id=test_id, user_id=principal.user_id)
            session.add(attempt)
            await session.flush()

    if attempt.completed_at is not None:
        raise HTTPException(status_code=400, detail="Attempt already completed")

    await session.execute(
        delete(models.AttemptAnswer).where(models.AttemptAnswer.attempt_id == attempt.id)
    )
    await session.flush()

    score = 0
    max_score = len(test.questions)

    for q in test.questions:
        ans = answers_by_question.get(q.id)
        if not ans:
            continue

        q_type = q.type
        is_correct = False

        if q_type in (models.QuestionType.single, models.QuestionType.multiple):
            option_ids = ans.option_ids
            if not option_ids:
                raise HTTPException(
                    status_code=400,
                    detail=f"option_ids required for question {q.id}",
                )

            selected_set = set(option_ids)
            for oid in selected_set:
                qid = option_to_question.get(oid)
                if qid is None or qid != q.id:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Option {oid} does not belong to question {q.id}",
                    )

            correct_set = correct_options_by_question.get(q.id, set())

            if q_type == models.QuestionType.single:
                if len(selected_set) != 1:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Exactly one option must be selected for question {q.id}",
                    )
                is_correct = selected_set == correct_set
            else:
                is_correct = bool(selected_set) and selected_set.issubset(correct_set)

            for oid in selected_set:
                session.add(
                    models.AttemptAnswer(
                        attempt_id=attempt.id,
                        question_id=q.id,
                        option_id=oid,
                        numeric_answer=None,
                        is_correct=is_correct,
                    )
                )

        elif q_type == models.QuestionType.numeric:
            if ans.numeric_answer is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"numeric_answer required for numeric question {q.id}",
                )
            if q.correct_number is None:
                raise HTTPException(
                    status_code=500,
                    detail=f"No correct_number configured for numeric question {q.id}",
                )

            is_correct = (ans.numeric_answer == q.correct_number)

            session.add(
                models.AttemptAnswer(
                    attempt_id=attempt.id,
                    question_id=q.id,
                    option_id=None,
                    numeric_answer=ans.numeric_answer,
                    is_correct=is_correct,
                )
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Unsupported question type for question {q.id}",
            )

        if is_correct:
            score += 1

    attempt.score = score
    attempt.max_score = max_score
    attempt.completed_at = datetime.utcnow()

    await session.commit()
    await session.refresh(attempt)

    return schemas.SubmitResult(
        attempt_id=attempt.id,
        score=attempt.score or 0,
        max_score=attempt.max_score or 0,
        completed_at=attempt.completed_at or datetime.utcnow(),
    )


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.quizzes_host,
        port=settings.quizzes_port,
    )
