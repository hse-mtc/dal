<template>
  <div>
    <el-row class="pageTitle">
      <h1>Подтверждения регистрации</h1>
    </el-row>
    <el-row>
      <PrimeTable
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
          :field="row => row.milgroup && row.milgroup.title"
          column-key="milgroup"
          header="Взвод"
          sortable
        />
        <PrimeColumn
          header="Статус"
          sortable
          field="status"
          column-key="status"
        >
          <template #body="{ data: student }">
            <el-tag :type="tagByStatus(student.status)">
              {{ student.status | filterStatus }}
            </el-tag>
          </template>
        </PrimeColumn>
        <PrimeColumn
          header="Действия с регистрацией"
          column-key="buttons"
        >
          <template #body="{ data: student }">
            <el-tooltip
              class="item"
              effect="dark"
              content="Сделать абитуриента студентом"
              placement="bottom"
            >
              <el-button
                size="medium"
                icon="el-icon-user"
                type=""
                circle
                class="approve-button"
                :disabled="student.status === 'ST'"
                @click="approve(student)"
              />
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="Поставить в ожидание"
              placement="bottom"
            >
              <el-button
                size="medium"
                icon="el-icon-tickets"
                type=""
                circle
                class="wait-button"
                :disabled="student.status === 'AW'"
                @click="putOnWait(student)"
              />
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="Отклонить регистрацию"
              placement="bottom"
            >
              <el-button
                size="medium"
                icon="el-icon-close"
                type=""
                circle
                class="disapprove-button"
                :disabled="student.status === 'DE'"
                @click="disapprove(student)"
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
import { getUsersToApprove, changeStudentStatus } from "@/api/admin";
import { getError, postError, deleteError } from "@/utils/message";

export default {
  name: "",
  filters: {
    filterStatus(val) {
      switch (val) {
        case "AP":
          return "Абитуриент";
        case "ST":
          return "Студент";
        case "EX":
          return "Отчислен";
        case "GR":
          return "Выпустился";
        case "AW":
          return "В ожидании";
        case "DE":
          return "Отклонен";
        default:
          return "Ошибка";
      }
    },
  },
  data() {
    return {
      approveList: [],
    };
  },
  async created() {
    try {
      const { data } = await getUsersToApprove();
      this.approveList = data;
    } catch (err) {
      getError("данных для подтверждения активации", err.response.status);
    }
  },
  methods: {
    approve(user) {
      changeStudentStatus(user.id, "ST")
        .then(() => {
          // todo
          // eslint-disable-next-line no-param-reassign
          user.status = "ST";
        })
        .catch(err => postError("записи об активированной регистрации", err.response.status));
    },
    putOnWait(user) {
      changeStudentStatus(user.id, "AW")
        .then(() => {
          // todo
          // eslint-disable-next-line no-param-reassign
          user.status = "AW";
        })
        .catch(err => postError("записи об активированной регистрации", err.response.status));
    },
    disapprove(user) {
      this.$confirm(
        "Вы уверены, что хотите отклонить регистрацию абитуриента?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      )
        .then(() => {
          changeStudentStatus(user.id, "DE")
            .then(() => {
              // todo
              // eslint-disable-next-line no-param-reassign
              user.status = "DE";
            })
            .catch(err => postError(
              "записи об активированной регистрации",
              err.response.status,
            ));
        })
        .catch(() => {});
    },
    tagByStatus(status) {
      switch (status) {
        case "AP":
          return "info";
        case "ST":
          return "success";
        case "GR":
          return "info";
        case "AW":
          return "warning";
        default:
          return "danger";
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
