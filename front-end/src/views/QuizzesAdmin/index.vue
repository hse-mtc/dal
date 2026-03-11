<template>
  <div class="app-container">
    <el-row>
      <el-col :span="20" :offset="2">
        <PageHeader title="Конструктор летучек" />

        <el-alert
          v-if="errorMessage"
          type="error"
          :closable="false"
          show-icon
          :title="errorMessage"
          class="alert"
        />

        <el-card shadow="never" class="card-block">
          <div slot="header" class="card-header">
            Создать летучку
          </div>

          <el-form :model="testForm" label-width="140px">
            <el-form-item label="Название">
              <el-input v-model="testForm.title" placeholder="Введите название летучки" />
            </el-form-item>
            <el-form-item label="Описание">
              <el-input
                v-model="testForm.description"
                type="textarea"
                :rows="3"
                placeholder="Введите описание"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="creatingTest" @click="createTest">
                Создать летучку
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card shadow="never" class="card-block">
          <div slot="header" class="card-header">
            Доступные летучки
          </div>

          <el-table v-loading="loadingTests" :data="tests" class="tests-table">
            <el-table-column prop="title" label="Название" min-width="220" />
            <el-table-column prop="description" label="Описание" min-width="220">
              <template slot-scope="scope">
                {{ scope.row.description || "—" }}
              </template>
            </el-table-column>
            <el-table-column label="Действие" width="150" align="right">
              <template slot-scope="scope">
                <el-button size="mini" type="primary" @click="selectTest(scope.row)">
                  Выбрать
                </el-button>
                <el-button size="mini" type="text" @click="openEditTest(scope.row)">
                  Редактировать
                </el-button>
                <el-button size="mini" type="text" @click="removeTest(scope.row)">
                  Удалить
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <el-card v-if="selectedTest" shadow="never" class="card-block">
          <div slot="header" class="card-header">
            Добавить вопрос в летучку: {{ selectedTest.title }}
          </div>

          <el-form :model="questionForm" label-width="160px">
            <el-form-item label="Текст вопроса">
              <el-input
                v-model="questionForm.text"
                type="textarea"
                :rows="3"
                placeholder="Введите текст вопроса"
              />
            </el-form-item>

            <el-form-item label="Тип вопроса">
              <el-select v-model="questionForm.type" placeholder="Выберите тип" style="width: 260px">
                <el-option label="Один вариант" value="single" />
                <el-option label="Несколько вариантов" value="multiple" />
                <el-option label="Числовой" value="numeric" />
              </el-select>
            </el-form-item>

            <template v-if="questionForm.type === 'numeric'">
              <el-form-item label="Правильное число">
                <el-input-number v-model="questionForm.correct_number" :controls="false" />
              </el-form-item>
            </template>

            <template v-else>
              <el-form-item label="Варианты ответов">
                <div class="hint">
                  Для «Несколько вариантов» отметьте все правильные ответы.
                </div>
                <div
                  v-for="(option, index) in questionForm.options"
                  :key="`option-${index}`"
                  class="option-row"
                >
                  <el-input
                    v-model="option.text"
                    placeholder="Текст варианта"
                    class="option-input"
                  />
                  <el-checkbox v-model="option.is_correct">
                    Правильный
                  </el-checkbox>
                  <el-button type="text" @click="removeOption(index)">
                    Удалить
                  </el-button>
                </div>

                <el-button size="mini" @click="addOption">
                  Добавить вариант
                </el-button>
              </el-form-item>
            </template>

            <el-form-item>
              <el-button type="primary" :loading="creatingQuestion" @click="createQuestion">
                Добавить вопрос
              </el-button>
            </el-form-item>
          </el-form>

          <el-divider />

          <div class="sub-title">
            Вопросы летучки
          </div>
          <el-table v-loading="loadingQuestions" :data="questions" class="tests-table">
            <el-table-column prop="order" label="#" width="80" />
            <el-table-column prop="text" label="Вопрос" min-width="260" />
            <el-table-column label="Тип" width="150">
              <template slot-scope="scope">
                {{ typeLabel(scope.row.type) }}
              </template>
            </el-table-column>
            <el-table-column label="Действие" width="120" align="right">
              <template slot-scope="scope">
                <el-button type="text" @click="openEditQuestion(scope.row)">
                  Редактировать
                </el-button>
                <el-button type="text" @click="removeQuestion(scope.row)">
                  Удалить
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <el-dialog
          title="Редактировать летучку"
          :visible.sync="editTestDialogVisible"
          width="560px"
        >
          <el-form :model="editTestForm" label-width="120px">
            <el-form-item label="Название">
              <el-input v-model="editTestForm.title" />
            </el-form-item>
            <el-form-item label="Описание">
              <el-input v-model="editTestForm.description" type="textarea" :rows="3" />
            </el-form-item>
          </el-form>
          <span slot="footer">
            <el-button @click="editTestDialogVisible = false">Отмена</el-button>
            <el-button type="primary" :loading="updatingTest" @click="saveEditedTest">
              Сохранить
            </el-button>
          </span>
        </el-dialog>

        <el-dialog
          title="Редактировать вопрос"
          :visible.sync="editQuestionDialogVisible"
          width="760px"
        >
          <el-form :model="editQuestionForm" label-width="150px">
            <el-form-item label="Текст вопроса">
              <el-input v-model="editQuestionForm.text" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item label="Тип вопроса">
              <el-select v-model="editQuestionForm.type" style="width: 260px">
                <el-option label="Один вариант" value="single" />
                <el-option label="Несколько вариантов" value="multiple" />
                <el-option label="Числовой" value="numeric" />
              </el-select>
            </el-form-item>

            <template v-if="editQuestionForm.type === 'numeric'">
              <el-form-item label="Правильное число">
                <el-input-number v-model="editQuestionForm.correct_number" :controls="false" />
              </el-form-item>
            </template>

            <template v-else>
              <el-form-item label="Варианты ответов">
                <div class="hint">
                  Для «Несколько вариантов» отметьте все правильные ответы.
                </div>
                <div
                  v-for="(option, index) in editQuestionForm.options"
                  :key="`edit-option-${index}`"
                  class="option-row"
                >
                  <el-input v-model="option.text" class="option-input" />
                  <el-checkbox v-model="option.is_correct">
                    Правильный
                  </el-checkbox>
                  <el-button type="text" @click="removeEditOption(index)">
                    Удалить
                  </el-button>
                </div>
                <el-button size="mini" @click="addEditOption">
                  Добавить вариант
                </el-button>
              </el-form-item>
            </template>
          </el-form>
          <span slot="footer">
            <el-button @click="editQuestionDialogVisible = false">Отмена</el-button>
            <el-button type="primary" :loading="updatingQuestion" @click="saveEditedQuestion">
              Сохранить
            </el-button>
          </span>
        </el-dialog>
      </el-col>
    </el-row>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import PageHeader from "@/common/PageHeader";
import {
  createQuizQuestion,
  createQuizTest,
  deleteQuizQuestion,
  deleteQuizTest,
  getAdminQuizzes,
  getQuizQuestions,
  updateQuizQuestion,
  updateQuizTest,
} from "@/api/quizzes";

function getDefaultQuestionForm() {
  return {
    text: "",
    type: "single",
    options: [
      { text: "", is_correct: false },
      { text: "", is_correct: false },
    ],
    correct_number: null,
  };
}

export default {
  name: "QuizzesAdminPage",
  components: { PageHeader },
  data() {
    return {
      loadingTests: false,
      loadingQuestions: false,
      creatingTest: false,
      creatingQuestion: false,
      updatingTest: false,
      updatingQuestion: false,
      errorMessage: "",
      tests: [],
      questions: [],
      selectedTest: null,
      editTestDialogVisible: false,
      editQuestionDialogVisible: false,
      editTestForm: {
        id: null,
        title: "",
        description: "",
      },
      editQuestionForm: {
        id: null,
        text: "",
        order: 1,
        type: "single",
        options: [],
        correct_number: null,
      },
      testForm: {
        title: "",
        description: "",
      },
      questionForm: getDefaultQuestionForm(),
    };
  },
  created() {
    this.fetchTests();
  },
  methods: {
    async fetchTests() {
      this.loadingTests = true;
      this.errorMessage = "";

      try {
        const response = await getAdminQuizzes();
        this.tests = response.data || [];
      } catch (error) {
        this.errorMessage = "Не удалось загрузить список летучек";
      } finally {
        this.loadingTests = false;
      }
    },
    async fetchQuestions() {
      if (!this.selectedTest?.id) {
        return;
      }

      this.loadingQuestions = true;

      try {
        const response = await getQuizQuestions(this.selectedTest.id);
        this.questions = response.data || [];
      } catch (error) {
        this.errorMessage = "Не удалось загрузить вопросы летучки";
      } finally {
        this.loadingQuestions = false;
      }
    },
    async createTest() {
      if (!this.testForm.title.trim()) {
        this.errorMessage = "Введите название летучки";
        return;
      }

      this.creatingTest = true;
      this.errorMessage = "";

      try {
        const response = await createQuizTest({
          title: this.testForm.title.trim(),
          description: this.testForm.description?.trim() || null,
        });

        this.$message.success("Летучка создана");
        this.testForm.title = "";
        this.testForm.description = "";
        await this.fetchTests();
        this.selectTest(response.data);
      } catch (error) {
        this.errorMessage = error?.response?.data?.detail || "Не удалось создать летучку";
      } finally {
        this.creatingTest = false;
      }
    },
    selectTest(test) {
      this.selectedTest = test;
      this.questionForm = getDefaultQuestionForm();
      this.questions = [];
      this.fetchQuestions();
    },
    addOption() {
      this.questionForm.options.push({ text: "", is_correct: false });
    },
    removeOption(index) {
      this.questionForm.options.splice(index, 1);
    },
    openEditTest(test) {
      this.editTestForm = {
        id: test.id,
        title: test.title || "",
        description: test.description || "",
      };
      this.editTestDialogVisible = true;
    },
    async saveEditedTest() {
      if (!this.editTestForm.id) {
        return;
      }
      if (!this.editTestForm.title.trim()) {
        this.errorMessage = "Название летучки не может быть пустым";
        return;
      }

      this.updatingTest = true;
      this.errorMessage = "";

      try {
        const response = await updateQuizTest(this.editTestForm.id, {
          title: this.editTestForm.title.trim(),
          description: this.editTestForm.description?.trim() || null,
        });

        this.$message.success("Летучка обновлена");
        this.editTestDialogVisible = false;
        await this.fetchTests();

        if (this.selectedTest?.id === this.editTestForm.id) {
          this.selectedTest = response.data;
        }
      } catch (error) {
        this.errorMessage = error?.response?.data?.detail || "Не удалось обновить летучку";
      } finally {
        this.updatingTest = false;
      }
    },
    openEditQuestion(question) {
      this.editQuestionForm = {
        id: question.id,
        text: question.text || "",
        order: question.order,
        type: question.type || "single",
        options: (question.options || []).map(option => ({
          text: option.text,
          is_correct: false,
        })),
        correct_number: question.correct_number,
      };

      if (!this.editQuestionForm.options.length && this.editQuestionForm.type !== "numeric") {
        this.editQuestionForm.options = [
          { text: "", is_correct: false },
          { text: "", is_correct: false },
        ];
      }

      this.editQuestionDialogVisible = true;
    },
    addEditOption() {
      this.editQuestionForm.options.push({ text: "", is_correct: false });
    },
    removeEditOption(index) {
      this.editQuestionForm.options.splice(index, 1);
    },
    buildEditQuestionPayload() {
      const base = {
        text: this.editQuestionForm.text.trim(),
        order: this.editQuestionForm.order,
        type: this.editQuestionForm.type,
      };

      if (this.editQuestionForm.type === "numeric") {
        return {
          ...base,
          options: [],
          correct_number: this.editQuestionForm.correct_number,
        };
      }

      return {
        ...base,
        options: this.editQuestionForm.options
          .map(option => ({
            text: (option.text || "").trim(),
            is_correct: Boolean(option.is_correct),
          }))
          .filter(option => option.text),
        correct_number: null,
      };
    },
    async saveEditedQuestion() {
      if (!this.selectedTest?.id || !this.editQuestionForm.id) {
        return;
      }

      const payload = this.buildEditQuestionPayload();
      const validationError = this.validateQuestionPayload(payload);
      if (validationError) {
        this.errorMessage = validationError;
        return;
      }

      this.updatingQuestion = true;
      this.errorMessage = "";

      try {
        await updateQuizQuestion(this.selectedTest.id, this.editQuestionForm.id, payload);
        this.$message.success("Вопрос обновлён");
        this.editQuestionDialogVisible = false;
        await this.fetchQuestions();
      } catch (error) {
        this.errorMessage = error?.response?.data?.detail || "Не удалось обновить вопрос";
      } finally {
        this.updatingQuestion = false;
      }
    },
    buildQuestionPayload() {
      const maxOrder = this.questions.reduce((acc, question) => {
        const currentOrder = Number(question.order) || 0;
        return currentOrder > acc ? currentOrder : acc;
      }, 0);

      const base = {
        text: this.questionForm.text.trim(),
        order: maxOrder + 1,
        type: this.questionForm.type,
      };

      if (this.questionForm.type === "numeric") {
        return {
          ...base,
          options: [],
          correct_number: this.questionForm.correct_number,
        };
      }

      return {
        ...base,
        options: this.questionForm.options
          .map(option => ({
            text: option.text.trim(),
            is_correct: Boolean(option.is_correct),
          }))
          .filter(option => option.text),
        correct_number: null,
      };
    },
    validateQuestionPayload(payload) {
      if (!payload.text) {
        return "Введите текст вопроса";
      }

      if (payload.type === "numeric") {
        if (payload.correct_number === null || payload.correct_number === undefined) {
          return "Укажите правильный числовой ответ";
        }
        return "";
      }

      if (!payload.options || payload.options.length < 2) {
        return "Добавьте минимум два варианта ответа";
      }

      const correctCount = payload.options.filter(option => option.is_correct).length;
      if (correctCount < 1) {
        return "Отметьте хотя бы один правильный вариант";
      }

      if (payload.type === "single" && correctCount !== 1) {
        return "Для типа 'Один вариант' должен быть ровно один правильный ответ";
      }

      return "";
    },
    async createQuestion() {
      if (!this.selectedTest?.id) {
        this.errorMessage = "Сначала выберите летучку";
        return;
      }

      const payload = this.buildQuestionPayload();
      const validationError = this.validateQuestionPayload(payload);
      if (validationError) {
        this.errorMessage = validationError;
        return;
      }

      this.creatingQuestion = true;
      this.errorMessage = "";

      try {
        await createQuizQuestion(this.selectedTest.id, payload);
        this.$message.success("Вопрос добавлен");
        this.questionForm = getDefaultQuestionForm();
        await this.fetchQuestions();
      } catch (error) {
        this.errorMessage = error?.response?.data?.detail || "Не удалось добавить вопрос";
      } finally {
        this.creatingQuestion = false;
      }
    },
    async removeTest(test) {
      try {
        await this.$confirm(
          `Удалить летучку "${test.title}"?`,
          "Подтверждение",
          {
            confirmButtonText: "Удалить",
            cancelButtonText: "Отмена",
            type: "warning",
          },
        );

        await deleteQuizTest(test.id);
        this.$message.success("Летучка удалена");

        if (this.selectedTest?.id === test.id) {
          this.selectedTest = null;
          this.questions = [];
          this.questionForm = getDefaultQuestionForm();
        }

        await this.fetchTests();
      } catch (error) {
        if (error !== "cancel") {
          this.errorMessage = error?.response?.data?.detail || "Не удалось удалить летучку";
        }
      }
    },
    async removeQuestion(question) {
      if (!this.selectedTest?.id) {
        return;
      }

      try {
        await this.$confirm(
          "Удалить вопрос?",
          "Подтверждение",
          {
            confirmButtonText: "Удалить",
            cancelButtonText: "Отмена",
            type: "warning",
          },
        );

        await deleteQuizQuestion(this.selectedTest.id, question.id);
        this.$message.success("Вопрос удалён");
        await this.fetchQuestions();
      } catch (error) {
        if (error !== "cancel") {
          this.errorMessage = error?.response?.data?.detail || "Не удалось удалить вопрос";
        }
      }
    },
    typeLabel(type) {
      if (type === "single") {
        return "Один";
      }
      if (type === "multiple") {
        return "Несколько";
      }
      return "Числовой";
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.alert {
  margin-bottom: $m;
}

.card-block {
  margin-bottom: $l;
}

.card-header {
  font-family: $nova-bold;
}

.tests-table {
  width: 100%;
}

.option-row {
  display: flex;
  align-items: center;
  gap: $m;
  margin-bottom: $s;
}

.option-input {
  width: 360px;
}

.sub-title {
  font-family: $nova-bold;
  margin-bottom: $m;
}
</style>
