<template>
  <div>
    <el-row class="filterRow" :gutter="20">
      <el-col :span="6">
        <el-input
          clearable
          placeholder="Поиск..."
          v-model="filter.search"
          v-on:clear="onFilter"
          v-on:keyup.native.enter="onFilter"
        />
      </el-col>
      <el-col :span="5">
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
      <el-col :span="6">
        <el-select
          v-model="filter.type"
          clearable
          placeholder="Выберите тип взыскания"
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
      <el-col :span="6">
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
        <el-table-column sortable label="Дата" width="100">
          <template slot-scope="scope">
            {{ formatDate(scope.row.date) }}
          </template>
        </el-table-column>
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
              :type="tagByPunishmentType(scope.row.punishment_type)"
              disable-transitions
              >{{ scope.row.punishment_type }}</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="Причина" />
        <el-table-column width="115px">
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
            type="date"
            placeholder="Выберите дату"
            v-model="editPunishment.date"
            style="width: 100%"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
          ></el-date-picker>
        </el-form-item>
        <el-form-item
          label="Студент"
          required
          v-if="!(editPunishment.id && editPunishment.id > 0)"
        >
          <el-select
            v-model="editPunishment.student.id"
            placeholder="Выберите студента"
            filterable
            style="display: block"
          >
            <el-option
              v-for="st in students"
              :key="st.id"
              :label="st.fullname"
              :value="st.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Преподаватель" required>
          <el-select
            v-model="editPunishment.teacher.id"
            placeholder="Выберите преподавателя"
            filterable
            style="display: block"
          >
            <el-option
              v-for="t in teachers"
              :key="t.id"
              :label="t.fullname"
              :value="t.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Тип взыскания: " required>
          <el-select
            v-model="editPunishment.punishment_type"
            placeholder="Выберите тип взыскания"
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
        <el-form-item label="Причина: ">
          <el-input
            v-model="editPunishment.reason"
            placeholder="Введите причину"
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
  getPunishment,
  deletePunishment,
  patchPunishment,
  postPunishment,
} from "@/api/punishment";

import moment from "moment";
import { getStudent } from "../../api/student";
import { getTeacher } from "../../api/teacher";

export default {
  name: "Punishment",
  data() {
    return {
      editPunishment: {
        id: 0,
        date: "",
        punishment_type: "",
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
      types: ["Взыскание", "Выговор", "Отчисление"],
      filter: {
        search: null,
        mg: null,
        dateRange: [
          moment().format("YYYY-MM-DD"),
          moment().format("YYYY-MM-DD"),
        ],
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
    formatDate: (d) => moment(d).format("DD.MM.YY"),
    onFilter() {
      getPunishment({
        date_from:
          this.filter.dateRange !== null ? this.filter.dateRange[0] : null,
        date_to:
          this.filter.dateRange !== null ? this.filter.dateRange[1] : null,
        punishment_type: this.filter.type,
        search: this.filter.search,
        milgroup: this.filter.mg !== null ? this.filter.mg.milgroup : null,
      })
        .then((response) => {
          this.punishments = response.data;
        })
        .catch(() => {});
    },
    tagByPunishmentType(type) {
      switch (type) {
        case "Отчисление":
          return "info";
        case "Выговор":
          return "danger";
        default:
          return "warning";
      }
    },
    async onCreate() {
      this.editPunishmentFullname = "Новое взыскание";
      this.editPunishment = {
        student: { id: null },
        teacher: { id: null },
        date: moment().format("YYYY-MM-DD"),
      };
      this.students = (await getStudent()).data;
      this.teachers = (await getTeacher()).data;
      this.dialogVisible = true;
    },
    async onEdit(row) {
      this.editPunishmentFullname = row.student.fullname;
      this.editPunishment = { ...row };
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
        }
      ).then(() => {
        deletePunishment({ id })
          .then(() => {
            this.$message({
              message: "Пропуск успешно удален",
              type: "success",
            });
            this.onFilter();
          })
          .catch(() => {
            this.$message({
              message: "Ошибка при удалении взыскания!",
              type: "error",
            });
          });
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
        }
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
            this.$message({
              message: "Взыскание успешно отредактировано",
              type: "success",
            });
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch(() => {
            this.$message({
              message: "Ошибка при редактировании взыскания!",
              type: "error",
            });
          });
      } else {
        postPunishment(this.editPunishment)
          .then(() => {
            this.$message({
              message: "Взыскание успешно создано",
              type: "success",
            });
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch(() => {
            this.$message({
              message: "Ошибка при создании взыскания!",
              type: "error",
            });
          });
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
