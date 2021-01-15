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
          placeholder="Выберите тип поощрения"
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
          Новое поощрение
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-table
        :data="encouragements"
        :default-sort="{ prop: 'date', order: 'descending' }"
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
        <el-table-column label="Тип поощрения">
          <template slot-scope="scope">
            <el-tag
              :type="tagByEncouragementType(scope.row.encouragement_type)"
              disable-transitions
              >{{ scope.row.encouragement_type }}</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="Причина" />
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
    <el-dialog
      :title="editEncouragementFullname"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editEncouragement"
      >
        <el-form-item label="Дата" required>
          <el-date-picker
            type="date"
            placeholder="Выберите дату"
            v-model="editEncouragement.date"
            style="width: 100%"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
          ></el-date-picker>
        </el-form-item>
        <el-form-item
          label="Студент"
          required
          v-if="!(editEncouragement.id && editEncouragement.id > 0)"
        >
          <el-select
            v-model="editEncouragement.student.id"
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
            v-model="editEncouragement.teacher.id"
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
        <el-form-item label="Тип поощрения: " required>
          <el-select
            v-model="editEncouragement.encouragement_type"
            placeholder="Выберите тип поощрения"
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
            v-model="editEncouragement.reason"
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
  getEncouragement,
  deleteEncouragement,
  patchEncouragement,
  postEncouragement,
} from "@/api/encouragement";

import moment from "moment";
import { getStudent } from "../../api/student";
import { getTeacher } from "../../api/teacher";

export default {
  name: "Encouragement",
  data() {
    return {
      editEncouragement: {
        id: 0,
        date: "",
        encouragement_type: "",
        reason: "",
        student: {
          id: 0,
        },
        teacher: {
          id: 0,
        },
      },
      editEncouragementFullname: null,
      dialogVisible: false,
      encouragements: [],
      types: ["Благодарность", "Снятие взыскания"],
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
    formatDate: (row) => moment(row.date).format("DD.MM.YY"),
    onFilter() {
      getEncouragement({
        date_from:
          this.filter.dateRange !== null ? this.filter.dateRange[0] : null,
        date_to:
          this.filter.dateRange !== null ? this.filter.dateRange[1] : null,
        encouragement_type: this.filter.type,
        search: this.filter.search,
        milgroup: this.filter.mg !== null ? this.filter.mg.milgroup : null,
      })
        .then((response) => {
          this.encouragements = response.data;
        })
        .catch(() => {});
    },
    tagByEncouragementType(type) {
      switch (type) {
        case "Благодарность":
          return "";
        case "Снятие взыскания":
          return "success";
      }
    },
    async onCreate() {
      this.editEncouragementFullname = "Новое поощрение";
      this.editEncouragement = {
        student: { id: null },
        teacher: { id: null },
        date: moment().format("YYYY-MM-DD"),
      };
      this.students = (await getStudent()).data;
      this.teachers = (await getTeacher()).data;
      this.dialogVisible = true;
    },
    async onEdit(row) {
      this.editEncouragementFullname = row.student.fullname;
      this.editEncouragement = { ...row };
      this.students = (await getStudent()).data;
      this.teachers = (await getTeacher()).data;
      this.dialogVisible = true;
    },
    handleDelete(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить поощрение?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        }
      ).then(() => {
        deleteEncouragement({ id })
          .then(() => {
            this.$message({
              message: "Поощрение успешно удалено",
              type: "success",
            });
            this.onFilter();
          })
          .catch(() => {
            this.$message({
              message: "Ошибка при удалении поошрения!",
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
      if (this.editEncouragement.id && this.editEncouragement.id > 0) {
        patchEncouragement(this.editEncouragement)
          .then(() => {
            this.$message({
              message: "Поощрение успешно отредактировано",
              type: "success",
            });
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch(() => {
            this.$message({
              message: "Ошибка при редактировании поощрение!",
              type: "error",
            });
          });
      } else {
        postEncouragement(this.editEncouragement)
          .then(() => {
            this.$message({
              message: "Поощрение успешно создано",
              type: "success",
            });
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch(() => {
            this.$message({
              message: "Ошибка при создании поощрения!",
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
