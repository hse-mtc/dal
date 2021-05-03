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
      <el-col :span="6">
        <el-select
          v-model="filter.type"
          clearable
          placeholder="Выберите тип взыскания"
          style="display: block"
          @change="onFilter"
        >
          <el-option
            v-for="item in types"
            :key="item.label"
            :label="item.label"
            :value="item.code"
          />
        </el-select>
      </el-col>
    </el-row>
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
    <el-row>
      <el-table
        :data="punishments"
        :default-sort="{ prop: 'date', order: 'descending' }"
        style="width: 100%"
        max-height="680"
        stripe
      >
        <el-table-column
          sortable
          label="Дата"
          sort-by="date"
          width="100"
          prop="date"
          :formatter="formatDate"
        />
        <el-table-column
          prop="student.fullname"
          sortable
          show-overflow-tooltip
          label="Студент"
        />
        <el-table-column
          prop="teacher.fullname"
          sortable
          show-overflow-tooltip
          label="Преподаватель"
        />
        <el-table-column
          prop="student.milgroup.milgroup"
          sortable
          label="Взвод"
          width="100"
        />
        <el-table-column label="Тип взыскания">
          <template slot-scope="scope">
            <el-tag
              :type="tagByPunishmentType(scope.row.type)"
              disable-transitions
            >
              {{ scope.row.type | typeFilter }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="Причина" />
        <el-table-column
          sortable
          label="Дата снятия"
          sort-by="remove_date"
          width="130"
          prop="remove_date"
          :formatter="formatRemoveDate"
        />
        <el-table-column width="150px">
          <template slot-scope="scope">
            <el-tooltip
              v-if="!scope.row.remove_date"
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
                @click="onRemove(scope.row)"
              />
            </el-tooltip>
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
          <el-select
            v-model="editPunishment.teacher"
            value-key="id"
            filterable
            style="display: block"
          >
            <el-option
              v-for="t in teachers"
              :key="t.id"
              :label="t.fullname"
              :value="t.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Тип взыскания: " required>
          <el-select
            v-model="editPunishment.type"
            placeholder="Выберите тип взыскания"
            style="display: block"
          >
            <el-option
              v-for="item in types"
              :key="item.label"
              :label="item.label"
              :value="item.code"
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
      editPunishment: {
        id: 0,
        date: "",
        type: "",
        reason: "",
        student: {
          id: 0,
        },
        teacher: {
          id: 0,
        },
      },
      editPunishmentFullname: null,
      dialogVisible: false,
      punishments: [],
      types: [
        { label: "Взыскание", code: "PU" },
        { label: "Выговор", code: "RE" },
      ],
      filter: {
        search: null,
        mg: null,
        dateRange: ["", ""],
        type: null,
      },
      students: [],
      teachers: [],
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
        milgroup: this.filter.mg !== null ? this.filter.mg.milgroup : null,
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
      this.editPunishment = {
        student: null,
        teacher: null,
        date: moment().format("YYYY-MM-DD"),
      };
      this.students = (await getStudent()).data;
      this.teachers = (await getTeacher()).data;
      this.dialogVisible = true;
    },
    async onEdit(row) {
      this.editPunishmentFullname = row.student.fullname;
      this.editPunishment = { ...row };
      this.editPunishment.student = row.student.id;
      this.editPunishment.teacher = row.teacher.id;
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
