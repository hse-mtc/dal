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
              fixed
            />
            <el-table-column
              v-for="d in journal.dates"
              :key="d"
              :label="formatDate(d)"
              align="center"
              min-width="150"
            >
              <template slot-scope="scope">
                <div class="mark-journal-cell">
                  <el-popover
                    v-if="scope.row.marks.some((x) => x.lesson.date == d)"
                    trigger="hover"
                    placement="top"
                  >
                    <el-form
                      label-position="right"
                      label-width="150px"
                      size="mini"
                      :model="scope.row.marks.find((x) => x.lesson.date == d)"
                    >
                      <el-form-item label="Тип занятия: ">
                        <el-tag
                          :type="
                            tagByLessonType(
                              scope.row.marks.find((x) => x.lesson.date == d)
                                .lesson.lesson_type
                            )
                          "
                          disable-transitions
                        >
                          {{
                            scope.row.marks.find((x) => x.lesson.date == d)
                              .lesson.lesson_type
                          }}
                        </el-tag>
                      </el-form-item>
                      <el-form-item label="Комментарий: ">
                        {{
                          scope.row.marks.find((x) => x.lesson.date == d)
                            .comment
                        }}
                      </el-form-item>
                    </el-form>
                    <el-button-group>
                      <el-button
                        size="mini"
                        icon="el-icon-plus"
                        type="primary"
                        @click="onCreate(scope.row, d)"
                        >Пересдача</el-button
                      >
                      <el-button
                        size="mini"
                        icon="el-icon-edit"
                        type="info"
                        @click="
                          onEdit(
                            scope.row.marks.find((x) => x.lesson.date == d),
                            scope.row
                          )
                        "
                        >Редактировать</el-button
                      >
                      <el-button
                        size="mini"
                        icon="el-icon-delete"
                        type="danger"
                        @click="
                          handleDelete(
                            scope.row.marks.find((x) => x.lesson.date == d).id
                          )
                        "
                        >Удалить</el-button
                      >
                    </el-button-group>
                    <el-tag
                      v-for="m in scope.row.marks.find(
                        (x) => x.lesson.date == d
                      ).mark"
                      :key="m"
                      slot="reference"
                      :type="tagByMark(m)"
                      effect="dark"
                      disable-transitions
                    >
                      {{ m }}
                    </el-tag>
                  </el-popover>
                  <el-button
                    v-else
                    type="text"
                    icon="el-icon-plus"
                    @click="onCreate(scope.row, d)"
                    class="create-mark-btn"
                  />
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-dialog
      :title="editMarkFullname"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
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
        <el-form-item label="Комментарий: ">
          <el-input
            v-model="editMark.comment"
            placeholder="Введите комментарий"
            type="textarea"
            :rows="2"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Отмена</el-button>
        <el-button type="primary" @click="handleAccept()">Применить</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import moment from "moment";
import { getMarkJournal, patchMark, postMark, deleteMark } from "@/api/mark";
import { getSubjects } from "@/api/subjects";
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
      lesson_types: [
        "Семинар",
        "Лекция",
        "Групповое занятие",
        "Практическое занятие",
      ],
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
    formatDate: (d) => moment(d).format("DD.MM.YY"),
    tagByLessonType(type) {
      switch (type) {
        case "Лекция":
          return "primary";
        case "Семинар":
          return "danger";
        case "Групповое занятие":
          return "warning";
        case "Практическое занятие":
          return "success";
        case "Зачет":
          return "info";
        case "Экзамен":
          return "info";
        case "Контрольная работа":
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
        milgroup: { milgroup: this.filter.mg },
        subject: {},
      };
      this.editMarkFullname = student.fullname;
      this.getSubjects();
      // this.dialogVisible = true;
    },
    onEdit(mark, student) {
      this.editMark = {
        id: mark.id,
        student: student.id,
        lesson: mark.lesson.id,
        mark: mark.mark,
      };
      console.log(this.editMark);
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
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
