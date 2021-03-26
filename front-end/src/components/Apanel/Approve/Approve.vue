<template>
  <div>
    <el-col :offset="2" :span="20">
      <el-row class="pageTitle">
        <h1>Подтверждения регистрации</h1>
      </el-row>
      <el-row>
        <el-table
          :data="approveList"
          width="300px"
          stripe
          :row-class-name="tableRowClassName"
        >
          <el-table-column
            prop="fullname"
            label="ФИО"
            sortable
            show-overflow-tooltip
          >
          </el-table-column>
          <el-table-column prop="milgroup" label="Взвод" sortable width="180">
          </el-table-column>
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
                  @click="approve(scope.row)"
                  :disabled="scope.row.status === 'ST'"
                >
                </el-button>
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
                  @click="putOnWait(scope.row)"
                  :disabled="scope.row.status === 'AW'"
                ></el-button>
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
                  @click="disapprove(scope.row)"
                  :disabled="scope.row.status === 'DE'"
                ></el-button>
              </el-tooltip>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
  </div>
</template>

<script>
import {
  getUsersToApprove,
  approveUser,
  putUserOnWait,
  disapproveUser,
} from "@/api/admin";
import { getError, postError, deleteError } from "@/utils/message";

export default {
  name: "",
  data() {
    return {
      approveList: [],
    };
  },
  created() {
    getUsersToApprove()
      .then((response) => {
        this.approveList = response.data;
      })
      // TODO: when back-end is done, change fake data to error
      // .catch((err) => getError("данных для подтверждения активации", err.response.status));
      .catch((err) => {
        getError("данных для подтверждения активации", err.response.status);
        this.approveList = [
          {
            id: 1,
            fullname: "Хромов Григорий Александрович",
            milgroup: 1809,
            status: "AP",
          },
          {
            id: 2,
            fullname: "Васюткин Вася Васильевич",
            milgroup: 1810,
            status: "AP",
          },
          {
            id: 3,
            fullname: "Иванов Иван Иванович",
            milgroup: 1808,
            status: "AP",
          },
        ];
      });
  },
  methods: {
    approve(user) {
      approveUser(user.id)
        .then(() => {
          user.status = "ST";
        })
        // TODO: when back-end is done, change fake data to error
        // .catch((err) => postError("записи об активированной регистрации", err.response.status));
        .catch((err) => {
          postError(
            "записи об активированной регистрации",
            err.response.status
          );
          user.status = "ST";
        });
    },
    putOnWait(user) {
      putUserOnWait(user.id)
        .then(() => {
          user.status = "AW";
        })
        // TODO: when back-end is done, change fake data to error
        // .catch((err) => postError("записи об активированной регистрации", err.response.status));
        .catch((err) => {
          postError(
            "записи в списке отложенных регистраций",
            err.response.status
          );
          user.status = "AW";
        });
    },
    disapprove(user) {
      this.$confirm(
        "Вы уверены, что хотите отклонить регистрацию абитуриента?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        }
      )
        .then(() => {
          user.status = "DE";
          disapproveUser(user.id)
            .then(() => {
              user.status = "DE";
            })
            // TODO: when back-end is done, change fake data to error
            // .catch((err) => postError("записи об активированной регистрации", err.response.status));
            .catch((err) => {
              deleteError("регистрации", err.response.status);
              user.status = "DE";
            });
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
          return "";
        case "AW":
          return "warning";
        default:
          return "danger";
      }
    },
  },
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
};
</script>

<style scoped lang="scss">
@import "style";
</style>
