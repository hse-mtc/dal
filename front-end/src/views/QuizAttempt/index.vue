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
            v-if="successMessage"
            type="success"
            :closable="false"
            show-icon
            :title="successMessage"
            class="alert"
          />

          <el-card v-loading="loading" shadow="never" class="attempt-card">
            <div class="attempt-meta">
              <div><span class="attempt-label">Количество вопросов:</span> {{ questions.length }}</div>
            </div>

            <el-alert
              type="info"
              :closable="false"
              show-icon
              title="Ответьте на вопросы и нажмите “Завершить попытку”"
              class="alert"
            />

            <div v-if="!questions.length" class="quiz-attempt-content">
              В этой летучке пока нет вопросов
            </div>

            <div
              v-for="question in questions"
              :key="question.id"
              class="question-card"
            >
              <div class="question-title">
                {{ question.order }}. {{ question.text }}
              </div>

              <el-radio-group
                v-if="question.type === 'single'"
                v-model="question.selectedSingleOptionId"
              >
                <el-radio
                  v-for="option in question.options"
                  :key="option.id"
                  :label="option.id"
                  class="answer-option"
                >
                  {{ option.text }}
                </el-radio>
              </el-radio-group>

              <div v-else-if="question.type === 'multiple'">
                <el-checkbox
                  v-for="option in question.options"
                  :key="option.id"
                  v-model="option.selected"
                  class="answer-option"
                >
                  {{ option.text }}
                </el-checkbox>
              </div>

              <el-input-number
                v-else
                v-model="question.selectedNumericAnswer"
                :controls="false"
                placeholder="Введите число"
              />
            </div>

            <el-button
              type="primary"
              :loading="isSubmitting"
              :disabled="!questions.length"
              @click="submitAnswers"
            >
              Завершить попытку
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
import { getQuizById, getQuizQuestions, submitQuizAnswers } from "@/api/quizzes";

export default {
  name: "QuizAttemptPage",
  components: {
    PageHeader,
  },
  data() {
    return {
      loading: false,
      isSubmitting: false,
      errorMessage: "",
      successMessage: "",
      quizTitle: "Прохождение летучки",
      questions: [],
    };
  },
  computed: {
    quizId() {
      return this.$route.params.quizId;
    },
    attemptId() {
      return this.$route.params.attemptId;
    },
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.errorMessage = "";

      try {
        const [quizResponse, questionsResponse] = await Promise.all([
          getQuizById(this.quizId),
          getQuizQuestions(this.quizId),
        ]);

        this.quizTitle = quizResponse?.data?.title || "Прохождение летучки";
        this.questions = (questionsResponse?.data || []).map(question => {
          const options = Array.isArray(question.options)
            ? question.options.map(option => {
              // Создаем новый объект с реактивным свойством selected
              const newOption = {
                id: option.id,
                text: option.text,
                is_correct: option.is_correct,
                selected: false,
              };
              return newOption;
            })
            : [];

          return {
            id: question.id,
            text: question.text,
            type: question.type,
            order: question.order,
            options,
            selectedSingleOptionId: null,
            selectedNumericAnswer: null,
          };
        });
      } catch (error) {
        this.errorMessage = "Не удалось загрузить вопросы летучки";
      } finally {
        this.loading = false;
      }
    },
    buildAnswersPayload() {
      const payload = [];

      this.questions.forEach(question => {
        if (question.type === "single") {
          const optionId = question.selectedSingleOptionId;
          if (optionId) {
            payload.push({
              question_id: question.id,
              option_ids: [optionId],
            });
          }
        } else if (question.type === "multiple") {
          console.log(`Question ${question.id} options:`, question.options);
          const optionIds = (question.options || [])
            .filter(option => {
              console.log(`Option ${option.id} selected:`, option.selected);
              return option.selected;
            })
            .map(option => option.id)
            .filter(Boolean);
          console.log(`Question ${question.id} selected option IDs:`, optionIds);
          if (optionIds.length) {
            payload.push({
              question_id: question.id,
              option_ids: optionIds,
            });
          }
        } else if (question.type === "numeric") {
          const numericAnswer = question.selectedNumericAnswer;
          if (numericAnswer !== null && numericAnswer !== undefined && numericAnswer !== "") {
            payload.push({
              question_id: question.id,
              numeric_answer: Number(numericAnswer),
            });
          }
        }
      });

      console.log("Final payload:", payload);
      return payload;
    },
    async submitAnswers() {
      this.isSubmitting = true;
      this.errorMessage = "";
      this.successMessage = "";

      try {
        const answers = this.buildAnswersPayload();
        if (!answers.length) {
          this.errorMessage = "Выберите хотя бы один ответ перед отправкой";
          return;
        }

        const response = await submitQuizAnswers(this.quizId, this.attemptId, answers);
        const result = response?.data;

        this.$message.success(`Попытка завершена. Результат: ${result.score} из ${result.max_score}`);
        this.$router.push("/discipline-control/quizzes/");
      } catch (error) {
        this.errorMessage = error?.response?.data?.detail || "Не удалось отправить ответы";
      } finally {
        this.isSubmitting = false;
      }
    },
    goBack() {
      this.$router.push("/discipline-control/quizzes/");
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.back-button {
  margin-bottom: $m;
}

.attempt-card {
  margin-bottom: $l;
}

.attempt-meta {
  margin-bottom: $m;
}

.attempt-label {
  font-family: $nova-bold;
}

.alert {
  margin-bottom: $m;
}

.quiz-attempt-content {
  border: 1px dashed $lightGray;
  border-radius: 8px;
  padding: $l;
  color: $gray;
}

.question-card {
  border: 1px solid $lightGray;
  border-radius: 8px;
  padding: $m;
  margin-bottom: $m;
}

.question-title {
  font-family: $nova-bold;
  margin-bottom: $m;
}

.answer-option {
  display: block;
  margin-bottom: $s;
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
