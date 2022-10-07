<template>
  <div>
    <el-row class="pageTitle" style="margin-bottom: 15px">
      <h1>Подтверждения регистрации преподавателей</h1>
    </el-row>

    <el-row>
      <PrimeTable
        v-loading="loading"
        :value="approveList"
        auto-layout
        class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
      >
        <PrimeColumn
          field="fullname"
          column-key="fullname"
          header="ФИО"
          sortable
        />

        <PrimeColumn
          field="email"
          column-key="email"
          header="Почта"
          sortable
        />

        <PrimeColumn
          :field="(teacher) => teacher.milfaculty ? teacher.milfaculty.abbreviation : '---'"
          column-key="milfaculty"
          header="Цикл"
          sortable
        />

        <PrimeColumn
          header="Прикреплённые взвода"
          column-key="milgroups"
          :body-style="`width: 200px`"
        >
          <template #body="{ data: teacher }">
            <ElTag
              v-for="milgroup in teacher.milgroups"
              :key="milgroup.id"
              :closable="false"
              class="ml-2"
            >
              {{ milgroup.title }}
            </ElTag>
          </template>
        </PrimeColumn>

        <PrimeColumn
          :field="(teacher) => teacherPostLabelFromValue(teacher.post)"
          column-key="post"
          header="Должность"
          sortable
        />

        <PrimeColumn
          :field="(teacher) => teacherRankLabelFromValue(teacher.rank)"
          column-key="rank"
          header="Звание"
          sortable
        />

        <PrimeColumn
          header="Роли"
          column-key="roles"
        >
          <template #body="{ data: teacher }">
            <ElSelect
              v-model="teacher.permission_groups"
              :multiple="true"
              placeholder="Выберите роли"
            >
              <ElOption
                v-for="role in roles"
                :key="role.key"
                :label="role.label"
                :value="role.key"
              />
            </ElSelect>
          </template>
        </PrimeColumn>

        <PrimeColumn
          header="Действия"
          column-key="buttons"
        >
          <template #body="{ data: teacher }">
            <el-tooltip
              class="item"
              effect="dark"
              content="Подтвердить"
              placement="bottom"
            >
              <el-button
                size="medium"
                icon="el-icon-user"
                type=""
                circle
                class="approve-button"
                @click="approve(teacher)"
              />
            </el-tooltip>

            <el-tooltip
              class="item"
              effect="dark"
              content="Отклонить"
              placement="bottom"
            >
              <el-button
                size="medium"
                icon="el-icon-close"
                type=""
                circle
                class="disapprove-button"
                @click="disapprove(teacher)"
              />
            </el-tooltip>
          </template>
        </PrimeColumn>

        <template #empty>
          <center>
            Нет новых пользователей
          </center>
        </template>
      </PrimeTable>
    </el-row>
  </div>
</template>

<script>
import {
  getTeachersToApprove, approveTeacher, getAllRoles, disapproveTeacher,
} from "@/api/admin";
import { getError, patchError } from "@/utils/message";
import { TeacherPostsMixin, TeacherRanksMixin } from "@/mixins/teachers";

export default {
  name: "ApproveTeachers",
  mixins: [TeacherPostsMixin, TeacherRanksMixin],

  data() {
    return {
      approveList: [],
      roles: [],
      fetchingData: false,
    };
  },

  computed: {
    loading() {
      return this.teacherPostsAreLoading || this.teacherRanksAreLoading || this.fetchingData;
    },
  },

  async created() {
    this.fetchingData = true;

    let responses;
    try {
      responses = await Promise.all([
        getTeachersToApprove(),
        getAllRoles(),
      ]);
    } catch (err) {
      getError("данных для подтверждения активации", err.response?.status);
      return;
    } finally {
      this.fetchingData = false;
    }

    [this.approveList, this.roles] = responses.map(r => r.data);
    this.roles = this.roles.filter(role => role.label !== "Студент" && role.label !== "Абитуриент");
    this.approveList = this.approveList(teacher => ({
      permission_groups: [],
      ...teacher,
    }));
  },

  methods: {
    async approve(teacher) {
      await this.$confirm(
        "Вы уверены? Отменить подтверждение регистрации нельзя.",
        "",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      );

      this.fetchingData = true;
      try {
        await approveTeacher(teacher.id, {
          permission_groups: teacher.permission_groups,
        });
      } catch (e) {
        patchError("регистрации преподавателя", e.response?.status);
        return;
      } finally {
        this.fetchingData = false;
      }

      this.approveList = this.approveList.filter(t => t.id !== teacher.id);
      this.$message({
        type: "success",
        message: "Регистрация подтверждена.",
        duration: 3000,
      });
    },
    async disapprove(teacher) {
      await this.$confirm(
        "Вы уверены, что хотите отклонить регистрацию?",
        "",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      );

      this.fetchingData = true;
      try {
        await disapproveTeacher(teacher.id);
      } catch (e) {
        patchError("отклонения регистрации преподавателя", e.response?.status);
        return;
      } finally {
        this.fetchingData = false;
      }

      this.approveList = this.approveList.filter(s => s.id !== teacher.id);
      this.$message({
        type: "success",
        message: "Регистрация отклонена.",
        duration: 3000,
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
