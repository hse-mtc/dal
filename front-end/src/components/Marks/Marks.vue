<template>
  <div>
    <el-col :offset="2" :span="20" class="Marks">
      <el-row class="pageTitle">
        <h1>{{ this.$route.meta.title }}</h1>
      </el-row>
      <el-row>
        <el-tabs v-model="filter.subject_id" @tab-click="fetchData()">
          <el-tab-pane
            v-for="item in subjects"
            :key="item.id"
            :label="item.title"
            :name="item.id"
          >
          </el-tab-pane></el-tabs
      ></el-row>
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
      <el-tabs tab-position="left" v-model="filter.mg" @tab-click="fetchData()">
        <el-tab-pane
          v-for="mg in milgroups"
          :key="mg.milgroup"
          :label="mg.milgroup"
          :name="mg.milgroup"
        >
          <el-table
            :data="journal.ordinals"
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
              v-for="d in journal.dates"
              :key="d"
              :label="formatDate(d)"
              align="center"
              min-width="250"
              show-overflow-tooltip
            >
              <template slot-scope="scope">
                <div class="mark-journal-cell">
                  <el-popover
                    v-if="scope.row.marks.some((x) => x.date == d)"
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
                          onEdit(scope.row.marks.find((x) => x.date == d))
                        "
                      />
                      <el-button
                        size="mini"
                        icon="el-icon-delete"
                        type="danger"
                        circle
                        @click="
                          handleDelete(
                            scope.row.marks.find((x) => x.date == d).id
                          )
                        "
                      />
                    </div>
                    <div slot="reference">
                      <div>
                        <svg-icon icon-class="notebook-outline" />
                        {{
                          scope.row.marks.find((x) => x.date == d).subject.title
                        }}
                      </div>

                      <div>
                        <svg-icon icon-class="map-marker-outline" />
                        {{ scope.row.marks.find((x) => x.date == d).room }}
                      </div>

                      <el-tag
                        :type="
                          tagByLessonType(
                            scope.row.marks.find((x) => x.date == d).mark_type
                          )
                        "
                        disable-transitions
                      >
                        {{ scope.row.marks.find((x) => x.date == d).mark_type }}
                      </el-tag>
                    </div>
                  </el-popover>
                  <el-button
                    v-else
                    type="text"
                    icon="el-icon-plus"
                    @click="onCreate(scope.row.ordinal, d)"
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
        <el-form-item label="Дисциплина: " required>
          <el-select
            filterable
            v-model="editMark.subject"
            value-key="id"
            placeholder="Выберите дисциплину"
            style="display: block"
          >
            <el-option
              v-for="item in subjects"
              :key="item.id"
              :label="item.title"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Аудитория: " required>
          <el-select
            filterable
            v-model="editMark.room"
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
            v-model="editMark.mark_type"
            placeholder="Выберите тип занятия"
            style="display: block"
          >
            <el-option
              v-for="item in mark_types"
              :key="item"
              :label="item"
              :value="item"
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
import { getMarkJournal, patchMark, postMark, deleteMark } from "@/api/mark";
import { getSubjects } from "@/api/subjects";
import {
  getError,
  postError,
  patchError,
  deleteError,
  postSuccess,
  patchSuccess,
} from "@/utils/message";

export default {
  name: "Marks",
  data() {
    return {
      dialogVisible: false,
      editMarkFullname: "",
      editMark: {
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
        mark_type: "",
        room: "",
      },
      filter: {
        subject_id: null,
        mg: null,
        dateRange: [
          moment().format("YYYY-MM-DD"),
          moment().add(1, "months").format("YYYY-MM-DD"),
        ],
      },
      lesson_types: [
        "Семинар",
        "Лекция",
        "Групповое занятие",
        "Практическое занятие",
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
      journal: {},
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
    this.getSubjects();
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
        default:
          return "info";
      }
    },
    fetchData() {
      if (this.filter.mg > 0) {
        getMarkJournal({
          milgroup: this.filter.mg,
          date_from: this.filter.dateRange[0],
          date_to: this.filter.dateRange[1],
        })
          .then((response) => {
            this.journal = response.data;
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
      this.editMark = {
        ordinal,
        date,
        milgroup: { milgroup: this.filter.mg },
        subject: {},
      };
      this.editMarkFullname = "Новое занятие";
      this.getSubjects();
      this.dialogVisible = true;
    },
    onEdit(row) {
      this.editMark = { ...row };
      this.editMark.milgroup = {
        milgroup: this.editMark.milgroup.milgroup,
      };
      this.editMarkFullname = "Редактирование занятия";
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
            patchSuccess("занятия");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch((err) => patchError("занятия", err.response.status));
      } else {
        postMark(this.editMark)
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
        deleteMark({ id })
          .then(() => {
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
