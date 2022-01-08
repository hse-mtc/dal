<template>
  <div>
    <el-row class="filterRow">
      <el-col :span="5">
        <el-select
          v-model="filter.weekday"
          placeholder="Выберите учебный день"
          style="display: block"
          @change="onWeekdayChanged"
        >
          <el-option
            v-for="(value, key) in WEEKDAYS"
            :key="key"
            :label="value"
            :value="key"
          />
        </el-select>
      </el-col>
      <el-col :offset="1" :span="8">
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
          style="width: auto"
          @change="onJournal"
        />
      </el-col>
    </el-row>
    <el-tabs
      v-model="filter.milgroup"
      v-loading="loading || absenceExcusesAreLoading || absenceStatusesAreLoading"
      tab-position="left"
      class="my-tabs"
      @tab-click="onJournal"
    >
      <el-tab-pane
        v-for="mg in milgroups"
        :key="mg.id"
        :label="mg.title.toString()"
        :name="mg.id.toString()"
      >
        <PrimeTable
          :value="tableData"
          scrollable
          scroll-height="680px"
          sort-field="fullname"
          :sort-order="1"
          class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
          frozen-width="300px"
        >
          <PrimeColumn
            width="250"
            header-style="width: 250px"
            body-style="width: 250px; height: 90px"
            field="fullname"
            header="ФИО"
            frozen
            column-key="fullname"
          />
          <PrimeColumn
            v-for="d in journal.dates"
            :key="d"
            :column-key="d"
            :header="formatDate(d)"
            header-style="width: 100px; text-align: center;"
            body-style="width: 100px; height: 90px; text-align: center;"
          >
            <template #body="{ data }">
              <div class="absence-journal-cell">
                <el-popover
                  v-if="data[d]"
                  placement="top"
                  trigger="hover"
                >
                  <GenericForm
                    v-model="data[d]"
                    :fields="getPreviewFields(data[d])"
                    left-label
                    label-width="150px"
                  >
                    <template #buttons>
                      <center>
                        <AZGuard :permissions="getPermissions('patch')">
                          <el-button
                            size="mini"
                            icon="el-icon-edit"
                            type="info"
                            @click="onEdit(data[d], data.fullname)"
                          >
                            Редактировать
                          </el-button>
                        </AZGuard>
                        <AZGuard :permissions="getPermissions('delete')">
                          <el-button
                            size="mini"
                            icon="el-icon-delete"
                            type="danger"
                            @click="handleDelete(data[d].id)"
                          >
                            Удалить
                          </el-button>
                        </AZGuard>
                      </center>
                    </template>
                  </GenericForm>
                  <i
                    slot="reference"
                    :class="iconByAbsenceStatus(data[d].status)"
                    :style="colorByAbsenceStatus(data[d].status)"
                  />
                </el-popover>
                <AZGuard v-else :permissions="getPermissions('post')">
                  <el-button
                    type="text"
                    icon="el-icon-plus"
                    class="create-absence-btn"
                    @click="onCreate(data, d)"
                  />
                </AZGuard>
              </div>
            </template>
          </PrimeColumn>
        </PrimeTable>
      </el-tab-pane>
    </el-tabs>
    <el-dialog
      :title="editAbsenceFullname"
      :visible.sync="dialogVisible"
      :before-close="handleClose"
    >
      <GenericForm
        v-model="editAbsence"
        :fields="fields"
        :rules="rules"
        :on-submit="handleAccept"
        left-label
        label-width="150px"
      >
        <template #buttons="{ validate }">
          <span style="display: flex; justify-content: flex-end">
            <el-button @click="dialogVisible = false">Отмена</el-button>
            <el-button type="primary" @click="validate">Применить</el-button>
          </span>
        </template>
      </GenericForm>
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
import { ReferenceModule, UserModule } from "@/store";
import { WEEKDAYS } from "@/utils/enums";
import GenericForm from "@/common/Form/index.vue";
import { AbsenceExcusesMixin, AbsenceStatusesMixin } from "@/mixins/absences";

export default {
  name: "Absence",
  components: { GenericForm },
  mixins: [AbsenceExcusesMixin, AbsenceStatusesMixin],
  data() {
    return {
      WEEKDAYS,
      dialogVisible: false,
      loading: false,
      editAbsence: {
        id: 0,
        date: "",
        excuse: "",
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
        milgroup: null,
        weekday: null,
        dateRange: [
          moment()
            .add(-3, "months")
            .format("YYYY-MM-DD"),
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

      rules: {
        excuse: [{ required: true, message: "Обязательное поле" }],
        reason: [{ required: true, message: "Обязательное поле" }],
      },
    };
  },
  computed: {
    milgroups() {
      return ReferenceModule.milgroups.filter(
        x => x.weekday === +this.filter.weekday,
      );
    },
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    userMilgroups() {
      return UserModule.personMilgroups;
    },

    fields() {
      return {
        excuse: {
          component: "select",
          title: "Тип причины",
          props: {
            options: Object.values(this.absenceExcuses),
          },
        },
        status: {
          component: "switch",
          title: "Статус",
          props: {
            trueValue: "CL",
            falseValue: "OP",
            activeText: "Закрыт",
            inactiveText: "Открыт",
          },
        },
        reason: {
          component: "text",
          title: "Причина",
          props: {
            placeholder: "Введите причину",
          },
        },
        comment: {
          component: "text",
          title: "Комментарий",
          props: {
            placeholder: "Введите комментарий",
            isTextArea: true,
          },
        },
      };
    },

    tableData() {
      if (this.loading) {
        return [];
      }

      const { students, dates } = this.journal;

      return students.map(student => ({
        id: student.id,
        fullname: student.fullname,
        ...dates.reduce((memo, date) => {
          const rawAbsence = student.absences.find(absence => absence.date === date);
          if (rawAbsence) {
            return {
              ...memo,
              [date]: {
                ...rawAbsence,
              },
            };
          }

          return memo;
        }, {}),
      }));
    },
  },
  async created() {
    this.filter.weekday = moment().day() - 1;
    await this.onWeekdayChanged();
  },
  methods: {
    getPermissions(method) {
      return [
        `absences.${method}.all`,
        {
          codename: `absences.${method}.milfaculty`,
          validator: () => this.userMilfaculty === this.journal.milgroup.milfaculty,
        },
        {
          codename: `absences.${method}.milgroup`,
          validator: () => this.userMilgroups.some(
            x => x === this.journal.milgroup.milgroup,
          ),
        },
      ];
    },
    async onWeekdayChanged() {
      this.loading = true;
      this.filter.milgroup = this.milgroups.length
        ? this.milgroups[0].id.toString()
        : "0";
      await this.onJournal();
    },
    // TODO(TmLev): Send this info from back-end in "choices/.../" views.
    tagByExcuse(excuse) {
      switch (excuse) {
        case "IL":
          return "danger";
        case "LA":
          return "warning";
        default:
          return "success";
      }
    },
    // TODO(TmLev): Send this info from back-end in "choices/.../" views.
    iconByAbsenceStatus(status) {
      switch (status) {
        case "OP":
          return "el-icon-circle-close";
        default:
          return "el-icon-circle-check";
      }
    },
    // TODO(TmLev): Send this info from back-end in "choices/.../" views.
    colorByAbsenceStatus(status) {
      switch (status) {
        case "OP":
          return "color: red;";
        default:
          return "color: green;";
      }
    },
    formatDate: d => moment(d).format("DD.MM.YY"),
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
        },
      )
        .then(() => {
          this.dialogVisible = false;
        });
    },
    handleAccept() {
      if (this.editAbsence.id) {
        patchAbsence(this.editAbsence)
          .then(() => {
            patchSuccess("пропуска");
            this.dialogVisible = false;
            if (this.filter.milgroup) this.onJournal();
          })
          .catch(err => patchError("пропуска", err.response.status));
      } else {
        postAbsence(this.editAbsence)
          .then(() => {
            postSuccess("пропуска");
            this.dialogVisible = false;
            if (this.filter.milgroup) this.onJournal();
          })
          .catch(err => postError("пропуска", err.response.status));
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
        },
      ).then(() => {
        deleteAbsence({ id })
          .then(() => {
            deleteSuccess("пропуска");
            if (this.filter.milgroup) this.onJournal();
          })
          .catch(err => deleteError("пропуска", err.response.status));
      });
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
    getPreviewFields(data) {
      return {
        excuse: {
          component: "el-tag",
          title: "Тип причины",
          props: {
            type: this.tagByExcuse(data.excuse),
            disableTransitions: true,
          },
          display: this.absenceExcuseLabelFromValue,
        },
        reason: {
          component: "span",
          title: "Причина",
        },
        comment: {
          component: "span",
          title: "Комментарий",
        },
      };
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
