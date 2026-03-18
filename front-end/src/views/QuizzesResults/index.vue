<template>
  <div class="app-container">
    <el-row>
      <el-col :span="20" :offset="2">
        <PageHeader title="Результаты летучек" />

        <el-card v-loading="loading" shadow="never" class="quizzes-card">
          <div v-if="!quizzes.length && !loading" class="empty-state">
            Нет доступных летучек
          </div>

          <el-table
            v-else
            :data="quizzes"
            style="width: 100%"
            border
          >
            <el-table-column label="Название теста" prop="title" />
            <el-table-column label="Описание" prop="description">
              <template slot-scope="{ row }">
                {{ row.description || '—' }}
              </template>
            </el-table-column>
            <el-table-column label="Дата создания" width="180">
              <template slot-scope="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="Действия" width="220" align="center">
              <template slot-scope="{ row }">
                <el-button
                  size="small"
                  type="primary"
                  icon="el-icon-view"
                  @click="openResults(row)"
                >
                  Результаты
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- Диалог с результатами -->
        <el-dialog
          :title="`Результаты: ${selectedQuiz ? selectedQuiz.title : ''}`"
          :visible.sync="resultsDialogVisible"
          width="80%"
          top="5vh"
          @close="handleDialogClose"
        >
          <div v-loading="resultsLoading">
            <div v-if="!attempts.length && !resultsLoading" class="empty-state">
              Никто ещё не проходил этот тест
            </div>

            <el-table
              v-else
              :data="attempts"
              style="width: 100%"
              border
              :default-sort="{ prop: 'score', order: 'descending' }"
            >
              <el-table-column type="index" label="№" width="55" />
              <el-table-column label="Студент" min-width="200">
                <template slot-scope="{ row }">
                  <span v-if="row.studentName">{{ row.studentName }}</span>
                  <span v-else class="user-id-fallback">ID: {{ row.email }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="Результат"
                width="130"
                align="center"
                prop="score"
                sortable
              >
                <template slot-scope="{ row }">
                  <template v-if="row.completed_at">
                    <el-tag :type="getScoreTagType(row.score, row.max_score)">
                      {{ row.score }} / {{ row.max_score }}
                    </el-tag>
                  </template>
                  <el-tag v-else type="info">
                    В процессе
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="%" width="90" align="center">
                <template slot-scope="{ row }">
                  <span v-if="row.completed_at && row.max_score">
                    {{ Math.round((row.score / row.max_score) * 100) }}%
                  </span>
                  <span v-else>—</span>
                </template>
              </el-table-column>
              <el-table-column label="Статус" width="130" align="center">
                <template slot-scope="{ row }">
                  <el-tag v-if="row.completed_at" type="success">
                    Завершён
                  </el-tag>
                  <el-tag v-else type="warning">
                    Не завершён
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="Начало" width="160">
                <template slot-scope="{ row }">
                  {{ formatDate(row.started_at) }}
                </template>
              </el-table-column>
              <el-table-column label="Завершение" width="160">
                <template slot-scope="{ row }">
                  {{ row.completed_at ? formatDate(row.completed_at) : '—' }}
                </template>
              </el-table-column>
            </el-table>

            <div v-if="attempts.length" class="results-summary">
              <span>Всего попыток: <strong>{{ attempts.length }}</strong></span>
              <span>Завершено: <strong>{{ completedCount }}</strong></span>
              <span>Средний балл: <strong>{{ averageScore }}</strong></span>
            </div>
          </div>

          <span slot="footer">
            <el-button @click="resultsDialogVisible = false">Закрыть</el-button>
          </span>
        </el-dialog>
      </el-col>
    </el-row>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import PageHeader from "@/common/PageHeader";
import { getAdminQuizzes, getTestAttempts } from "@/api/quizzes";
import { findStudentByUserId } from "@/api/students";

export default {
  name: "QuizzesResultsPage",
  components: { PageHeader },
  data() {
    return {
      loading: false,
      quizzes: [],
      resultsDialogVisible: false,
      resultsLoading: false,
      selectedQuiz: null,
      attempts: [],
    };
  },
  computed: {
    completedCount() {
      return this.attempts.filter(a => a.completed_at).length;
    },
    averageScore() {
      const completed = this.attempts.filter(a => a.completed_at && a.max_score);
      if (!completed.length) { return "—"; }
      const sum = completed.reduce((acc, a) => acc + Math.round((a.score / a.max_score) * 100), 0);
      return `${Math.round(sum / completed.length)}%`;
    },
  },
  created() {
    this.fetchQuizzes();
  },
  methods: {
    async fetchQuizzes() {
      this.loading = true;
      try {
        const response = await getAdminQuizzes();
        this.quizzes = response?.data || [];
      } catch (error) {
        this.$message.error("Не удалось загрузить список тестов");
      } finally {
        this.loading = false;
      }
    },
    async openResults(quiz) {
      this.selectedQuiz = quiz;
      this.resultsDialogVisible = true;
      this.attempts = [];
      this.resultsLoading = true;

      try {
        const response = await getTestAttempts(quiz.id);
        const rawAttempts = response?.data || [];

        // Загружаем имена студентов параллельно
        const attemptsWithNames = await Promise.all(
          rawAttempts.map(async attempt => {
            try {
              const studentResponse = await findStudentByUserId(attempt.user_id);
              const student = studentResponse?.data[0];
              const fullName = student?.fullname
                || (student?.surname && student?.name
                  ? `${student.surname} ${student.name}${student.patronymic ? ` ${student.patronymic}` : ""}`
                  : null);
              return { ...attempt, studentName: fullName || null };
            } catch {
              return { ...attempt, studentName: null };
            }
          }),
        );

        this.attempts = attemptsWithNames;
      } catch (error) {
        this.$message.error("Не удалось загрузить результаты");
      } finally {
        this.resultsLoading = false;
      }
    },
    handleDialogClose() {
      this.selectedQuiz = null;
      this.attempts = [];
    },
    formatDate(dateStr) {
      if (!dateStr) { return "—"; }
      return new Date(dateStr).toLocaleString("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    getScoreTagType(score, maxScore) {
      if (!maxScore) { return "info"; }
      const pct = score / maxScore;
      if (pct >= 0.8) { return "success"; }
      if (pct >= 0.5) { return "warning"; }
      return "danger";
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.quizzes-card {
  margin-bottom: $l;
}

.empty-state {
  border: 1px dashed $lightGray;
  border-radius: 8px;
  padding: $l;
  color: $gray;
  text-align: center;
}

.user-id-fallback {
  color: $gray;
  font-style: italic;
}

.results-summary {
  display: flex;
  gap: $l;
  margin-top: $m;
  padding-top: $m;
  border-top: 1px solid $lightGray;
  color: $gray;

  strong {
    color: $black;
  }
}
</style>
