<template>
  <div>
    <el-col :offset="2" :span="20" class="Marks">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-row class="filterRow" style="margin-bottom: 15px" :gutter="20">
        <el-col :offset="11" :span="6">
          <el-select
            v-model="filter.subject_id"
            filterable
            placeholder="Дисциплина"
            style="display: block"
            @change="fetchData()"
          >
            <el-option
              v-for="item in subjects"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            />
          </el-select>
        </el-col>
        <el-col :span="7">
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            align="right"
            unlink-panels
            :clearable="false"
            range-separator="по"
            start-placeholder="Начальная дата"
            end-placeholder="Конечная дата"
            :picker-options="pickerOptions"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
            @change="fetchData"
          />
        </el-col>
      </el-row>
      <el-tabs
        v-model="filter.mg"
        tab-position="left"
        class="my-tabs"
        @tab-click="fetchData()"
      >
        <el-tab-pane
          v-for="mg in milgroups"
          :key="mg.milgroup"
          :label="mg.milgroup"
          :name="mg.milgroup"
        >
          <el-row>
            <el-col :span="22">
              <PrimeTable
                :value="journal.students"
                scroll-height="730"
                scrollable
                sort-field="ordinal"
                :sort-order="1"
                class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
              >
                <PrimeColumnGroup type="header">
                  <PrimeRow>
                    <PrimeColumn
                      header="ФИО"
                      :rowspan="2"
                      column-key="fullname-header"
                    />
                    <PrimeColumn
                      v-for="d in journal.dates"
                      :key="d"
                      :column-key="`${d}-header`"
                      :header="formatDate(d)"
                      header-style="text-align: center"
                      :colspan="journal.lessons.filter((x) => x.date === d).length"
                    />
                  </PrimeRow>

                  <PrimeRow>
                    <template v-for="d in journal.dates">
                      <PrimeColumn
                        v-for="item in journal.lessons.filter((x) => x.date === d)"
                        :key="`${item.id}-header`"
                      >
                        <template #header>
                          <el-popover placement="top" trigger="hover">
                            <div class="header-template">
                              <!-- <span>
                              {{ item.topic }}
                            </span> -->
                              <el-tag
                                :type="tagByLessonType(item.type)"
                                disable-transitions
                              >
                                {{ item.type | typeFilter }}
                              </el-tag>
                              <span>
                                <svg-icon icon-class="map-marker-outline" />
                                {{ item.room }}
                              </span>
                              <div>
                                <el-button
                                  size="mini"
                                  icon="el-icon-edit"
                                  type="info"
                                  circle
                                  @click="onEditLesson(item)"
                                />
                                <el-button
                                  size="mini"
                                  icon="el-icon-delete"
                                  type="danger"
                                  circle
                                  @click="handleDeleteLesson(item.id)"
                                />
                              </div>
                            </div>
                            <div slot="reference" class="header-template">
                              <span> {{ item.ordinal }} пара </span>
                            </div>
                          </el-popover>
                        </template>
                      </PrimeColumn>
                    </template>
                  </PrimeRow>
                </PrimeColumnGroup>

                <PrimeColumn
                  header="ФИО"
                  field="fullname"
                  width="250"
                  column-key="fullname"
                />
                <template
                  v-for="d in journal.dates"
                >
                  <PrimeColumn
                    v-for="item in journal.lessons.filter((x) => x.date === d)"
                    :key="item.id"
                  >
                    <template #body="{ data }">
                      <div class="mark-journal-cell">
                        <div
                          v-for="m in getMarksByLesson(
                            data.marks,
                            item.id,
                          )"
                          :key="m"
                        >
                          <el-tag
                            :type="tagByMark(m)"
                            effect="dark"
                            disable-transitions
                            class="is-clickable margin-x"
                            @click="onEdit(
                              data.marks.find((x) => x.lesson === item.id),
                              data,
                            )"
                          >
                            {{ m }}
                          </el-tag>
                        </div>
                        <el-button
                          type="text"
                          icon="el-icon-plus"
                          class="create-mark-btn"
                          @click="
                            onCreate(
                              data,
                              item,
                              data.marks.find((x) => x.lesson === item.id),
                            )
                          "
                        />
                      </div>
                    </template>
                  </PrimeColumn>
                </template>
              </PrimeTable>
            </el-col>
            <el-col :span="2" class="new-lesson-col">
              <el-button
                type="primary"
                icon="el-icon-plus"
                circle
                @click="onCreateLesson()"
              />
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-dialog
      :title="editMarkFullname"
      :visible.sync="dialogVisible"
      width="20%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="100px"
        size="mini"
        :model="editMark"
      >
        <el-form-item label="Оценка: " required>
          <el-input-number
            v-model="editMark.mark"
            controls-position="right"
            :min="2"
            :max="5"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button
          v-if="editMarkId"
          type="danger"
          @click="handleDelete(editMarkId)"
        >Удалить</el-button>
        <el-button type="primary" @click="handleAccept()">Применить</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="editLessonFullname"
      :visible.sync="lessonDialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editLesson"
      >
        <el-form-item label="Дата: " required>
          <el-date-picker
            v-model="editLesson.date"
            type="date"
            placeholder="Выберите дату"
            style="width: 100%"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item label="Номер занятия: " required>
          <el-input-number
            v-model="editLesson.ordinal"
            size="mini"
            controls-position="right"
            :min="1"
            :max="10"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="Аудитория: " required>
          <el-select
            v-model="editLesson.room"
            filterable
            placeholder="Выберите аудиторию"
            style="display: block"
          >
            <el-option
              v-for="item in rooms"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Тип занятия: " required>
          <el-select
            v-model="editLesson.type"
            placeholder="Выберите тип занятия"
            style="display: block"
          >
            <el-option
              v-for="item in lessonTypes"
              :key="item.code"
              :label="item.label"
              :value="item.code"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="lessonDialogVisible = false">Отмена</el-button>
        <el-button
          type="primary"
          @click="handleAcceptLesson()"
        >Применить</el-button>
      </span>
    </el-dialog>

    <el-drawer :title="drawerTitle" :visible.sync="drawer" direction="rtl">
      <span>Hi, there!</span>
    </el-drawer>

    <el-button
      type="primary"
      size="large"
      class="drawer-button"
      icon="el-icon-arrow-left"
      plain
      @click="openDrawer"
    />
  </div>
</template>

<script>
import moment from "moment";
import {
  getMarkJournal,
  patchMark,
  postMark,
  putMark,
  deleteMark,
} from "@/api/mark";
import { getSubjects } from "@/api/subjects";
import { postLesson, patchLesson, deleteLesson } from "@/api/lesson";
import {
  getError,
  postError,
  patchError,
  deleteError,
  postSuccess,
  patchSuccess,
  deleteSuccess,
} from "@/utils/message";

export default {
  name: "Marks",
  filters: {
    typeFilter(value) {
      switch (value) {
        case "LE":
          return "Лекция";
        case "SE":
          return "Семинар";
        case "GR":
          return "Групповое занятие";
        case "PR":
          return "Практическое занятие";
        case "FI":
          return "Зачет";
        case "EX":
          return "Экзамен";
        default:
          return "Ошибка";
      }
    },
  },
  data() {
    return {
      lessonDialogVisible: false,
      editLessonFullname: "",
      editLesson: {
        id: 0,
        subject: {
          id: 0,
          title: "",
        },
        milgroup: {
          milgroup: null,
          milfaculty: "",
        },
        date: "",
        ordinal: 0,
        type: "",
        room: "",
      },
      drawer: false,
      drawerTitle: "",
      dialogVisible: false,
      editMarkFullname: "",
      editMark: {
        id: 0,
        student: {},
        lesson: {
          id: 0,
          title: "",
        },
        mark: 0,
      },
      editMarkId: 0,
      editMarkMethod: "POST",
      filter: {
        subject_id: 0,
        mg: 0,
        dateRange: [
          moment().add(-3, "months").format("YYYY-MM-DD"),
          moment().format("YYYY-MM-DD"),
        ],
      },
      milgroups: [
        {
          milgroup: "1807",
          milfaculty: "ВКС",
        },
        {
          milgroup: "1808",
          milfaculty: "ВКС",
        },
        {
          milgroup: "1809",
          milfaculty: "ВКС",
        },
      ],
      lessonTypes: [
        { label: "Семинар", code: "SE" },
        { label: "Лекция", code: "LE" },
        { label: "Групповое занятие", code: "GR" },
        { label: "Практическое занятие", code: "PR" },
        { label: "Зачет", code: "FI" },
        { label: "Экзамен", code: "EX" },
      ],
      rooms: ["510", "501", "502", "503", "504", "Плац"],
      subjects: [],
      journal: {},
      pickerOptions: {
        shortcuts: [
          {
            text: "Неделя",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "Месяц",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "3 месяца",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
    };
  },
  async created() {
    await this.getSubjects();
    this.filter.subject_id = this.subjects[0].id;
    this.filter.mg = this.milgroups[0].milgroup;
    this.fetchData();
  },
  methods: {
    getMarksByLesson(marks, lessonId) {
      const m = marks.find(x => x.lesson === lessonId);
      if (m) {
        const result = m.mark;
        return result;
      }
      return [];
    },
    formatDate: d => moment(d).format("DD.MM.YY"),
    isOnlyLesson(marks) {
      return marks.length === 1;
    },
    tagByLessonType(type) {
      switch (type) {
        case "LE":
          return "primary";
        case "SE":
          return "danger";
        case "GR":
          return "warning";
        case "PR":
          return "success";
        case "FI":
          return "info";
        case "EX":
          return "info";
        default:
          return "info";
      }
    },
    tagByMark(mark) {
      switch (mark) {
        case 5:
          return "primary";
        case 4:
          return "success";
        case 3:
          return "warning";
        case 2:
          return "danger";
        default:
          return "info";
      }
    },
    fetchData() {
      if (this.filter.mg > 0 && this.filter.subject_id > 0) {
        getMarkJournal({
          milgroup: this.filter.mg,
          subject: this.filter.subject_id,
          date_from: this.filter.dateRange[0],
          date_to: this.filter.dateRange[1],
        })
          .then(response => {
            this.journal = response.data;
          })
          .catch(err => getError("расписания", err.response.status));
      }
    },
    async getSubjects() {
      this.subjects = (await getSubjects()).data;
    },

    onCreate(student, lesson, mark) {
      if (student.marks.some(x => x.lesson === lesson.id)) {
        this.editMarkMethod = "PUT";
        this.editMarkId = mark.id;
        this.editMark = {
          mark: 5,
        };
      } else {
        this.editMarkMethod = "POST";
        this.editMarkId = null;
        this.editMark = {
          student: student.id,
          lesson: lesson.id,
          mark: 5,
        };
      }
      console.log("🚀 > this.editMark ", this.editMark);
      this.editMarkFullname = student.fullname;
      this.dialogVisible = true;
    },
    onEdit(mark, student) {
      this.editMarkMethod = "PATCH";
      this.editMark = {
        mark: mark.mark[mark.mark.length - 1],
      };
      this.editMarkId = mark.id;
      this.editMarkFullname = student.fullname;
      this.dialogVisible = true;
    },
    handleClose() {
      this.$confirm(
        "Вы уверены, что хотите закрыть окно редактирования?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      )
        .then(() => {
          this.dialogVisible = false;
          this.lessonDialogVisible = false;
        })
        .catch(() => {});
    },
    handleAccept() {
      if (this.editMarkMethod === "PATCH") {
        patchMark(this.editMark, this.editMarkId)
          .then(() => {
            patchSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch(err => patchError("оценки", err.response.status));
      } else if (this.editMarkMethod === "POST") {
        postMark(this.editMark)
          .then(() => {
            postSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch(err => postError("оценки", err.response.status));
      } else if (this.editMarkMethod === "PUT") {
        putMark(this.editMark, this.editMarkId)
          .then(() => {
            patchSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch(err => patchError("оценки", err.response.status));
      }
    },
    handleDelete(id) {
      this.$confirm("Вы уверены, что хотите удалить оценку?", "Подтверждение", {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      }).then(() => {
        deleteMark({ id })
          .then(() => {
            deleteSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg > 0) this.fetchData();
          })
          .catch(err => deleteError("оценки", err.response.status));
      });
    },
    onCreateLesson() {
      this.editLesson = {
        milgroup: this.filter.mg,
        subject: this.filter.subject_id,
        ordinal: 1,
        date: moment().format("YYYY-MM-DD"),
      };
      this.editLessonFullname = "Новое занятие";
      this.lessonDialogVisible = true;
    },
    onEditLesson(row) {
      this.editLesson = { ...row };
      this.editLesson.milgroup = this.editLesson.milgroup.milgroup;
      this.editLesson.subject = this.editLesson.subject.id;
      this.editLessonFullname = "Редактирование занятия";
      this.lessonDialogVisible = true;
    },
    handleAcceptLesson() {
      if (this.editLesson.id) {
        patchLesson(this.editLesson)
          .then(() => {
            patchSuccess("занятия");
            this.lessonDialogVisible = false;
            if (this.filter.mg) {
              this.fetchData();
            }
          })
          .catch(err => patchError("занятия", err.response.status));
      } else {
        postLesson(this.editLesson)
          .then(() => {
            postSuccess("занятия");
            this.lessonDialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch(err => postError("занятия", err.response.status));
      }
    },
    handleDeleteLesson(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить занятие?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(() => {
        deleteLesson({ id })
          .then(() => {
            deleteSuccess("занятия");
            if (this.filter.mg > 0) this.fetchData();
          })
          .catch(err => deleteError("занятия", err.response.status));
      });
    },
    openDrawer() {
      this.drawer = true;
      // fetch data
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
