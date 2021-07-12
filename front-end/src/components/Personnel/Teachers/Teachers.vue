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
            :key="item.id"
            :label="item.abbreviation"
            :value="item.id"
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
        :row-class="() => 'clickable'"
        row-hover
        @row-click="onEdit"
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
          :field="teacher => teacher.milfaculty.title"
          header="Цикл"
          sortable
          column-key="milfaculty"
        />
        <PrimeColumn
          :field="teacher => teacher.rank.title"
          header="Звание"
          column-key="rank"
        />
        <PrimeColumn
          :field="teacher => displayTeacherPost(teacher.post)"
          header="Должность"
          column-key="teacherPost"
        />
        <PrimeColumn
          :field="displayMilgroups"
          header="Прикр. взвода"
          column-key="milgroup"
        />
        <PrimeColumn
          header-style="width: 50px"
          body-style="width: 50px"
          column-key="buttons"
        >
          <template #body="{ data }">
            <AZGuard
              v-slot="{ disabled }"
              :permissions="[
                'teachers.delete.all',
                {
                  codename: 'teachers.delete.milfaculty',
                  validator: () => userMilfaculty === data.milfaculty,
                },
              ]"
              disable
            >
              <el-button
                size="mini"
                icon="el-icon-delete"
                type="danger"
                circle
                :disabled="disabled"
                @click="onDelete($event, data.id)"
              />
            </AZGuard>
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
import { ReferenceModule, UserModule } from "@/store";

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
    };
  },
  computed: {
    milfaculties() {
      return ReferenceModule.milfaculties;
    },
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    userMilgroups() {
      return UserModule.personMilgroups;
    },
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
    onDelete(e, id) {
      e.stopPropagation();
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
    onEdit({ data }) {
      this.$router.push({ name: "Teacher", params: { teacherId: data.id } });
    },
    displayMilgroups(teacher) {
      if (teacher.milgroups === null) {
        return "";
      }

      return teacher.milgroups.map(m => m.title).sort().join(", ");
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
