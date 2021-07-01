<template>
  <div>
    <el-col :offset="2" :span="20" class="Absence">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-tabs value="absences" stretch @click="onFilter">
        <el-tab-pane label="Пропуски" name="absences">
          <el-row class="filterRow" :gutter="20">
            <el-col :span="8">
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
                style="width: auto"
                @change="onFilter"
                @clear="onFilter"
              />
            </el-col>
            <el-col :span="4">
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
            <PrimeTable
              v-loading="loading"
              :value="absences"
              :sort-field="dateField"
              :sort-order="-1"
              scrollable
              scroll-height="680px"
              class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
            >
              <PrimeColumn
                sortable
                header="Дата"
                :field="dateField"
                column-key="date"
                header-style="width: 100px"
                body-style="width: 100px"
              />
              <PrimeColumn
                :field="(row) => row.student.fullname"
                sortable
                header="ФИО"
                column-key="fullname"
              />
              <PrimeColumn
                :field="row => row.student.milgroup.milgroup"
                sortable
                header="Взвод"
                header-style="width: 100px"
                body-style="width: 100px"
                column-key="milgroup"
              />

              <PrimeColumn
                sortable
                header="Тип причины"
                column-key="type"
                field="type"
              >
                <template #body="{ data: { type } }">
                  <el-tag
                    :type="tagByAbsenceType(type)"
                    disable-transitions
                  >
                    {{ type | absenceTypeFilter }}
                  </el-tag>
                </template>
              </PrimeColumn>

              <PrimeColumn
                sortable
                header="Статус"
                column-key="status"
                field="status"
              >
                <template #body="{ data: { status } }">
                  <i
                    slot="reference"
                    :class="iconByAbsenceStatus(status)"
                    :style="colorByAbsenceStatus(status)"
                  />
                  {{ status | absenceStatusFilter }}
                </template>
              </PrimeColumn>

              <PrimeColumn
                field="reason"
                sortable
                column-key="reason"
                header="Причина"
              />
              <PrimeColumn
                field="comment"
                column-key="comment"
                header="Комментарий"
              />
              <PrimeColumn
                column-key="buttons"
                header-style="width: 120px"
                body-style="width: 120px"
              >
                <template #body="{ data }">
                  <el-button
                    size="mini"
                    icon="el-icon-edit"
                    type="info"
                    circle
                    @click="onEdit(data, data.student.fullname)"
                  />
                  <el-button
                    size="mini"
                    icon="el-icon-delete"
                    type="danger"
                    circle
                    @click="handleDelete(data.id)"
                  />
                </template>
              </PrimeColumn>
            </PrimeTable>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="Журнал" name="journal">
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
import AbsenceJournal from "./AbsenceJournal/AbsenceJournal.vue";

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
      loading: false,
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
  computed: {
    milgroups() {
      return this.$store.state.reference.milgroups;
    },
    types() {
      return this.$store.state.reference.absenceTypes;
    },
    statuses() {
      return this.$store.state.reference.absenceStatuses;
    },
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
    dateField: row => moment(row.date).format("DD.MM.YY"),
    async fetchData() {
      if (!this.$store.state.reference.milgroups.length) {
        await this.$store.dispatch("reference/setMilgroups");
      }
      if (!this.$store.state.reference.absenceTypes.length) {
        await this.$store.dispatch("reference/setAbsenceTypes");
      }
      if (!this.$store.state.reference.absenceStatuses.length) {
        await this.$store.dispatch("reference/setAbsenceStatuses");
      }
    },
    async onFilter() {
      try {
        this.loading = true;
        await this.fetchData();
        this.absences = (
          await getAbsence({
            date_from:
              this.filter.dateRange !== null ? this.filter.dateRange[0] : null,
            date_to:
              this.filter.dateRange !== null ? this.filter.dateRange[1] : null,
            type: this.filter.type,
            status: this.filter.status,
            search: this.filter.search,
            milgroup: this.filter.mg !== null ? this.filter.mg.milgroup : null,
          })
        ).data;
      } catch (err) {
        getError("пропусков", err.response.status);
      } finally {
        this.loading = false;
      }
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
