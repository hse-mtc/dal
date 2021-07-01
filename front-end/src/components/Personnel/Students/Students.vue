<template>
  <div>
    <el-row class="filterRow" :gutter="20" style="margin-bottom: 15px">
      <el-col :span="8">
        <el-input
          v-model="filter.search"
          clearable
          placeholder="Поиск..."
          @clear="onFilter"
          @keyup.native.enter="onFilter"
        />
      </el-col>
      <el-col :span="7">
        <el-select
          v-model="filter.milgroup"
          value-key="milgroup"
          clearable
          placeholder="Выберите взвод"
          style="display: block"
          @change="onFilter"
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
      <el-col :span="2">
        <el-button type="text" @click="clearFilter">
          Сбросить
        </el-button>
      </el-col>
    </el-row>
    <el-row class="table">
      <PrimeTable
        v-loading="loading"
        scrollable
        scroll-height="600px"
        :value="students"
        :sort-field="milgroupField"
        :sort-order="1"
        class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
      >
        <PrimeColumn
          field="fullname"
          header="ФИО"
          sortable
          header-style="width: 300px"
          body-style="width: 300px"
        />
        <PrimeColumn
          sortable
          :field="milgroupField"
          header="Взвод"
        />
        <PrimeColumn
          :field="row => row.milgroup.milfaculty"
          header="Цикл"
        />
        <PrimeColumn
          :field="row => row.university_info.program.program"
          header="Программа"
          header-style="width: 300px"
          body-style="width: 300px"
        />
        <PrimeColumn
          :field="row => dateFilter(row.birth_info && row.birth_info.date)"
          header="Дата рождения"
        />
        <PrimeColumn
          :field="row => statusFilter(row.status)"
          header="Статус"
          header-style="width: 150px"
          body-style="width: 150px"
        />
        <PrimeColumn>
          <template #body="{ data }">
            <el-button
              size="mini"
              icon="el-icon-edit"
              type="info"
              circle
              @click="onEdit(data)"
            />
            <el-button
              size="mini"
              icon="el-icon-delete"
              type="danger"
              circle
              @click="onDelete(data)"
            />
          </template>
        </PrimeColumn>
      </PrimeTable>
    </el-row>
    <Student
      v-model="modal"
      :student="editStudent"
      @closeModal="closeModal"
      @submitModal="clearFilter"
    />
  </div>
</template>

<script>
import moment from "moment";
import { getError, deleteError, deleteSuccess } from "@/utils/message";
import { getStudent, deleteStudent } from "@/api/students";
import Student from "../Student/Student.vue";

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
      } finally {
        this.loading = false;
      }
    },
    async clearFilter() {
      Object.keys(this.filter).forEach(key => {
        this.filter[key] = null;
      });
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
        },
      ).then(async() => {
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
    milgroupField(row) {
      return row.milgroup.milgroup;
    },
    dateFilter(value) {
      if (value) return moment(value).format("DD.MM.YYYY");
      return "Нет данных";
    },
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
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
