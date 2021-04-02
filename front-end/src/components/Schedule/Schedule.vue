<template>
  <div>
    <el-col :offset="2" :span="20" class="Schedule">
      <el-row class="pageTitle">
        <h1>{{ this.$route.meta.title }}</h1>
      </el-row>
      <el-row class="filterRow" style="margin-bottom: 15px">
        <el-col :offset="17" :span="5">
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
            :data="schedule.ordinals"
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
              label="№"
              prop="ordinal"
              align="center"
              width="40"
              fixed
            />
            <el-table-column
              v-for="d in schedule.dates"
              :key="d"
              :label="formatDate(d)"
              align="center"
              min-width="250"
              show-overflow-tooltip
            >
              <template slot-scope="scope">
                <div class="lesson-journal-cell">
                  <el-popover
                    v-if="scope.row.lessons.some((x) => x.date == d)"
                    placement="right"
                    trigger="hover"
                  >
                    <div class="text-center">
                      <el-button
                        size="mini"
                        icon="el-icon-edit"
                        type="info"
                        circle
                        @click="
                          onEdit(scope.row.lessons.find((x) => x.date == d))
                        "
                      />
                      <el-button
                        size="mini"
                        icon="el-icon-delete"
                        type="danger"
                        circle
                        @click="
                          handleDelete(
                            scope.row.lessons.find((x) => x.date == d).id
                          )
                        "
                      />
                    </div>
                    <div slot="reference">
                      <div>
                        <svg-icon icon-class="notebook-outline" />
                        {{
                          scope.row.lessons.find((x) => x.date == d).subject
                            .title
                        }}
                      </div>

                      <div>
                        <svg-icon icon-class="map-marker-outline" />
                        {{ scope.row.lessons.find((x) => x.date == d).room }}
                      </div>

                      <el-tag
                        :type="
                          tagByLessonType(
                            scope.row.lessons.find((x) => x.date == d).type
                          )
                        "
                        disable-transitions
                      >
                        {{
                          scope.row.lessons.find((x) => x.date == d).type
                            | typeFilter
                        }}
                      </el-tag>
                    </div>
                  </el-popover>
                  <el-button
                    v-else
                    type="text"
                    icon="el-icon-plus"
                    @click="onCreate(scope.row.ordinal, d)"
                    class="create-lesson-btn"
                  />
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-dialog
      :title="editLessonFullname"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editLesson"
      >
        <el-form-item label="Дисциплина: " required>
          <el-select
            filterable
            v-model="editLesson.subject"
            value-key="id"
            placeholder="Выберите дисциплину"
            style="display: block"
          >
            <el-option
              v-for="item in subjects"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            >
            </el-option>
          </el-select>
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
        <el-button @click="dialogVisible = false">Отмена</el-button>
        <el-button type="primary" @click="handleAccept()">Применить</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import moment from "moment";
import {
  getLessonJournal,
  patchLesson,
  postLesson,
  deleteLesson,
} from "@/api/lesson";
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
  name: "Schedule",
  data() {
    return {
      dialogVisible: false,
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
      filter: {
        mg: null,
        dateRange: [
          moment().format("YYYY-MM-DD"),
          moment().add(1, "months").format("YYYY-MM-DD"),
        ],
      },
      lesson_types: [
        { label: "Семинар", code: "SE" },
        { label: "Лекция", code: "LE" },
        { label: "Групповое занятие", code: "GR" },
        { label: "Практическое занятие", code: "PR" },
        { label: "Зачет", code: "FI" },
        { label: "Экзамен", code: "EX" },
      ],
      rooms: ["510", "501", "502", "503", "504", "Плац"],
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
      schedule: {},
      pickerOptions: {
        shortcuts: [
          {
            text: "Неделя",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              end.setTime(start.getTime() + 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "Месяц",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              end.setTime(start.getTime() + 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "3 месяца",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              end.setTime(start.getTime() + 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
    };
  },
  created() {
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
    formatDate: (d) => moment(d).format("DD.MM.YY"),
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
    limitDateRange() {
      var main, other;
      var maxMonths = 6;
      if (
        moment().diff(this.filter.dateRange[1]) >
        moment().diff(this.filter.dateRange[0])
      ) {
        main = 1;
        other = 0;
      } else {
        main = 0;
        other = 1;
      }
      var diff = moment(this.filter.dateRange[main]).diff(
        this.filter.dateRange[other],
        "months",
        true
      );
      if (Math.abs(diff) > maxMonths) {
        this.filter.dateRange[other] = moment(this.filter.dateRange[main])
          .add(Math.sign(diff) * maxMonths, "months")
          .format("YYYY-MM-DD");
      }
    },
    fetchData() {
      if (this.filter.mg > 0) {
        this.limitDateRange();
        getLessonJournal({
          milgroup: this.filter.mg,
          date_from: this.filter.dateRange[0],
          date_to: this.filter.dateRange[1],
        })
          .then((response) => {
            this.schedule = response.data;
          })
          .catch((err) => getError("расписания", err.response.status));
      }
    },
    getSubjects() {
      getSubjects()
        .then((response) => {
          this.subjects = response.data;
        })
        .catch((err) => getError("дисциплин", err.response.status));
    },

    onCreate(ordinal, date) {
      this.editLesson = {
        ordinal,
        date,
        milgroup: this.filter.mg,
      };
      this.editLessonFullname = "Новое занятие";
      this.getSubjects();
      this.dialogVisible = true;
    },
    onEdit(row) {
      this.editLesson = { ...row };
      this.editLesson.milgroup = this.editLesson.milgroup.milgroup;
      this.editLesson.subject = this.editLesson.subject.id;
      this.editLessonFullname = "Редактирование занятия";
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
      if (this.editLesson.id) {
        patchLesson(this.editLesson)
          .then(() => {
            patchSuccess("занятия");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch((err) => patchError("занятия", err.response.status));
      } else {
        postLesson(this.editLesson)
          .then(() => {
            postSuccess("занятия");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch((err) => postError("занятия", err.response.status));
      }
    },
    handleDelete(id) {
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
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
