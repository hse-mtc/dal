<template>
  <div class="app-container">
    <el-row>
      <el-col :span="20" :offset="2">
        <PageHeader :title="quizTitle" />

        <template>
          <el-button class="back-button" type="text" @click="goBack">
            Вернуться к списку
          </el-button>

          <el-alert
            v-if="errorMessage"
            type="error"
            :closable="false"
            show-icon
            :title="errorMessage"
            class="alert"
          />

          <el-alert
            v-if="completedMessage"
            type="warning"
            :closable="false"
            show-icon
            :title="completedMessage"
            class="alert"
          />

          <el-card v-loading="loading" shadow="never" class="quiz-card">
            <div class="quiz-row">
              <span class="quiz-label">Описание:</span>
              <span>{{ quiz.description || "—" }}</span>
            </div>
            <div class="quiz-row">
              <span class="quiz-label">Время на прохождение:</span>
              <span>{{ quiz.timeLimitMinutes ? `${quiz.timeLimitMinutes} мин.` : "Не ограничено" }}</span>
            </div>
            <div class="quiz-row">
              <span class="quiz-label">Количество вопросов:</span>
              <span>{{ questionsCountLabel }}</span>
            </div>
            <div class="quiz-row">
              <span class="quiz-label">Статус:</span>
              <span>{{ statusLabel(quiz.status) }}</span>
            </div>
            <div class="quiz-row">
              <span class="quiz-label">Полученный балл:</span>
              <span>{{ scoreLabel }}</span>
            </div>

            <el-button
              type="primary"
              :loading="isStarting"
              :disabled="isCompletedAttempt"
              @click="startAttempt"
            >
              {{ quiz.status === QUIZ_STATUS.inProgress ? "Продолжить" : "Начать попытку" }}
            </el-button>
          </el-card>
        </template>
      </el-col>
    </el-row>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import PageHeader from "@/common/PageHeader";
import {
  getQuizById,
  getMyQuizAttempt,
  startQuizAttempt,
  QUIZ_STATUS,
} from "@/api/quizzes";

export default {
  name: "QuizDetailsPage",
  components: {
    PageHeader,
  },
  data() {
    return {
      loading: false,
      isStarting: false,
      errorMessage: "",
      completedMessage: "",
      isCompletedAttempt: false,
      attemptScore: null,
      attemptMaxScore: null,
      quiz: {
        id: "",
        title: "Квиз",
        discipline: null,
        timeLimitMinutes: null,
        questionsCount: null,
        status: QUIZ_STATUS.notStarted,
      },
      QUIZ_STATUS,
    };
  },
  computed: {
    quizId() {
      return this.$route.params.quizId;
    },
    quizTitle() {
      return this.quiz.title || "Прохождение квизов";
    },
    questionsCountLabel() {
      return this.quiz.questionsCount !== null && this.quiz.questionsCount !== undefined
        ? this.quiz.questionsCount
        : "—";
    },
    scoreLabel() {
      if (!this.isCompletedAttempt) {
        return "-";
      }

      const score = this.attemptScore !== null && this.attemptScore !== undefined
        ? this.attemptScore
        : 0;
      const maxScore = this.attemptMaxScore !== null && this.attemptMaxScore !== undefined
        ? this.attemptMaxScore
        : (this.quiz.questionsCount || 0);

      return `${score} из ${maxScore}`;
    },
  },
  created() {
    this.fetchQuiz();
  },
  methods: {
    async fetchQuiz() {
      this.loading = true;
      this.errorMessage = "";
      this.completedMessage = "";
      this.isCompletedAttempt = false;
      this.attemptScore = null;
      this.attemptMaxScore = null;

      try {
        const [quizResponse, attemptResponse] = await Promise.all([
          getQuizById(this.quizId),
          getMyQuizAttempt(this.quizId),
        ]);

        this.quiz = { ...this.quiz, ...quizResponse.data };

        const attempt = attemptResponse?.data;
        if (attempt && attempt.completedAt) {
          this.isCompletedAttempt = true;
          this.quiz.status = QUIZ_STATUS.completed;
          this.attemptScore = attempt.score;
          this.attemptMaxScore = attempt.maxScore;
          this.completedMessage = "Вы уже отправили ответы на этот квиз";
        } else if (attempt && attempt.attemptId) {
          this.quiz.status = QUIZ_STATUS.inProgress;
        }
      } catch (error) {
        this.errorMessage = "Не удалось загрузить информацию о квизе";
      } finally {
        this.loading = false;
      }
    },
    async startAttempt() {
      if (this.isCompletedAttempt) {
        this.errorMessage = "Вы уже отправили ответы на этот квиз";
        return;
      }

      this.isStarting = true;
      this.errorMessage = "";

      try {
        const attempt = await startQuizAttempt(this.quizId);

        this.$router.push(`/discipline-control/quizzes/${this.quizId}/attempt/${attempt.attemptId}/`);
      } catch (error) {
        this.errorMessage = "Не удалось начать попытку";
      } finally {
        this.isStarting = false;
      }
    },
    goBack() {
      this.$router.push("/discipline-control/quizzes/");
    },
    statusLabel(status) {
      if (status === QUIZ_STATUS.inProgress) {
        return "В процессе";
      }
      if (status === QUIZ_STATUS.completed) {
        return "Сдан";
      }
      return "Не начат";
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.back-button {
  margin-bottom: $m;
}

.alert {
  margin-bottom: $m;
}

.quiz-card {
  margin-bottom: $l;
}

.quiz-row {
  display: flex;
  gap: $s;
  margin-bottom: $m;
}

.quiz-label {
  min-width: 220px;
  font-family: $nova-bold;
}

.state-wrapper {
  margin-top: $xxl;
}

.empty-state {
  color: $gray;
  background: $white;
  border: 1px solid $lightGray;
  border-radius: 8px;
  padding: $l;
}
</style>
