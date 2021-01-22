<template>
  <el-col :offset="2" :span="20" class="ReferenceBook">
    <el-row class="pageTitle">
      <h1>{{ this.$route.meta.title }}</h1>
    </el-row>
    <el-row>
      <el-collapse>
        <el-collapse-item
          v-for="item in books"
          :key="item.ref"
          :title="item.ref"
          :name="item.ref"
        >
          <el-tag
            :key="name"
            v-for="name in item.names"
            closable
            :disable-transitions="false"
            @close="handleClose(item, name)"
            style="margin-bottom: 10px"
          >
            {{ name }}
          </el-tag>
          <el-input
            class="input-new-tag"
            v-if="item.inputVisible"
            v-model="item.inputValue"
            :ref="saveTagInput"
            size="mini"
            @keyup.enter.native="handleInputConfirm(item)"
            @blur="handleInputConfirm(item)"
            style="margin-bottom: 10px"
          >
          </el-input>
          <el-button
            v-else
            class="button-new-tag"
            size="small"
            @click="showInput(item)"
            style="margin-bottom: 10px"
          >
            + Добавить
          </el-button>
        </el-collapse-item>
      </el-collapse>
    </el-row>
  </el-col>
</template>

<script>
import { getReferenceBooks } from "@/api/reference-book";
import { getError } from "@/utils/message";

export default {
  name: "",
  components: {},
  data() {
    return {
      inputVisible: false,
      inputValue: "",
      books: [
        {
          ref: "Взвода",
          inputValue: null,
          inputVisible: null,
          names: [1807, 1808, 1809],
        },
        {
          ref: "Должности",
          inputValue: null,
          inputVisible: null,
          names: ["Командир взвода", "Командир отделения", "Журналист"],
        },
        {
          ref: "Навыки",
          inputValue: null,
          inputVisible: null,
          names: ["Футбол", "Шахматы", "Математика"],
        },
        {
          ref: "Звания",
          inputValue: null,
          inputVisible: null,
          names: ["Подполковник", "Полковник", "Генерал-Майор"],
        },
      ],
    };
  },
  methods: {
    handleClose(item, name) {
      item.names.splice(item.names.indexOf(name), 1);
    },
    showInput(item) {
      item.inputVisible = true;
    },
    handleInputConfirm(item) {
      item.inputVisible = false;
      if (item.inputValue) item.names.push(item.inputValue);
      item.inputVisible = false;
      item.inputValue = null;
    },
    fetchData() {
      getReferenceBooks()
        .then((response) => {
          this.books = response.data;
        })
        .catch((err) => getError("справочников", err.response.status));
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";

.el-tag + .el-tag {
  margin-left: 10px;
}
.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>
