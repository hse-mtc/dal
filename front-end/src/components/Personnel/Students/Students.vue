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
            :key="item.title"
            :value="item.id"
            :label="item.title"
          >
            <span style="float: left">{{ item.title }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{
              item.milfaculty.abbreviation
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
            v-for="status in studentStatuses"
            :key="status.value"
            :label="status.label"
            :value="status"
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
          :field="(row) => row.milgroup.milfaculty.title"
          header="Цикл"
          column-key="milfaculty"
        />
        <PrimeColumn
          :field="(row) => dateFilter(row.birth_info && row.birth_info.date)"
          header="Дата рождения"
          column-key="birthday"
        />
        <PrimeColumn
          :field="(row) => studentStatusLabelFromValue(row.status)"
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
            <AZGuard
              v-slot="{ disabled }"
              :permissions="[
                'students.delete.all',
                {
                  codename: 'students.delete.milfaculty',
                  validator: () => userMilfaculty === data.milgroup.milfaculty,
                },
                {
                  codename: 'students.delete.milgroup',
                  validator: () =>
                    userMilgroups.some((x) => x === data.milgroup.milgroup),
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
import moment from "moment";
import { getError, deleteError, deleteSuccess } from "@/utils/message";
import { getStudent, deleteStudent } from "@/api/students";
import { ReferenceModule, UserModule } from "@/store";
import { studentStatusesMixin } from "@/mixins/students";

export default {
  name: "Students",
  mixins: [studentStatusesMixin],
  data() {
    return {
      loading: false,
      filter: {
        search: null,
        milgroup: null,
        status: null,
      },
      students: [],
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
  },
  async created() {
    await this.onFilter();
  },
  methods: {
    async onFilter() {
      try {
        this.loading = true;
        const filter = {
          ...this.filter,
          status: this.filter.status?.value,
        };
        this.students = (await getStudent(filter)).data;
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
      this.$router.push({ name: "Student", params: { studentId: data.id } });
    },
    milgroupField(row) {
      return row.milgroup.title;
    },
    dateFilter(value) {
      if (value) return moment(value).format("DD.MM.YYYY");
      return "Нет данных";
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
