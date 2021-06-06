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
          v-model="filter.milfaculty"
          clearable
          placeholder="Выберите цикл"
          style="display: block"
          @change="onFilter"
        >
          <el-option
            v-for="item in milfaculties"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </el-col>
      <el-col :offset="7" :span="2">
        <el-button type="text" @click="clearFilter">
          Сбросить
        </el-button>
      </el-col>
    </el-row>
    <el-row class="table">
      <PrimeTable
        v-loading="loading"
        :value="teachers"
        scrollable
        scroll-height="600px"
        sort-field="fullname"
        :sort-order="-1"
        class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
      >
        <PrimeColumn
          field="fullname"
          header="ФИО"
          sortable
          column-key="fullname"
          header-style="width: 400px"
          body-style="width: 400px"
        />
        <PrimeColumn
          field="milfaculty"
          header="Цикл"
          sortable
          column-key="milfaculty"
        />
        <PrimeColumn
          field="rank"
          header="Звание"
          column-key="rank"
        />
        <PrimeColumn
          field="teacher_post"
          header="Должность"
          column-key="teacherPost"
        />
        <PrimeColumn
          :field="row => row.milgroup && row.milgroup.milgroup"
          header="Прикр. взвод"
          column-key="milgroup"
        />
        <PrimeColumn
          header-style="width: 120px"
          body-style="width: 120px"
          column-key="buttons"
        >
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
              @click="onDelete(data.id)"
            />
          </template>
        </PrimeColumn>
      </PrimeTable>
    </el-row>
  </div>
</template>

<script>
import { getTeacher, deleteTeacher } from "@/api/teachers";
import moment from "moment";
import { getError, deleteError, deleteSuccess } from "@/utils/message";
import Teacher from "../Teacher/Teacher.vue";

export default {
  name: "Teachers",
  data() {
    return {
      loading: false,
      filter: {
        search: null,
        milfaculty: null,
      },
      teachers: [],
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
      editTeacher: null,
    };
  },
  async created() {
    await this.onFilter();
  },
  methods: {
    formatDate(d) {
      if (d) return moment(d.date).format("DD.MM.YYYY");
      return "Нет данных";
    },
    async onFilter() {
      try {
        this.loading = true;
        this.teachers = (await getTeacher(this.filter)).data;
      } catch (err) {
        getError("преподавателей", err.response.status);
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
        "Вы уверены, что хотите удалить преподавателя?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(async() => {
        try {
          await deleteTeacher(id);
          this.onFilter();
          deleteSuccess("преподавателя");
        } catch (err) {
          deleteError("преподавателя", err.response.status);
        }
      });
    },
    onEdit(teacherId) {
      this.$router.push({ name: "Teacher", params: { teacherId } });
    },
  },
};
</script>

<style scoped lang="less"></style>
