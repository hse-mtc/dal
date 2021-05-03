<template>
  <el-col :offset="2" :span="20" class="ReferenceBook">
    <el-row class="pageTitle">
      <h1>{{ $route.meta.title }}</h1>
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
            v-for="name in item.names"
            :key="name"
            closable
            :disable-transitions="false"
            style="margin-bottom: 10px"
            @close="handleClose(item, name)"
          >
            {{ name }}
          </el-tag>
          <el-input
            v-if="item.inputVisible"
            :ref="saveTagInput"
            v-model="item.inputValue"
            class="input-new-tag"
            size="mini"
            style="margin-bottom: 10px"
            @keyup.enter.native="handleInputConfirm(item)"
            @blur="handleInputConfirm(item)"
          />
          <el-button
            v-else
            class="button-new-tag"
            size="small"
            style="margin-bottom: 10px"
            @click="showInput(item)"
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
      // todo
      // eslint-disable-next-line no-param-reassign
      item.inputVisible = true;
    },
    handleInputConfirm(item) {
      // todo
      /* eslint-disable no-param-reassign */
      item.inputVisible = false;
      if (item.inputValue) item.names.push(item.inputValue);
      item.inputVisible = false;
      item.inputValue = null;
      /* eslint-enable no-param-reassign */
    },
    fetchData() {
      getReferenceBooks()
        .then(response => {
          this.books = response.data;
        })
        .catch(err => getError("справочников", err.response.status));
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
