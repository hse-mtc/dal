<template>
  <div>
    <el-col :offset="2" :span="20" class="Absence">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-tabs v-model="activeTab" stretch @click="onFilter">
        <el-tab-pane label="Пропуски" name="absences">
          <el-row class="filterRow" :gutter="20">
            <el-col :span="7">
              <el-date-picker
                v-model="filter.dateRange"
                type="daterange"
                align="right"
                unlink-panels
                range-separator="по"
                start-placeholder="Начальная дата"
                end-placeholder="Конечная дата"
                :picker-options="pickerOptions"
                format="dd.MM.yyyy"
                value-format="yyyy-MM-dd"
                @change="onFilter"
                @clear="onFilter"
              />
            </el-col>
            <el-col :span="5">
              <el-input
                v-model="filter.search"
                clearable
                placeholder="Поиск..."
                @clear="onFilter"
                @keyup.native.enter="onFilter"
              />
            </el-col>
            <el-col :span="4">
              <el-select
                v-model="filter.mg"
                value-key="milgroup"
                clearable
                placeholder="Выберите взвод"
                style="display: block"
                @change="onFilter"
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
                style="display: block"
                @change="onFilter"
              >
                <el-option
                  v-for="item in types"
                  :key="item.code"
                  :label="item.label"
                  :value="item.code"
                />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select
                v-model="filter.status"
                clearable
                placeholder="Выберите статус"
                style="display: block"
                @change="onFilter"
              >
                <el-option
                  v-for="item in statuses"
                  :key="item.code"
                  :label="item.label"
                  :value="item.code"
                />
              </el-select>
            </el-col>
          </el-row>
          <el-row>
            <el-table
              :data="absences"
              :default-sort="{
                prop: 'date',
                order: 'descending'
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
                    :type="tagByAbsenceType(scope.row.type)"
                    disable-transitions
                  >
                    {{ scope.row.type | absenceTypeFilter }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column sortable label="Статус">
                <template slot-scope="scope">
                  <i
                    slot="reference"
                    :class="iconByAbsenceStatus(scope.row.status)"
                    :style="colorByAbsenceStatus(scope.row.status)"
                  />
                  {{ scope.row.status | absenceStatusFilter }}
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
        <el-tab-pane label="Журнал" name="journal">
          <AbsenceJournal v-if="activeTab === 'journal'" />
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
            v-model="editAbsence.type"
            placeholder="Выберите тип причины"
            style="display: block"
          >
            <el-option
              v-for="item in types"
              :key="item.code"
              :label="item.label"
              :value="item.code"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Статус: ">
          <el-switch
            :value="editAbsence.status === 'CL'"
            active-text="Закрыт"
            inactive-text="Открыт"
            @change="changeAbsenceStatus(editAbsence)"
          />
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
import {
  getError,
  patchError,
  deleteError,
  patchSuccess,
  deleteSuccess,
} from "@/utils/message";
import AbsenceJournal from "@/components/AbsenceJournal/AbsenceJournal.vue";

export default {
  name: "Absence",
  components: {
    AbsenceJournal,
  },
  filters: {
    absenceTypeFilter(value) {
      switch (value) {
        case "SE":
          return "Уважительная";
        case "NS":
          return "Неуважительная";
        case "LA":
          return "Опоздание";
        default:
          return "Ошибка";
      }
    },
    absenceStatusFilter(value) {
      switch (value) {
        case "OP":
          return "Открыт";
        case "CL":
          return "Закрыт";
        default:
          return "Ошибка";
      }
    },
  },
  data() {
    return {
      dialogVisible: false,
      activeTab: "absences",
      editAbsence: {
        id: 0,
        date: "",
        type: "",
        status: "",
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
      types: [
        { label: "Уважительная", code: "SE" },
        { label: "Неуважительная", code: "NS" },
        { label: "Опоздание", code: "LA" },
      ],
      statuses: [
        { label: "Закрыт", code: "CL" },
        { label: "Открыт", code: "OP" },
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
      // todo
      // eslint-disable-next-line no-param-reassign
      absence.status = absence.status === "CL" ? "OP" : "CL";
    },
    tagByAbsenceType(type) {
      switch (type) {
        case "NS":
          return "danger";
        case "LA":
          return "warning";
        default:
          return "success";
      }
    },
    iconByAbsenceStatus(status) {
      switch (status) {
        case "OP":
          return "el-icon-circle-close";
        default:
          return "el-icon-circle-check";
      }
    },
    colorByAbsenceStatus(status) {
      switch (status) {
        case "OP":
          return "color: red;";
        default:
          return "color: green;";
      }
    },
    formatDate: row => moment(row.date).format("DD.MM.YY"),
    onFilter() {
      getAbsence({
        date_from:
          this.filter.dateRange !== null ? this.filter.dateRange[0] : null,
        date_to:
          this.filter.dateRange !== null ? this.filter.dateRange[1] : null,
        type: this.filter.type,
        status: this.filter.status,
        search: this.filter.search,
        milgroup: this.filter.mg !== null ? this.filter.mg.milgroup : null,
      })
        .then(response => {
          this.absences = response.data;
        })
        .catch(err => getError("пропусков", err.response.status));
    },
    onCreate(student, date) {
      this.editAbsence = { status: "Открыт", student: student.id, date };
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
        },
      )
        .then(() => {
          this.dialogVisible = false;
        })
        .catch(() => {});
    },
    handleAccept() {
      patchAbsence(this.editAbsence)
        .then(() => {
          patchSuccess("пропуска");
          this.dialogVisible = false;
          this.onFilter();
        })
        .catch(err => patchError("пропуска", err.response.status));
    },
    handleDelete(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить пропуск?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(() => {
        deleteAbsence({ id })
          .then(() => {
            deleteSuccess("пропуска");
            this.onFilter();
          })
          .catch(err => deleteError("пропуска", err.response.status));
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
