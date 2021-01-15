<template>
  <div>
    <el-col :offset="2" :span="20" class="Absence">
      <el-row class="pageTitle">
        <h1>{{ this.$route.meta.title }}</h1>
      </el-row>
      <el-tabs stretch>
        <el-tab-pane label="Пропуски">
          <el-row class="filterRow" :gutter="20">
            <el-col :span="5">
              <el-input
                clearable
                placeholder="Поиск..."
                v-model="filter.search"
                v-on:clear="onFilter"
                v-on:keyup.native.enter="onFilter"
              ></el-input>
            </el-col>
            <el-col :span="4">
              <el-select
                v-model="filter.mg"
                value-key="milgroup"
                clearable
                placeholder="Выберите взвод"
                v-on:change="onFilter"
                style="display: block"
              >
                <el-option
                  v-for="item in milgroups"
                  :key="item.milgroup"
                  :label="item.milgroup"
                  :value="item"
                >
                  <span style="float: left">{{ item.milgroup }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{
                    item.milfaculty
                  }}</span>
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select
                v-model="filter.type"
                clearable
                placeholder="Выберите тип причины"
                v-on:change="onFilter"
                style="display: block"
              >
                <el-option
                  v-for="item in types"
                  :key="item"
                  :label="item"
                  :value="item"
                >
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select
                v-model="filter.status"
                clearable
                placeholder="Выберите статус"
                v-on:change="onFilter"
                style="display: block"
              >
                <el-option
                  v-for="item in statuses"
                  :key="item"
                  :label="item"
                  :value="item"
                >
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="5">
              <el-date-picker
                v-model="filter.dateRange"
                type="daterange"
                align="right"
                unlink-panels
                range-separator="по"
                start-placeholder="Начальная дата"
                end-placeholder="Конечная дата"
                :picker-options="pickerOptions"
                v-on:change="onFilter"
                v-on:clear="onFilter"
                format="dd.MM.yyyy"
                value-format="yyyy-MM-dd"
              >
              </el-date-picker>
            </el-col>
          </el-row>
          <el-row>
            <el-table
              :data="absences"
              :default-sort="{
                prop: 'date',
                order: 'descending',
              }"
              style="width: 100%"
              max-height="680"
              stripe
            >
              <el-table-column
                sortable
                label="Дата"
                width="100"
                prop="date"
                :formatter="formatDate"
              />
              <el-table-column
                prop="student.fullname"
                sortable
                show-overflow-tooltip
                label="ФИО"
              />
              <el-table-column
                prop="student.milgroup.milgroup"
                sortable
                label="Взвод"
                width="100"
              />
              <el-table-column sortable label="Тип причины">
                <template slot-scope="scope">
                  <el-tag
                    :type="tagByAbsenceType(scope.row.absence_type)"
                    disable-transitions
                    >{{ scope.row.absence_type }}</el-tag
                  >
                </template>
              </el-table-column>
              <el-table-column sortable label="Статус">
                <template slot-scope="scope">
                  <i
                    slot="reference"
                    :class="iconByAbsenceStatus(scope.row.absence_status)"
                    :style="colorByAbsenceStatus(scope.row.absence_status)"
                  />
                  {{ scope.row.absence_status }}
                </template>
              </el-table-column>
              <el-table-column prop="reason" sortable label="Причина" />
              <el-table-column prop="comment" label="Комментарий" />
              <el-table-column width="120px">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    icon="el-icon-edit"
                    type="info"
                    circle
                    @click="onEdit(scope.row, scope.row.student.fullname)"
                  />
                  <el-button
                    size="mini"
                    icon="el-icon-delete"
                    type="danger"
                    circle
                    @click="handleDelete(scope.row.id)"
                  />
                </template>
              </el-table-column>
            </el-table>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="Журнал">
          <AbsenceJournal />
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-dialog
      :title="editAbsenceFullname"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editAbsence"
      >
        <el-form-item label="Тип причины: ">
          <el-select
            v-model="editAbsence.absence_type"
            placeholder="Выберите тип причины"
            style="display: block"
          >
            <el-option
              v-for="item in types"
              :key="item"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Статус: ">
          <el-switch
            :value="editAbsence.absence_status == 'Закрыт'"
            active-text="Закрыт"
            inactive-text="Открыт"
            @change="changeAbsenceStatus(editAbsence)"
          >
          </el-switch>
        </el-form-item>
        <el-form-item label="Причина: ">
          <el-input
            v-model="editAbsence.reason"
            placeholder="Введите причину"
          />
        </el-form-item>
        <el-form-item label="Комментарий: ">
          <el-input
            v-model="editAbsence.comment"
            type="textarea"
            :rows="2"
            placeholder="Введите комментарий"
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
import { getAbsence, patchAbsence, deleteAbsence } from "@/api/absence";
import moment from "moment";

import AbsenceJournal from "@/components/AbsenceJournal/AbsenceJournal";

export default {
  name: "Absence",
  components: {
    AbsenceJournal,
  },
  data() {
    return {
      dialogVisible: false,
      editAbsence: {
        id: 0,
        date: "",
        absence_type: "",
        absence_status: "",
        student: {
          id: "",
          name: "",
          surname: "",
          patronymic: "",
          fullname: "",
          milgroup: {
            milgroup: "",
            milfaculty: "",
          },
        },
        reason: "",
        comment: "",
      },
      editAbsenceFullname: "",
      filter: {
        type: null,
        status: null,
        dateRange: [
          moment().format("YYYY-MM-DD"),
          moment().format("YYYY-MM-DD"),
        ],
        search: null,
        mg: null,
      },
      absences: [],
      types: ["Уважительная", "Неуважительная", "Опоздание"],
      statuses: ["Закрыт", "Открыт"],
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
  created() {
    this.onFilter();
  },
  methods: {
    changeAbsenceStatus(absence) {
      absence.absence_status =
        absence.absence_status == "Закрыт" ? "Открыт" : "Закрыт";
    },
    tagByAbsenceType(type) {
      switch (type) {
        case "Неуважительная":
          return "danger";
        case "Опоздание":
          return "warning";
        default:
          return "success";
      }
    },
    iconByAbsenceStatus(status) {
      switch (status) {
        case "Открыт":
          return "el-icon-circle-close";
        default:
          return "el-icon-circle-check";
      }
    },
    colorByAbsenceStatus(status) {
      switch (status) {
        case "Открыт":
          return "color: red;";
        default:
          return "color: green;";
      }
    },
    formatDate: (row) => moment(row.date).format("DD.MM.YY"),
    onFilter() {
      getAbsence({
        date_from:
          this.filter.dateRange !== null ? this.filter.dateRange[0] : null,
        date_to:
          this.filter.dateRange !== null ? this.filter.dateRange[1] : null,
        absence_type: this.filter.type,
        absence_status: this.filter.status,
        search: this.filter.search,
        milgroup: this.filter.mg !== null ? this.filter.mg.milgroup : null,
      })
        .then((response) => {
          this.absences = response.data;
        })
        .catch(() => {
          this.$message({
            message: "Ошибка получения пропусков!",
            type: "error",
          });
        });
    },
    onCreate(student, date) {
      this.editAbsence = { absence_status: "Открыт", student, date };
      this.editAbsenceFullname = student.fullname;
      this.dialogVisible = true;
    },
    onEdit(row, fn) {
      this.editAbsence = { ...row };
      this.editAbsence.student = undefined;
      this.editAbsenceFullname = fn;
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
      patchAbsence(this.editAbsence)
        .then(() => {
          this.$message({
            message: "Пропуск успешно редактирован",
            type: "success",
          });
          this.dialogVisible = false;
          this.onFilter();
        })
        .catch(() => {
          this.$message({
            message: "Ошибка при редактировании пропуска!",
            type: "error",
          });
        });
    },
    handleDelete(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить пропуск?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        }
      ).then(() => {
        deleteAbsence({ id })
          .then(() => {
            this.$message({
              message: "Пропуск успешно удален",
              type: "success",
            });
            this.onFilter();
          })
          .catch(() => {
            this.$message({
              message: "Ошибка при удалении пропуска!",
              type: "error",
            });
          });
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
