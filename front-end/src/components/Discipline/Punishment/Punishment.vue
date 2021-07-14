<template>
  <div>
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
      <el-col :span="6">
        <el-input
          v-model="filter.search"
          clearable
          placeholder="Поиск..."
          @clear="onFilter"
          @keyup.native.enter="onFilter"
        />
      </el-col>
      <el-col :span="5">
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
      <el-col :span="6">
        <el-select
          v-model="filter.type"
          clearable
          placeholder="Выберите тип взыскания"
          style="display: block"
          @change="onFilter"
        >
          <el-option
            v-for="value, key in PUNISHMENT_TYPES"
            :key="key"
            :label="value"
            :value="key"
          />
        </el-select>
      </el-col>
    </el-row>
    <AZGuard
      :permissions="[
        'punishments.post.all',
        'punishments.post.milfaculty',
        'punishments.post.milgroup',
        'punishments.post.self',
      ]"
    >
      <el-row class="addRow">
        <el-col :span="24">
          <el-button
            class="addBtn"
            type="primary"
            icon="el-icon-plus"
            @click="onCreate"
          >
            Новое взыскание
          </el-button>
        </el-col>
      </el-row>
    </AZGuard>
    <el-row>
      <PrimeTable
        :value="punishments"
        :sort-field="formatDate"
        :sort-order="-1"
        scrollable
        scroll-height="680"
        class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
      >
        <PrimeColumn
          sortable
          header="Дата"
          :field="formatDate"
          column-key="date"
        />
        <PrimeColumn
          :field="(row) => row.student.fullname"
          sortable
          header="Студент"
          column-key="fullname"
        />
        <PrimeColumn
          :field="(row) => row.teacher.fullname"
          sortable
          header="Преподаватель"
          column-key="teacher"
        />
        <PrimeColumn
          :field="(row) => row.student.milgroup.title"
          sortable
          header="Взвод"
          header-style="width: 100px"
          body-style="width: 100px"
          column-key="milgroup"
        />
        <PrimeColumn header="Тип взыскания" column-key="type">
          <template #body="{ data }">
            <el-tag :type="tagByPunishmentType(data.type)" disable-transitions>
              {{ PUNISHMENT_TYPES[data.type] }}
            </el-tag>
          </template>
        </PrimeColumn>
        <PrimeColumn field="reason" header="Причина" column-key="reason" />
        <PrimeColumn
          sortable
          header="Дата снятия"
          header-style="width: 130px"
          body-style="width: 130px"
          :field="formatRemoveDate"
          column-key="remove-date"
        />
        <PrimeColumn
          header-style="width: 150px"
          body-style="width: 150px; text-align: center;"
          column-key="buttons"
        >
          <template #body="{ data }">
            <AZGuard
              v-slot="{ disabled }"
              :permissions="getPermissions('patch', data)"
              disable
            >
              <el-tooltip
                v-if="!data.remove_date"
                class="item"
                effect="dark"
                content="Снять взыскание"
                placement="top"
              >
                <el-button
                  size="mini"
                  icon="el-icon-remove-outline"
                  type="warning"
                  circle
                  :disabled="disabled"
                  @click="onRemove(data)"
                />
              </el-tooltip>
            </AZGuard>
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
                @click="onEdit(data)"
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
    <el-dialog
      :title="editPunishmentFullname"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editPunishment"
      >
        <el-form-item label="Дата" required>
          <el-date-picker
            v-model="editPunishment.date"
            type="date"
            placeholder="Выберите дату"
            style="width: 100%"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item
          v-if="!(editPunishment.id && editPunishment.id > 0)"
          label="Студент"
          required
        >
          <el-select
            v-model="editPunishment.student"
            value-key="id"
            placeholder="Выберите студента"
            filterable
            style="display: block"
          >
            <el-option
              v-for="st in students"
              :key="st.id"
              :label="st.fullname"
              :value="st.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Преподаватель" required>
          <AZGuard
            v-slot="{ disabled }"
            :permissions="[
              'punishments.post.all',
              'punishments.post.milfaculty',
            ]"
            disable
          >
            <el-select
              v-model="editPunishment.teacher"
              value-key="id"
              filterable
              style="display: block"
              :disabled="disabled"
            >
              <el-option
                v-for="t in teachers"
                :key="t.id"
                :label="t.fullname"
                :value="t.id"
              />
            </el-select>
          </AZGuard>
        </el-form-item>
        <el-form-item label="Тип взыскания: " required>
          <el-select
            v-model="editPunishment.type"
            placeholder="Выберите тип взыскания"
            style="display: block"
          >
            <el-option
              v-for="value, key in PUNISHMENT_TYPES"
              :key="key"
              :label="value"
              :value="key"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Причина: " required>
          <el-input
            v-model="editPunishment.reason"
            placeholder="Введите причину"
          />
        </el-form-item>
        <el-form-item>
          <el-checkbox
            :value="editPunishment.remove_date !== null"
            border
            @change="onRemovePunishmentCheckboxClick"
          >
            {{
              editPunishment.remove_date !== null
                ? "Взыскание снято"
                : "Взыскание НЕ снято"
            }}
          </el-checkbox>
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
  getPunishment,
  deletePunishment,
  patchPunishment,
  postPunishment,
} from "@/api/punishment";

import moment from "moment";
import { getStudent } from "@/api/students";
import { getTeacher } from "@/api/teachers";
import {
  getError,
  postError,
  patchError,
  deleteError,
  postSuccess,
  patchSuccess,
  deleteSuccess,
} from "@/utils/message";
import { UserModule, ReferenceModule } from "@/store";
import { PUNISHMENT_TYPES } from "@/utils/enums";

export default {
  name: "Punishment",
  filters: {
    typeFilter(value) {
      switch (value) {
        case "PU":
          return "Взыскание";
        case "RE":
          return "Выговор";
        default:
          return "Ошибка";
      }
    },
  },
  data() {
    return {
      PUNISHMENT_TYPES,
      editPunishment: {},
      editPunishmentFullname: null,
      dialogVisible: false,
      punishments: [],
      filter: {
        search: null,
        mg: null,
        dateRange: ["", ""],
        type: null,
      },
      students: [],
      teachers: [],
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
  },
  created() {
    this.onFilter();
  },
  methods: {
    getPermissions(method, data) {
      return [
        `punishments.${method}.all`,
        {
          codename: `punishments.${method}.milfaculty`,
          validator: () => this.userMilfaculty === data.student.milgroup.milfaculty,
        },
        {
          codename: `punishments.${method}.milgroup`,
          validator: () => this.userMilgroups.some(
            x => x === data.student.milgroup.milgroup,
          ),
        },
        {
          codename: `punishments.${method}.self`,
          validator: () => this.userId === data.teacher.id,
        },
      ];
    },
    formatDate: row => moment(row.date).format("DD.MM.YY"),
    formatRemoveDate: row => (row.remove_date ? moment(row.remove_date).format("DD.MM.YY") : null),
    onFilter() {
      getPunishment({
        date_from:
          this.filter.dateRange !== null ? this.filter.dateRange[0] : null,
        date_to:
          this.filter.dateRange !== null ? this.filter.dateRange[1] : null,
        type: this.filter.type,
        search: this.filter.search,
        milgroup: this.filter.mg?.id,
      })
        .then(response => {
          this.punishments = response.data;
        })
        .catch(err => getError("взысканий", err.response.status));
    },
    tagByPunishmentType(type) {
      switch (type) {
        case "RE":
          return "danger";
        default:
          return "warning";
      }
    },
    async onCreate() {
      this.editPunishmentFullname = "Новое взыскание";
      this.students = (await getStudent()).data;
      this.teachers = (await getTeacher()).data;
      this.editPunishment = {
        student: null,
        teacher: this.teachers.find(x => x.id === this.userId)?.id,
        date: moment().format("YYYY-MM-DD"),
        remove_date: null,
      };
      this.dialogVisible = true;
    },
    async onEdit(row) {
      this.editPunishmentFullname = row.student.fullname;
      this.editPunishment = {
        ...row,
        student: row.student.id,
        teacher: row.teacher.id,
      };
      this.students = (await getStudent()).data;
      this.teachers = (await getTeacher()).data;
      this.dialogVisible = true;
    },
    handleDelete(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить взыскание?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(() => {
        deletePunishment({ id })
          .then(() => {
            deleteSuccess("взыскания");
            this.onFilter();
          })
          .catch(err => deleteError("взыскания", err.response.status));
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
      if (this.editPunishment.id && this.editPunishment.id > 0) {
        patchPunishment(this.editPunishment)
          .then(() => {
            patchSuccess("взыскания");
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch(err => patchError("взыскания", err.response.status));
      } else {
        postPunishment(this.editPunishment)
          .then(() => {
            postSuccess("взыскания");
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch(err => postError("взыскания", err.response.status));
      }
    },
    onRemove(punishment) {
      this.$confirm(
        "Вы уверены, что хотите снять взыскание?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(() => {
        /* eslint-disable no-param-reassign */
        punishment.remove_date = moment().format("YYYY-MM-DD");
        punishment.student = punishment.student.id;
        punishment.teacher = punishment.teacher.id;
        patchPunishment(punishment)
          .then(() => {
            patchSuccess("взыскания");
            this.onFilter();
          })
          .catch(err => patchError("взыскания", err.response.status));
      });
    },
    onRemovePunishmentCheckboxClick() {
      if (this.editPunishment.remove_date != null) {
        this.editPunishment.remove_date = null;
      } else {
        this.editPunishment.remove_date = moment().format("YYYY-MM-DD");
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
