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
        :row-class="() => 'clickable'"
        row-hover
        @row-click="onEdit"
      >
        <PrimeColumn
          field="fullname"
          header="ФИО"
          sortable
          header-style="width: 300px"
          body-style="width: 300px"
          column-key="fullname"
        />
        <PrimeColumn
          sortable
          :field="milgroupField"
          header="Взвод"
          column-key="milgroup"
        />
        <PrimeColumn
          :field="(row) => row.milgroup.milfaculty"
          header="Цикл"
          column-key="milfaculty"
        />
        <PrimeColumn
          :field="(row) => dateFilter(row.birth_info && row.birth_info.date)"
          header="Дата рождения"
          column-key="birthday"
        />
        <PrimeColumn
          :field="(row) => statusFilter(row.status)"
          header="Статус"
          header-style="width: 150px"
          body-style="width: 150px"
          column-key="status"
        />
        <PrimeColumn
          column-key="buttons"
          header-style="width: 50px"
          body-style="width: 50px"
        >
          <template #body="{ data }">
            <el-button
              size="mini"
              icon="el-icon-delete"
              type="danger"
              circle
              @click="onDelete($event, data.id)"
            />
          </template>
        </PrimeColumn>
      </PrimeTable>
    </el-row>
  </div>
</template>

<script>
import moment from "moment";
import { getError, deleteError, deleteSuccess } from "@/utils/message";
import { getStudentBasic, deleteStudent } from "@/api/students";

export default {
  name: "Students",
  data() {
    return {
      loading: false,
      filter: {
        search: null,
        milgroup: null,
        status: "ST",
      },
      students: [],
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
    };
  },
  async created() {
    await this.onFilter();
  },
  methods: {
    async onFilter() {
      try {
        this.loading = true;
        this.students = (await getStudentBasic(this.filter)).data;
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
    onDelete(e, id) {
      e.stopPropagation();
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
    onEdit({ data }) {
      console.log("🚀 > data", data);
      this.$router.push({ name: "Student", params: { studentId: data.id } });
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
