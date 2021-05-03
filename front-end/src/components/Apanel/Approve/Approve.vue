<template>
  <div>
    <el-col :offset="2" :span="20">
      <el-row class="pageTitle">
        <h1>Подтверждения регистрации</h1>
      </el-row>
      <el-row>
        <el-table :data="approveList" width="300px" stripe>
          <el-table-column
            prop="fullname"
            label="ФИО"
            sortable
            show-overflow-tooltip
          />
          <el-table-column
            prop="milgroup.milgroup"
            label="Взвод"
            sortable
            width="180"
          />
          <el-table-column label="Статус" width="180">
            <template slot-scope="scope">
              <el-tag :type="tagByStatus(scope.row.status)">
                {{ scope.row.status | filterStatus }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="Действия с регистрацией" width="220">
            <template slot-scope="scope">
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
                  :disabled="scope.row.status === 'ST'"
                  @click="approve(scope.row)"
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
                  :disabled="scope.row.status === 'AW'"
                  @click="putOnWait(scope.row)"
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
                  :disabled="scope.row.status === 'DE'"
                  @click="disapprove(scope.row)"
                />
              </el-tooltip>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
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
  created() {
    getUsersToApprove()
      .then(response => {
        this.approveList = response.data;
      })
      .catch(err => getError("данных для подтверждения активации", err.response.status));
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
