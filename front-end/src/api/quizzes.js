import request from "@/utils/request";

const QUIZZES_API_URL = "/quizzes-api";

const STATUS = {
  notStarted: "NOT_STARTED",
  inProgress: "IN_PROGRESS",
  completed: "COMPLETED",
};

function normalizeQuiz(item = {}) {
  const questionsCount = Array.isArray(item.questions)
    ? item.questions.length
    : item.questions_count;

  return {
    id: item.id,
    title: item.title || "Без названия",
    discipline: item.discipline || item.subject || null,
    availabilityStart: item.available_from || item.start_at || null,
    availabilityEnd: item.available_to || item.deadline || null,
    status: item.status || STATUS.notStarted,
    questionsCount: Number.isFinite(questionsCount) ? questionsCount : null,
    timeLimitMinutes: item.time_limit_minutes || null,
    description: item.description || null,
  };
}

function applyFilters(quizzes, params = {}) {
  const search = (params.search || "").toLowerCase().trim();
  const discipline = (params.discipline || "").toLowerCase().trim();

  return quizzes.filter(quiz => {
    const matchByName = !search || quiz.title.toLowerCase().includes(search);
    const quizDiscipline = (quiz.discipline || "").toLowerCase();
    const matchByDiscipline = !discipline || quizDiscipline === discipline;

    return matchByName && matchByDiscipline;
  });
}

function mapAttemptResponse(data, quizId) {
  const attemptId = data?.attempt_id || data?.id || data?.attemptId;
  if (!attemptId) {
    throw new Error("attempt_not_provided");
  }

  return {
    attemptId,
    quizId,
    isStub: false,
  };
}

export async function getMyQuizAttempt(quizId) {
  try {
    const { data } = await request({
      url: `${QUIZZES_API_URL}/tests/${quizId}/attempts/me`,
      method: "get",
    });

    return {
      data: {
        attemptId: data?.attempt_id || null,
        startedAt: data?.started_at || null,
        completedAt: data?.completed_at || null,
        score: data && data.score !== undefined && data.score !== null ? data.score : null,
        maxScore: data && data.max_score !== undefined && data.max_score !== null ? data.max_score : null,
      },
    };
  } catch (error) {
    if (error?.response?.status === 404) {
      return { data: null };
    }
    throw error;
  }
}

export async function getStudentQuizzes(params = {}) {
  const { data } = await request({
    url: `${QUIZZES_API_URL}/tests`,
    method: "get",
  });

  const quizzes = Array.isArray(data) ? data.map(normalizeQuiz) : [];

  const quizzesWithStatus = await Promise.all(
    quizzes.map(async quiz => {
      try {
        const attemptResponse = await getMyQuizAttempt(quiz.id);
        const attempt = attemptResponse?.data;

        if (attempt && attempt.completedAt) {
          return {
            ...quiz,
            status: STATUS.completed,
          };
        }

        if (attempt && attempt.attemptId) {
          return {
            ...quiz,
            status: STATUS.inProgress,
          };
        }

        return {
          ...quiz,
          status: STATUS.notStarted,
        };
      } catch (error) {
        return quiz;
      }
    }),
  );

  return {
    data: applyFilters(quizzesWithStatus, params),
    isStub: false,
  };
}

export async function getQuizById(quizId) {
  const [testResponse, questionsResponse] = await Promise.all([
    request({
      url: `${QUIZZES_API_URL}/tests/${quizId}`,
      method: "get",
    }),
    request({
      url: `${QUIZZES_API_URL}/tests/${quizId}/questions`,
      method: "get",
    }),
  ]);

  const questions = Array.isArray(questionsResponse?.data) ? questionsResponse.data : [];

  return {
    data: normalizeQuiz({
      ...testResponse?.data,
      questions_count: questions.length,
    }),
    isStub: false,
  };
}

export async function startQuizAttempt(quizId) {
  const { data } = await request({
    url: `${QUIZZES_API_URL}/tests/${quizId}/attempts/start`,
    method: "post",
  });

  return mapAttemptResponse(data, quizId);
}

export async function getQuizQuestions(quizId) {
  const { data } = await request({
    url: `${QUIZZES_API_URL}/tests/${quizId}/questions`,
    method: "get",
  });

  return {
    data: Array.isArray(data) ? data : [],
  };
}

export async function submitQuizAnswers(quizId, attemptId, answers) {
  const { data } = await request({
    url: `${QUIZZES_API_URL}/tests/${quizId}/submit`,
    method: "post",
    data: {
      attempt_id: attemptId,
      answers,
    },
  });

  return {
    data,
  };
}

export const QUIZ_STATUS = STATUS;
