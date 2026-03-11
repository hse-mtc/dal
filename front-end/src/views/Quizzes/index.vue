<template>
  <div class="app-container">
    <el-row>
      <el-col :span="20" :offset="2">
        <PageHeader title="Прохождение летучек" />

        <template>
          <div class="statistics">
            <div class="statistics-card">
              <div class="statistics-card-number">
                {{ quizzes.length }}
              </div>
              <div class="statistics-card-text">
                Всего доступно
              </div>
            </div>
            <div class="statistics-card">
              <div class="statistics-card-number">
                {{ inProgressCount }}
              </div>
              <div class="statistics-card-text">
                В процессе
              </div>
            </div>
            <div class="statistics-card">
              <div class="statistics-card-number">
                {{ completedCount }}
              </div>
              <div class="statistics-card-text">
                Сдано
              </div>
            </div>
          </div>

          <el-row :gutter="16" class="filters-row">
            <el-col :md="12" :sm="24" :xs="24">
              <el-input
                v-model="searchQuery"
                clearable
                placeholder="Поиск по названию"
                @input="onFilterChanged"
              />
            </el-col>
            <el-col :md="12" :sm="24" :xs="24">
              <el-select
                v-model="disciplineFilter"
                clearable
                filterable
                placeholder="Фильтр по описанию"
                style="width: 100%"
                @change="onFilterChanged"
              >
                <el-option
                  v-for="description in descriptions"
                  :key="description"
                  :label="description"
                  :value="description"
                />
              </el-select>
            </el-col>
          </el-row>

          <el-alert
            v-if="errorMessage"
            type="error"
            :closable="false"
            show-icon
            :title="errorMessage"
            class="alert"
          />

          <el-table
            v-loading="loading"
            :data="filteredQuizzes"
            class="quizzes-table"
          >
            <el-table-column
              prop="title"
              label="Название летучки"
              min-width="260"
            />
            <el-table-column
              prop="description"
              label="Описание"
              min-width="180"
            >
              <template slot-scope="scope">
                {{ scope.row.description || "—" }}
              </template>
            </el-table-column>
            <el-table-column
              label="Доступность"
              min-width="220"
            >
              <template slot-scope="scope">
                {{ formatAvailability(scope.row) }}
              </template>
            </el-table-column>
            <el-table-column
              label="Статус"
              width="150"
            >
              <template slot-scope="scope">
                <el-tag :type="statusTagType(scope.row.status)">
                  {{ statusLabel(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label=""
              width="140"
              align="right"
            >
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="primary"
                  @click="openQuiz(scope.row)"
                >
                  {{ scope.row.status === QUIZ_STATUS.notStarted ? "Начать" : "Открыть" }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div
            v-if="!loading && !filteredQuizzes.length"
            class="state-wrapper"
          >
            <div class="empty-state">
              Доступных летучек пока нет
            </div>
          </div>
        </template>
      </el-col>
    </el-row>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import PageHeader from "@/common/PageHeader";
import { getStudentQuizzes, QUIZ_STATUS } from "@/api/quizzes";

export default {
  name: "QuizzesPage",
  components: {
    PageHeader,
  },
  data() {
    return {
      loading: false,
      quizzes: [],
      searchQuery: "",
      disciplineFilter: "",
      errorMessage: "",
      QUIZ_STATUS,
    };
  },
  computed: {
    descriptions() {
      return Array.from(new Set(this.quizzes.map(quiz => quiz.description).filter(Boolean)));
    },
    filteredQuizzes() {
      const search = this.searchQuery.toLowerCase().trim();
      const discipline = this.disciplineFilter.toLowerCase().trim();

      return this.quizzes.filter(quiz => {
        const bySearch = !search || quiz.title.toLowerCase().includes(search);
        const byDiscipline = !discipline || (quiz.description || "").toLowerCase() === discipline;
        return bySearch && byDiscipline;
      });
    },
    inProgressCount() {
      return this.quizzes.filter(quiz => quiz.status === QUIZ_STATUS.inProgress).length;
    },
    completedCount() {
      return this.quizzes.filter(quiz => quiz.status === QUIZ_STATUS.completed).length;
    },
  },
  created() {
    this.fetchQuizzes();
  },
  methods: {
    async fetchQuizzes() {
      this.loading = true;
      this.errorMessage = "";

      try {
        const response = await getStudentQuizzes();
        this.quizzes = response.data || [];
      } catch (error) {
        this.errorMessage = "Не удалось загрузить список летучек";
      } finally {
        this.loading = false;
      }
    },
    onFilterChanged() {
      this.errorMessage = "";
    },
    openQuiz(quiz) {
      this.$router.push(`/discipline-control/quizzes/${quiz.id}/`);
    },
    formatAvailability(quiz) {
      if (quiz.availabilityStart && quiz.availabilityEnd) {
        return `${this.formatDate(quiz.availabilityStart)} — ${this.formatDate(quiz.availabilityEnd)}`;
      }
      if (quiz.availabilityEnd) {
        return `До ${this.formatDate(quiz.availabilityEnd)}`;
      }
      return "Без ограничений";
    },
    formatDate(value) {
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) {
        return value;
      }
      return date.toLocaleString("ru-RU");
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
    statusTagType(status) {
      if (status === QUIZ_STATUS.inProgress) {
        return "warning";
      }
      if (status === QUIZ_STATUS.completed) {
        return "success";
      }
      return "info";
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.statistics {
  display: flex;
  margin-bottom: $xl;
  gap: $l;

  &-card {
    min-width: 220px;
    background: $white;
    border-radius: 12px;
    border: 1px solid $lightGray;
    padding: $m;

    &-number {
      font-family: $nova-bold;
      font-size: 28px;
      line-height: 32px;
      color: $darkBlue;
      margin-bottom: $s;
    }

    &-text {
      color: $gray;
    }
  }
}

.filters-row {
  margin-bottom: $l;
}

.alert {
  margin-bottom: $m;
}

.quizzes-table {
  width: 100%;
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

@media screen and (max-width: 992px) {
  .statistics {
    flex-direction: column;
  }
}
</style>
