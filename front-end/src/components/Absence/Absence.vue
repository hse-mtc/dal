<template>
  <div>
    <input
      ref="attachmentUpload"
      type="file"
      hidden
      accept="image/*"
      @change="onAttachmentPicked"
    >
    <el-col :offset="1" :span="22" class="Absence">
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
                value-key="id"
                clearable
                placeholder="Выберите взвод"
                style="display: block"
                @change="onFilter"
              >
                <el-option
                  v-for="item in milgroups"
                  :key="item.id"
                  :label="item.title"
                  :value="item"
                >
                  <span style="float: left">{{ item.title }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{
                    item.milfaculty.abbreviation
                  }}</span>
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select
                v-model="filter.excuse"
                clearable
                placeholder="Выберите тип причины"
                style="display: block"
                @change="onFilter"
              >
                <el-option
                  v-for="excuse in absenceExcuses"
                  :key="excuse.value"
                  :label="excuse.label"
                  :value="excuse.value"
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
                  v-for="status in absenceStatuses"
                  :key="status.value"
                  :label="status.label"
                  :value="status.value"
                />
              </el-select>
            </el-col>
          </el-row>
          <el-row>
            <PrimeTable
              v-loading="loading || absenceExcusesAreLoading || absenceStatusesAreLoading"
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
                :field="(row) => row.student.milgroup.title"
                sortable
                header="Взвод"
                header-style="width: 100px"
                body-style="width: 100px"
                column-key="milgroup"
              />

              <PrimeColumn
                sortable
                header="Тип причины"
                column-key="excuse"
                field="excuse"
              >
                <template #body="{ data: { excuse } }">
                  <el-tag :type="tagByExcuse(excuse)" disable-transitions>
                    {{ absenceExcuseLabelFromValue(excuse) }}
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
                  {{ absenceStatusLabelFromValue(status) }}
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
                column-key="attachment"
                header-style="width: 120px"
                body-style="width: 120px; text-align: center;"
                header="Приложение"
              >
                <template #body="{ data }">
                  <AZGuard
                    v-if="data.attachment"
                    v-slot="{ disabled }"
                    :permissions="getPermissions('get', data)"
                    disable
                  >
                    <el-button
                      size="mini"
                      icon="el-icon-download"
                      type="primary"
                      circle
                      :disabled="disabled"
                      @click="onAttachmentDownload(data.attachment.image)"
                    />
                  </AZGuard>
                  <AZGuard
                    v-if="data.attachment"
                    v-slot="{ disabled }"
                    :permissions="getPermissions('delete', data)"
                    disable
                  >
                    <el-button
                      size="mini"
                      icon="el-icon-document-delete"
                      type="danger"
                      circle
                      :disabled="disabled"
                      @click="onAttachmentDelete(data.attachment.id)"
                    />
                  </AZGuard>
                  <AZGuard
                    v-if="!data.attachment"
                    v-slot="{ disabled }"
                    :permissions="getPermissions('patch', data)"
                    disable
                  >
                    <el-button
                      size="mini"
                      icon="el-icon-camera"
                      type="primary"
                      circle
                      :disabled="disabled"
                      @click="onAttachmentUpload(data.id)"
                    />
                  </AZGuard>
                </template>
              </PrimeColumn>
              <PrimeColumn
                column-key="buttons"
                header-style="width: 160px"
                body-style="width: 160px; text-align: center;"
              >
                <template #body="{ data }">
                  <AZGuard
                    v-slot="{ disabled }"
                    :permissions="getPermissions('patch', data)"
                    disable
                  >
                    <el-button
                      size="mini"
                      icon="el-icon-edit"
                      type="info"
                      circle
                      :disabled="disabled"
                      @click="onEdit(data, data.student.fullname)"
                    />
                  </AZGuard>
                  <AZGuard
                    v-slot="{ disabled }"
                    :permissions="getPermissions('delete', data)"
                    disable
                  >
                    <el-button
                      size="mini"
                      icon="el-icon-delete"
                      type="danger"
                      circle
                      :disabled="disabled"
                      @click="handleDelete(data.id)"
                    />
                  </AZGuard>
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
  getAbsence,
  patchAbsence,
  deleteAbsence,
  deleteAbsenceAttachment,
} from "@/api/absence";
import moment from "moment";
import {
  getError,
  patchError,
  deleteError,
  patchSuccess,
  deleteSuccess,
} from "@/utils/message";
import { ReferenceModule, UserModule } from "@/store";
import { AbsenceExcusesMixin, AbsenceStatusesMixin } from "@/mixins/absences";
import GenericForm from "@/common/Form/index.vue";
import AbsenceJournal from "./AbsenceJournal/AbsenceJournal.vue";

export default {
  name: "Absence",
  components: {
    AbsenceJournal,
    GenericForm,
  },
  mixins: [AbsenceExcusesMixin, AbsenceStatusesMixin],
  data() {
    return {
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
      uploadAttachmentAbsenceId: 0,
      editAbsenceFullname: "",
      filter: {
        excuse: null,
        status: null,
        dateRange: [
          moment().format("YYYY-MM-DD"),
          moment().format("YYYY-MM-DD"),
        ],
        search: null,
        mg: {},
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

      rules: {
        excuse: [{ required: true, message: "Обязательное поле" }],
        reason: [{ required: true, message: "Обязательное поле" }],
      },
    };
  },
  computed: {
    milgroups() {
      return ReferenceModule.milgroups;
    },
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    userMilgroups() {
      return UserModule.personMilgroups;
    },
    userId() {
      return UserModule.personId;
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
  },
  created() {
    this.onFilter();
  },
  methods: {
    getPermissions(method, data) {
      return [
        `absences.${method}.all`,
        {
          codename: `absences.${method}.milfaculty`,
          validator: () => this.userMilfaculty === data.student.milgroup.milfaculty,
        },
        {
          codename: `absences.${method}.milgroup`,
          validator: () => this.userMilgroups.some(
            x => x === data.student.milgroup.milgroup,
          ),
        },
      ];
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
    dateField: row => moment(row.date).format("DD.MM.YY"),
    async onFilter() {
      try {
        this.loading = true;
        this.absences = (
          await getAbsence({
            excuse: this.filter.excuse,
            status: this.filter.status,
            search: this.filter.search,
            milgroup: this.filter.mg?.id,
            date_from: this.filter.dateRange ? this.filter.dateRange[0] : undefined,
            date_to: this.filter.dateRange ? this.filter.dateRange[1] : undefined,
          })
        ).data;
      } catch (err) {
        console.log(err);
        getError("пропусков", err.response?.status);
      } finally {
        this.loading = false;
      }
    },
    onEdit(row, fn) {
      this.editAbsence = { ...row };
      this.editAbsence.attachment = undefined;
      this.editAbsence.student = undefined;
      this.editAbsenceFullname = fn;
      this.dialogVisible = true;
    },
    onAttachmentDownload(file) {
      window.open(file, "_blank");
    },
    onAttachmentUpload(id) {
      this.$refs.attachmentUpload.value = null;
      this.uploadAttachmentAbsenceId = id;
      this.$refs.attachmentUpload.click();
    },
    async onAttachmentPicked() {
      const formData = new FormData();
      if (this.$refs.attachmentUpload.files[0]) {
        formData.set("image", this.$refs.attachmentUpload.files[0]);
      }
      try {
        await patchAbsence(this.uploadAttachmentAbsenceId, formData);
        patchSuccess("приложения");
        this.dialogVisible = false;
        this.onFilter();
      } catch (err) {
        patchError("приложения", err.response?.status);
      }
    },
    onAttachmentDelete(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить приложение?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(async() => {
        try {
          await deleteAbsenceAttachment(id);
          deleteSuccess("приложения");
          this.onFilter();
        } catch (err) {
          deleteError("приложения", err.response.status);
        }
      });
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
      patchAbsence(this.editAbsence.id, this.editAbsence)
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
