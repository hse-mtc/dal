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
      v-loading="loading"
      tab-position="left"
      class="my-tabs"
      @tab-click="onJournal()"
    >
      <el-tab-pane
        v-for="mg in milgroups"
        :key="mg.id"
        :label="mg.title.toString()"
        :name="mg.id.toString()"
      >
        <PrimeTable
          :value="journal.students"
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
                  v-if="data.absences.some((x) => x.date === d)"
                  placement="top"
                  trigger="hover"
                >
                  <el-form
                    label-position="right"
                    label-width="150px"
                    size="mini"
                    :model="data.absences.find((x) => x.date === d)"
                  >
                    <el-form-item label="Тип причины: ">
                      <el-tag
                        :type="
                          tagByExcuse(
                            data.absences.find((x) => x.date === d).excuse,
                          )
                        "
                        disable-transitions
                      >
                        {{
                          EXCUSES[data.absences.find((x) => x.date === d).excuse]
                        }}
                      </el-tag>
                    </el-form-item>
                    <el-form-item label="Причина: ">
                      {{ data.absences.find((x) => x.date === d).reason }}
                    </el-form-item>
                    <el-form-item label="Комментарий: ">
                      {{ data.absences.find((x) => x.date === d).comment }}
                    </el-form-item>
                    <el-form-item>
                      <AZGuard :permissions="getPermissions('patch')">
                        <el-button
                          size="mini"
                          icon="el-icon-edit"
                          type="info"
                          @click="
                            onEdit(
                              data.absences.find((x) => x.date === d),
                              data.fullname,
                            )
                          "
                        >
                          Редактировать
                        </el-button>
                      </AZGuard>
                      <AZGuard :permissions="getPermissions('delete')">
                        <el-button
                          size="mini"
                          icon="el-icon-delete"
                          type="danger"
                          @click="
                            handleDelete(
                              data.absences.find((x) => x.date === d).id,
                            )
                          "
                        >
                          Удалить
                        </el-button>
                      </AZGuard>
                    </el-form-item>
                  </el-form>
                  <i
                    slot="reference"
                    :class="
                      iconByAbsenceStatus(
                        data.absences.find((x) => x.date === d).status,
                      )
                    "
                    :style="
                      colorByAbsenceStatus(
                        data.absences.find((x) => x.date === d).status,
                      )
                    "
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
            v-model="editAbsence.excuse"
            placeholder="Выберите тип причины"
            style="display: block"
          >
            <el-option
              v-for="value, key in EXCUSES"
              :key="key"
              :label="value"
              :value="key"
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
import { WEEKDAYS, EXCUSES, ABSENCE_STATUSES } from "@/utils/enums";

export default {
  name: "Absence",
  data() {
    return {
      EXCUSES,
      WEEKDAYS,
      ABSENCE_STATUSES,
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
    changeAbsenceStatus(absence) {
      // todo
      // eslint-disable-next-line no-param-reassign
      absence.status = absence.status === "CL" ? "OP" : "CL";
    },
    tagByExcuse(excuse) {
      switch (excuse) {
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
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
