<template>
  <div>
    <el-col :offset="2" :span="20">
      <el-tabs v-model="activeTab" stretch @click="onFilter">
        <el-tab-pane label="Авторы" name="authors">
          <el-button
            style="width: 100%"
            class="addBtn"
            type="primary"
            icon="el-icon-plus"
            @click="
              onEdit({
                id: 0,
                surname: '',
                name: '',
                patronymic: '',
              })
            "
          >
            Новый автор
          </el-button>
          <el-table :data="authors" max-height="680" style="width: 100%" stripe>
            <el-table-column sortable label="Фамилия" prop="surname" />
            <el-table-column sortable label="Имя" prop="name" />
            <el-table-column sortable label="Отчество" prop="patronymic" />
            <el-table-column width="120px">
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
                  @click="handleDelete(scope.row.id)"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="Места публикации" name="publishers"> </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-dialog
      title="Редактирование автора"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editAuthor"
      >
        <el-form-item label="Фамилия: ">
          <el-input
            v-model="editAuthor.surname"
            placeholder="Введите фамилию"
          />
        </el-form-item>
        <el-form-item label="Имя: ">
          <el-input v-model="editAuthor.name" placeholder="Введите имя" />
        </el-form-item>
        <el-form-item label="Отчество: ">
          <el-input
            v-model="editAuthor.patronymic"
            placeholder="Введите отчество"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Отмена</el-button>
        <el-button type="primary" @click="handleAccept()">Применить</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {
  deleteAuthors,
  getAuthors,
  patchAuthor,
  postAuthor,
} from "@/api/authors";
import {
  deleteError,
  deleteSuccess,
  getError,
  patchError,
  patchSuccess,
  postSuccess,
} from "@/utils/message";

export default {
  name: "DictionariesComponent",
  data() {
    return {
      dialogVisible: false,
      activeTab: "authors",
      authors: [],
      editAuthor: {
        id: 0,
        surname: "",
        name: "",
        patronymic: "",
      },
    };
  },
  created() {
    this.onFilter();
  },
  methods: {
    onFilter() {
      getAuthors()
        .then((response) => {
          this.authors = response.data;
        })
        .catch((err) => getError("авторов", err.response.status));
    },
    onEdit(row) {
      this.editAuthor = { ...row };
      this.dialogVisible = true;
    },
    handleClose() {
      this.$confirm(
        "Вы уверены, что хотите закрыть окно редактирования?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        }
      )
        .then(() => {
          this.dialogVisible = false;
        })
        .catch(() => {});
    },
    handleDelete(id) {
      this.$confirm("Вы уверены, что хотите удалить автора?", "Подтверждение", {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      }).then(() => {
        deleteAuthors({ id })
          .then(() => {
            deleteSuccess("автора");
            this.onFilter();
          })
          .catch((err) => deleteError("автора", err.response.status));
      });
    },
    handleAccept() {
      if (this.editAuthor.id !== 0) {
        patchAuthor(this.editAuthor)
          .then(() => {
            patchSuccess("автора");
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch((err) => patchError("автора", err.response.status));
      } else {
        postAuthor(this.editAuthor)
          .then(() => {
            postSuccess("автора");
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch((err) => patchError("автора", err.response.status));
      }
    },
  },
};
</script>

<style scoped></style>
