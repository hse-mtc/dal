<template>
  <div>
    <el-row class="filterRow" :gutter="20" style="margin-bottom: 15px">
      <el-col :span="8">
        <el-input
          clearable
          placeholder="Поиск..."
          v-model="filter.search"
          v-on:clear="onFilter"
          v-on:keyup.native.enter="onFilter"
        ></el-input>
      </el-col>
      <el-col :span="7">
        <el-select
          v-model="filter.milgroup"
          value-key="milgroup"
          clearable
          placeholder="Выберите взвод"
          v-on:change="onFilter"
          style="display: block"
        >
          <el-option
            v-for="item in milgroups"
            :key="item.milgroup"
            :value="item.milgroup"
          >
            <span style="float: left">{{ item.milgroup }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{
              item.milfaculty
            }}</span>
          </el-option>
        </el-select>
      </el-col>
      <el-col :span="7">
        <el-select
          v-model="filter.status"
          clearable
          placeholder="Выберите статус"
          v-on:change="onFilter"
          style="display: block"
        >
          <el-option
            v-for="item in statuses"
            :key="item.code"
            :label="item.label"
            :value="item.code"
          >
          </el-option>
        </el-select>
      </el-col>
      <el-col :span="2">
        <el-button type="text" @click="clearFilter">Сбросить</el-button>
      </el-col>
    </el-row>
    <el-row class="table">
      <el-table
        max-height="600px"
        :data="students"
        :default-sort="{ prop: 'milgroup.milgroup', order: 'ascending' }"
        stripe
        v-loading="loading"
      >
        <el-table-column
          width="300px"
          sortable
          show-overflow-tooltip
          prop="fullname"
          label="ФИО"
        >
        </el-table-column>
        <el-table-column sortable prop="milgroup.milgroup" label="Взвод">
        </el-table-column>
        <el-table-column prop="milgroup.milfaculty" label="Цикл">
        </el-table-column>
        <el-table-column
          width="300px"
          show-overflow-tooltip
          prop="university_info.program.program"
          label="Программа"
        >
        </el-table-column>
        <el-table-column label="Дата рождения">
          <template slot-scope="scope">
            {{ scope.row.birth_info ? scope.row.birth_info.date : null | dateFilter }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="Статус" show-overflow-tooltip>
          <template slot-scope="scope">
            {{ scope.row.status | statusFilter }}
          </template>
        </el-table-column>
        <el-table-column label="" width="120px">
          <template slot-scope="scope">
            <el-button
              size="mini"
              icon="el-icon-edit"
              type="info"
              circle
              @click="onEdit(scope.row)"
            ></el-button>
            <el-button
              size="mini"
              icon="el-icon-delete"
              type="danger"
              circle
              @click="onDelete(scope.row.id)"
            ></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
    <Student
      v-model="modal"
      @closeModal="closeModal"
      @submitModal="clearFilter"
      :student="editStudent"
    />
  </div>
</template>

<script>
import Student from "../Student/Student";
import moment from "moment";
import { getError, deleteError, deleteSuccess } from "@/utils/message";
import { getStudent, deleteStudent } from "@/api/students";

export default {
  name: "Students",
  components: { Student },
  data() {
    return {
      loading: false,
      filter: {
        search: null,
        milgroup: null,
        status: "ST",
      },
      students: [],
      modal: false,
      statuses: [
        { code: "ST", label: "Обучающийся" },
        { code: "EX", label: "Отчислен" },
        { code: "GR", label: "Выпустился" },
      ],
      milgroups: [
        {
          milgroup: 1807,
          milfaculty: "ВКС",
        },
        {
          milgroup: 1808,
          milfaculty: "ВКС",
        },
        {
          milgroup: 1809,
          milfaculty: "ВКС",
        },
      ],
      milfaculties: ["Разведка", "Сержанты", "ВКС", "РВСН"],
      editStudent: {},
    };
  },
  filters: {
    statusFilter(value) {
      switch (value) {
        case "AP":
          return "Абитуриент";
        case "ST":
          return "Обучающийся";
        case "EX":
          return "Отчислен";
        case "GR":
          return "Выпустился";
        default:
          return "Ошибка";
      }
    },
    dateFilter(value) {
      if (value) return moment(value).format("DD.MM.YYYY");
      return "Нет данных";
    },
  },
  async created() {
    await this.onFilter();
  },
  methods: {
    closeModal() {
      this.modal = false;
      document
        .getElementById("main-container")
        .classList.remove("stop-scrolling");
      this.editStudent = {};
    },
    openModal() {
      this.modal = true;
      document.getElementById("main-container").classList.add("stop-scrolling");
    },
    async onFilter() {
      try {
        this.loading = true;
        this.students = (await getStudent(this.filter)).data;
      } catch (err) {
        getError("студентов", err.response.status);
      }
      finally {
        this.loading = false;
      }
    },
    async clearFilter() {
      for (let key in this.filter) {
        this.filter[key] = null;
      }
      await this.onFilter();
    },
    onDelete(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить студента?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        }
      ).then(async () => {
        try {
          await deleteStudent(id);
          deleteSuccess("студента");
          await this.onFilter();
        } catch (err) {
          deleteError("студента", err.response.status);
        }
      });
    },
    onEdit(row) {
      this.editStudent = { ...row };
      this.openModal();
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
