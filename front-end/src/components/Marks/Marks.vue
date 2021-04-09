<template>
  <div>
    <el-col :offset="2" :span="20" class="Marks">
      <el-row class="pageTitle">
        <h1>{{ this.$route.meta.title }}</h1>
      </el-row>
      <el-row class="filterRow" style="margin-bottom: 15px" :gutter="20">
        <el-col :offset="11" :span="6">
          <el-select
            filterable
            v-model="filter.subject_id"
            placeholder="Дисциплина"
            style="display: block"
            @change="fetchData()"
          >
            <el-option
              v-for="item in subjects"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            >
            </el-option>
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
            v-on:change="fetchData"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
          >
          </el-date-picker>
        </el-col>
      </el-row>
      <el-tabs
        tab-position="left"
        v-model="filter.mg"
        @tab-click="fetchData()"
        class="my-tabs"
      >
        <el-tab-pane
          v-for="mg in milgroups"
          :key="mg.milgroup"
          :label="mg.milgroup"
          :name="mg.milgroup"
        >
          <el-row>
            <el-col :span="22">
              <el-table
                :data="journal.students"
                style="width: 100%"
                height="730"
                :default-sort="{
                  prop: 'ordinal',
                  order: 'ascending',
                }"
                stripe
                border
              >
                <el-table-column
                  label="ФИО"
                  prop="fullname"
                  width="250"
                  show-overflow-tooltip
                />
                <el-table-column
                  v-for="d in journal.dates"
                  :key="d"
                  :label="formatDate(d)"
                  align="center"
                  min-width="50"
                >
                  <el-table-column
                    v-for="item in getLessonsByDate(d)"
                    :key="item.id"
                  >
                    <template slot="header">
                      <div class="column-template">
                        <span>
                          <svg-icon icon-class="map-marker-outline" />
                          {{ item.room }}
                        </span>
                        <span> {{ item.ordinal }} пара </span>
                        <el-tag :type="item.type" disable-transitions>
                          {{ item.type | typeFilter }}
                        </el-tag>
                      </div>
                    </template>
                    <template slot-scope="scope">
                      <div class="mark-journal-cell">
                        <div
                          v-for="marks in scope.row.marks
                            .filter((x) => x.lesson.date == d)
                            .map((x) => x.mark)"
                          :key="marks"
                        >
                          <el-tag
                            v-for="m in marks"
                            :key="m"
                            :type="tagByMark(m)"
                            effect="dark"
                            disable-transitions
                          >
                            {{ m }}
                          </el-tag>
                        </div>
                        <el-button
                          type="text"
                          icon="el-icon-plus"
                          @click="onCreate(scope.row, d)"
                          class="create-mark-btn"
                        />
                      </div>
                    </template>
                  </el-table-column>
                </el-table-column>
              </el-table>
            </el-col>
            <el-col :span="2" class="new-lesson-col">
              <el-button
                type="primary"
                icon="el-icon-plus"
                circle
                @click="onCreateLesson()"
              ></el-button>
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
        <el-button @click="dialogVisible = false">Отмена</el-button>
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
            type="date"
            placeholder="Выберите дату"
            v-model="editLesson.date"
            style="width: 100%"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="Номер занятия: " required>
          <el-input-number
            size="mini"
            v-model="editLesson.ordinal"
            controls-position="right"
            :min="1"
            :max="10"
            style="width: 100%"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="Аудитория: " required>
          <el-select
            filterable
            v-model="editLesson.room"
            placeholder="Выберите аудиторию"
            style="display: block"
          >
            <el-option
              v-for="item in rooms"
              :key="item"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Тип занятия: " required>
          <el-select
            v-model="editLesson.type"
            placeholder="Выберите тип занятия"
            style="display: block"
          >
            <el-option
              v-for="item in lesson_types"
              :key="item.code"
              :label="item.label"
              :value="item.code"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="lessonDialogVisible = false">Отмена</el-button>
        <el-button type="primary" @click="handleAcceptLesson()"
          >Применить</el-button
        >
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
    ></el-button>
  </div>
</template>

<script>
import moment from "moment";
import { getMarkJournal, patchMark, postMark, deleteMark } from "@/api/mark";
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
      lesson_types: [
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
  methods: {
    getLessonsByDate(d) {
      const student = this.journal.students.find((x) =>
        x.marks.some((y) => y.lesson.date === d)
      );
      console.log('🚀 > student', student);
      if (student) {
        const marks = student.marks.filter((x) => x.lesson.date === d);
        console.log('🚀 > marks', marks);
        if (marks) {
          const lessons = marks.map((x) => x.lesson);
          console.log('🚀 > lessons', lessons);
          return lessons;
        }
      }
      return [];
    },
    formatDate: (d) => moment(d).format("DD.MM.YY"),
    isOnlyLesson(marks) {
      console.log(marks);
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
          .then((response) => {
            this.journal = response.data;
          })
          .catch((err) => getError("расписания", err.response.status));
      }
    },
    async getSubjects() {
      this.subjects = (await getSubjects()).data;
    },

    onCreate(student, date) {
      this.editMark = {
        student,
        date,
        milgroup: this.filter.mg,
        subject: {},
      };
      this.editMarkFullname = student.fullname;
      this.getSubjects();
      // TODO: use on mark creation
      // this.dialogVisible = true;
    },
    onEdit(mark, student) {
      this.editMark = {
        id: mark.id,
        student: student.id,
        lesson: mark.lesson.id,
        mark: mark.mark,
      };
      this.editMarkFullname = student.fullname;
      this.getSubjects();
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
        }
      )
        .then(() => {
          this.dialogVisible = false;
          this.lessonDialogVisible = false;
        })
        .catch(() => {});
    },
    handleAccept() {
      if (this.editMark.id) {
        patchMark(this.editMark)
          .then(() => {
            patchSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch((err) => patchError("оценки", err.response.status));
      } else {
        postMark(this.editMark)
          .then(() => {
            postSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch((err) => postError("оценки", err.response.status));
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
            if (this.filter.mg > 0) this.fetchData();
          })
          .catch((err) => deleteError("оценки", err.response.status));
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
      this.getSubjects();
      this.lessonDialogVisible = true;
    },
    handleAcceptLesson() {
      console.log(this.editLesson);
      if (this.editLesson.id) {
        patchLesson(this.editLesson)
          .then(() => {
            patchSuccess("занятия");
            this.lessonDialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch((err) => patchError("занятия", err.response.status));
      } else {
        postLesson(this.editLesson)
          .then(() => {
            postSuccess("занятия");
            this.lessonDialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch((err) => postError("занятия", err.response.status));
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
        }
      ).then(() => {
        deleteLesson({ id })
          .then(() => {
            deleteSuccess("занятия");
            if (this.filter.mg > 0) this.fetchData();
          })
          .catch((err) => deleteError("занятия", err.response.status));
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
