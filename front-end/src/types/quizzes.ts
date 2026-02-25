export type QuizStatus = "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED";

export interface QuizDto {
  id: string;
  title: string;
  discipline: string | null;
  availabilityStart: string | null;
  availabilityEnd: string | null;
  status: QuizStatus;
  questionsCount: number | null;
  timeLimitMinutes: number | null;
  description?: string | null;
}

export interface StartAttemptResultDto {
  attemptId: string;
  quizId: string;
  isStub: boolean;
}
