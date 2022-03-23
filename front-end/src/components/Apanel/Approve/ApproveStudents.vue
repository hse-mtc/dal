<template>
  <div>
    <el-row class="pageTitle" style="margin-bottom: 15px">
      <h1>Подтверждения студентов</h1>
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
          :field="(student) => phoneNumberMixin(student.phone)"
          column-key="phone"
          header="Телефон"
          sortable
        />

        <PrimeColumn
          field="milgroup.title"
          header="Взвод"
          column-key="milgroup"
          sortable
        />

        <PrimeColumn
          :field="(student) => studentPostLabelFromValueOrDefault(student.post, 'Студент')"
          column-key="post"
          header="Должность"
          sortable
        />

        <PrimeColumn
          header="Действия"
          column-key="buttons"
        >
          <template #body="{ data: student }">
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
                @click="approve(student)"
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
import { getStudentsToApprove, approveStudent, getAllRoles } from "@/api/admin";
import { getError, patchError } from "@/utils/message";
import { StudentPostsMixin } from "@/mixins/students";

export default {
  name: "ApproveStudents",
  mixins: [StudentPostsMixin],

  data() {
    return {
      approveList: [],
      roles: [],
      fetchingData: false,
    };
  },

  computed: {
    loading() {
      return this.fetchingData;
    },
  },

  async created() {
    this.fetchingData = true;

    let responses;
    try {
      responses = await Promise.all([
        getStudentsToApprove(),
        getAllRoles(),
      ]);
    } catch (err) {
      getError("данных для подтверждения активации", err.response?.status);
      return;
    } finally {
      this.fetchingData = false;
    }

    [this.approveList, this.roles] = responses.map(r => r.data);
    this.approveList = this.approveList(student => ({
      permission_groups: [],
      ...student,
    }));
  },

  methods: {
    phoneNumberMixin(phoneNumber) {
      return "+".concat(phoneNumber);
    },
    async approve(student) {
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
        await approveStudent(student.id, {
          permission_groups: student.permission_groups,
        });
      } catch (e) {
        patchError("регистрации преподавателя", e.response?.status);
        return;
      } finally {
        this.fetchingData = false;
      }

      this.approveList = this.approveList.filter(s => s.id !== student.id);
      this.$message({
        type: "success",
        message: "Регистрация подтверждена.",
        duration: 3000,
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
