<template>
  <div>
    <el-row class="filterRow" style="margin-bottom: 15px">
      <el-col :offset="12" :span="5">
        <el-select
          v-model="filter.weekday"
          value-key="number"
          placeholder="Выберите учебный день"
          @change="onWeekdayChanged"
          style="display: block"
        >
          <el-option
            v-for="item in weekdays"
            :key="item.number"
            :label="item.name"
            :value="item.number"
          />
        </el-select>
      </el-col>
      <el-col :offset="1" :span="5">
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
          v-on:change="onJournal"
          format="dd.MM.yyyy"
          value-format="yyyy-MM-dd"
        >
        </el-date-picker>
      </el-col>
    </el-row>
    <el-tabs
      tab-position="left"
      v-model="filter.milgroup"
      @tab-click="onJournal()"
      class="my-tabs"
      v-loading="loading"
    >
      <el-tab-pane
        v-for="mg in milgroups"
        :key="mg.milgroup"
        :label="mg.milgroup.toString()"
        :name="mg.milgroup.toString()"
      >
        <el-table
          :data="journal.students"
          style="width: 100%"
          height="680"
          :default-sort="{
            prop: 'fullname',
            order: 'ascending',
          }"
          stripe
          border
        >
          <el-table-column
            width="250"
            prop="fullname"
            label="ФИО"
            show-overflow-tooltip
            fixed
          />
          <el-table-column
            v-for="d in journal.dates"
            :key="d"
            :label="formatDate(d)"
            align="center"
            min-width="100"
          >
            <template slot-scope="scope">
              <div class="absence-journal-cell">
                <el-popover
                  v-if="scope.row.absences.some((x) => x.date == d)"
                  placement="top"
                  trigger="hover"
                >
                  <el-form
                    label-position="right"
                    label-width="150px"
                    size="mini"
                    :model="scope.row.absences.find((x) => x.date == d)"
                  >
                    <el-form-item label="Тип причины: ">
                      <el-tag
                        :type="
                          tagByAbsenceType(
                            scope.row.absences.find((x) => x.date == d).type
                          )
                        "
                        disable-transitions
                      >
                        {{
                          scope.row.absences.find((x) => x.date == d).type
                            | absenceTypeFilter
                        }}
                      </el-tag>
                    </el-form-item>
                    <el-form-item label="Причина: ">
                      {{ scope.row.absences.find((x) => x.date == d).reason }}
                    </el-form-item>
                    <el-form-item label="Комментарий: ">
                      {{ scope.row.absences.find((x) => x.date == d).comment }}
                    </el-form-item>
                    <el-form-item>
                      <el-button
                        size="mini"
                        icon="el-icon-edit"
                        type="info"
                        @click="
                          onEdit(
                            scope.row.absences.find((x) => x.date == d),
                            scope.row.fullname
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
                            scope.row.absences.find((x) => x.date == d).id
                          )
                        "
                        >Удалить</el-button
                      >
                    </el-form-item>
                  </el-form>
                  <i
                    slot="reference"
                    :class="
                      iconByAbsenceStatus(
                        scope.row.absences.find((x) => x.date == d).status
                      )
                    "
                    :style="
                      colorByAbsenceStatus(
                        scope.row.absences.find((x) => x.date == d).status
                      )
                    "
                  />
                </el-popover>
                <el-button
                  v-else
                  type="text"
                  icon="el-icon-plus"
                  @click="onCreate(scope.row, d)"
                  class="create-absence-btn"
                />
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
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
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Статус: ">
          <el-switch
            :value="editAbsence.status == 'CL'"
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
import {
  getAbsenceJournal,
  patchAbsence,
  postAbsence,
  deleteAbsence,
} from "@/api/absence";
import moment from "moment";
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
  name: "Absence",
  components: {},
  data() {
    return {
      dialogVisible: false,
      loading: false,
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
        milgroup: null,
        weekday: null,
        dateRange: [
          moment().add(-3, "months").format("YYYY-MM-DD"),
          moment().format("YYYY-MM-DD"),
        ],
      },
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
      journal: {},
      weekdays: [
        { number: 0, name: "Понедельник" },
        { number: 1, name: "Вторник" },
        { number: 2, name: "Среда" },
        { number: 3, name: "Четверг" },
        { number: 4, name: "Пятница" },
        { number: 5, name: "Суббота" },
        { number: 6, name: "Воскресенье" },
      ],
    };
  },
  computed: {
    milgroups() {
      return this.$store.state.reference.milgroups.filter(
        (x) => x.weekday === this.filter.weekday
      );
    },
    milfaculties() {
      return this.$store.state.reference.milfaculties;
    },
    types() {
      return this.$store.state.reference.absenceTypes;
    },
    statuses() {
      return this.$store.state.reference.absenceStatuses;
    },
  },
  async created() {
    await this.fetchData();
    console.log(this.milgroups);
    this.filter.weekday = moment().day() - 1;
    console.log("🚀 > this.filter.weekday", this.filter.weekday);
    await this.onWeekdayChanged();
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
  methods: {
    async onWeekdayChanged() {
      this.loading = true;
      this.filter.milgroup = this.milgroups.length
        ? this.milgroups[0].milgroup.toString()
        : "0";
      await this.onJournal();
    },
    changeAbsenceStatus(absence) {
      absence.status = absence.status == "CL" ? "OP" : "CL";
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
    formatDate: (d) => moment(d).format("DD.MM.YY"),
    onCreate(student, date) {
      this.editAbsence = { status: "OP", student: student.id, date };
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
      if (this.editAbsence.id) {
        patchAbsence(this.editAbsence)
          .then(() => {
            patchSuccess("пропуска");
            this.dialogVisible = false;
            if (this.filter.milgroup) this.onJournal();
          })
          .catch((err) => patchError("пропуска", err.response.status));
      } else {
        postAbsence(this.editAbsence)
          .then(() => {
            postSuccess("пропуска");
            this.dialogVisible = false;
            if (this.filter.milgroup) this.onJournal();
          })
          .catch((err) => postError("пропуска", err.response.status));
      }
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
            deleteSuccess("пропуска");
            if (this.filter.milgroup) this.onJournal();
          })
          .catch((err) => deleteError("пропуска", err.response.status));
      });
    },
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
    async onJournal() {
      if (this.filter.milgroup > 0) {
        try {
          this.loading = true;
          this.journal = (
            await getAbsenceJournal({
              milgroup: this.filter.milgroup,
              date_from: this.filter.dateRange[0],
              date_to: this.filter.dateRange[1],
            })
          ).data;
        } catch (err) {
          getError("журнала", err.response.status);
        } finally {
          this.loading = false;
        }
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
