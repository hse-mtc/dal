<template>
  <div>
    <el-col :offset="2" :span="20" class="Personnel">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-tabs v-model="selectedSection" stretch @tab-click="onFilter">
        <el-tab-pane name="students" label="Студенты">
          <el-row class="filterRow" :gutter="20" style="margin-bottom: 15px">
            <el-col :span="8">
              <el-input
                v-model="filterS.search"
                clearable
                placeholder="Поиск..."
                @clear="onFilter"
                @keyup.native.enter="onFilter"
              />
            </el-col>
            <el-col :span="7">
              <el-select
                v-model="filterS.milgroup"
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
                v-model="filterS.status"
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
          <el-row class="addRow">
            <el-col :span="24">
              <el-button
                class="addBtn"
                type="primary"
                icon="el-icon-plus"
                @click="openModal"
              >
                Новый студент
              </el-button>
            </el-col>
          </el-row>
          <el-row class="table">
            <el-table
              max-height="600px"
              :data="studentsData"
              :default-sort="{ prop: 'milgroup.milgroup', order: 'ascending' }"
              stripe
            >
              <el-table-column
                width="300px"
                sortable
                show-overflow-tooltip
                prop="fullname"
                label="ФИО"
              />
              <el-table-column sortable prop="milgroup.milgroup" label="Взвод" />
              <el-table-column prop="milgroup.milfaculty" label="Цикл" />
              <el-table-column
                width="300px"
                show-overflow-tooltip
                prop="university_info.program.program"
                label="Программа"
              />
              <el-table-column label="Дата рождения">
                <template slot-scope="scope">
                  {{ formatDate(scope.row.birth_info) }}
                </template>
              </el-table-column>
              <el-table-column
                prop="status"
                label="Статус"
                show-overflow-tooltip
              >
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
                  />
                  <el-button
                    size="mini"
                    icon="el-icon-delete"
                    type="danger"
                    circle
                    @click="onDelete(scope.row.id)"
                  />
                </template>
              </el-table-column>
            </el-table>
          </el-row>
        </el-tab-pane>
        <el-tab-pane name="teachers" label="Преподаватели">
          <el-row class="filterRow" :gutter="20" style="margin-bottom: 15px">
            <el-col :span="8">
              <el-input
                v-model="filterT.search"
                clearable
                placeholder="Поиск..."
                @clear="onFilter"
                @keyup.native.enter="onFilter"
              />
            </el-col>
            <el-col :span="7">
              <el-select
                v-model="filterT.milfaculty"
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
          <el-row class="addRow">
            <el-col :span="24">
              <el-button class="addBtn" type="primary" icon="el-icon-plus">
                Новый преподаватель
              </el-button>
            </el-col>
          </el-row>
          <el-row class="table">
            <el-table
              max-height="600px"
              :data="teachersData"
              :default-sort="{ prop: 'milgroup.milgroup', order: 'ascending' }"
              stripe
            >
              <el-table-column width="400px" prop="fullname" label="ФИО" />
              <el-table-column prop="milfaculty" label="Цикл" />
              <el-table-column prop="rank" label="Звание" />
              <el-table-column prop="teacher_post" label="Должность" />
              <el-table-column prop="milgroup.milgroup" label="Прикр. взвод" />
              <el-table-column label="" width="120px">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    icon="el-icon-edit"
                    type="info"
                    circle
                  />
                  <el-button
                    size="mini"
                    icon="el-icon-delete"
                    type="danger"
                    circle
                    @click="onDelete(scope.row.id)"
                  />
                </template>
              </el-table-column>
            </el-table>
          </el-row>
        </el-tab-pane>
        <el-tab-pane name="uniform" label="Текущая форма одежды">
          <UniformPicker />
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <AddStudentModalWindow
      v-if="addModal"
      :student="editStudent"
      @closeModal="closeModal"
      @submitModal="clearFilter"
    />
    <div v-if="addModal" class="background" @click="closeModal" />
  </div>
</template>

<script>
import { getStudent, deleteStudent } from "@/api/student";
import { getTeacher, deleteTeacher } from "@/api/teacher";
import UniformPicker from "@/components/Personnel/UniformPicker/UniformPicker";
import moment from "moment";
import { getError, deleteError, deleteSuccess } from "@/utils/message";
import AddStudentModalWindow from "../AddStudentModalWindow/AddStudentModalWindow.vue";

export default {
  name: "",
  components: {
    AddStudentModalWindow,
    UniformPicker,
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
  },
  data() {
    return {
      filterS: {
        search: null,
        milgroup: null,
        status: null,
      },
      filterT: {
        search: null,
        milfaculty: null,
      },
      studentsData: [],
      teachersData: [],
      addModal: false,
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
      editStudent: null,
      selectedSection: "students",
    };
  },
  created() {
    this.onFilter();
  },
  methods: {
    formatDate(d) {
      if (d) return moment(d.date).format("DD.MM.YYYY");
      return "Нет данных";
    },
    closeModal() {
      this.addModal = false;
      document
        .getElementById("main-container")
        .classList.remove("stop-scrolling");
      this.editStudent = null;
    },
    openModal() {
      this.addModal = true;
      document.getElementById("main-container").classList.add("stop-scrolling");
    },
    onFilter() {
      if (this.selectedSection === "students") {
        getStudent({
          search: this.filterS.search,
          milgroup: this.filterS.milgroup,
          status: this.filterS.status,
        })
          .then(response => {
            this.studentsData = response.data;
          })
          .catch(err => getError("студентов", err.response.status));
      } else if (this.selectedSection === "teachers") {
        getTeacher({
          search: this.filterT.search,
          milfaculty: this.filterT.milfaculty,
        })
          .then(response => {
            this.teachersData = response.data;
          })
          .catch(err => getError("преподавателей", err.response.status));
      }
    },
    clearFilter() {
      if (this.selectedSection === "students") {
        this.filterS.search = null;
        this.filterS.milgroup = null;
        this.filterS.status = null;
      } else if (this.selectedSection === "teachers") {
        this.filterT.search = null;
        this.filterT.milfaculty = null;
      }
      this.onFilter();
    },
    onDelete(id) {
      if (this.selectedSection === "students") {
        this.$confirm(
          "Вы уверены, что хотите удалить студента?",
          "Подтверждение",
          {
            confirmButtonText: "Да",
            cancelButtonText: "Отмена",
            type: "warning",
          },
        ).then(() => {
          deleteStudent(id)
            .then(() => {
              this.onFilter();
              deleteSuccess("студента");
            })
            .catch(err => deleteError("студента", err.response.status));
        });
      } else if (this.selectedSection === "teachers") {
        this.$confirm(
          "Вы уверены, что хотите удалить преподавателя?",
          "Подтверждение",
          {
            confirmButtonText: "Да",
            cancelButtonText: "Отмена",
            type: "warning",
          },
        ).then(() => {
          deleteTeacher(id)
            .then(() => {
              this.onFilter();
              deleteSuccess("преподавателя");
            })
            .catch(err => deleteError("преподавателя", err.response.status));
        });
      }
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
