<template>
  <div class="addModal">
    <el-form ref="form" :model="form" label-width="175px">
      <el-form-item label="Название категории">
        <el-input placeholder="Введите название" v-model="form.title" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">Добавить</el-button>
        <el-button @click="closeModal">Отменить</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { addPaperCategories } from "@/api/paper_categories";

import EventBus from "../EventBus";

export default {
  name: "AddCategoryModalWindow",

  data() {
    return {
      form: {
        title: "",
      },
    };
  },

  methods: {
    async onSubmit() {
      const title = this.form.title.trim();
      if (title === "") {
        return;
      }

      try {
        await addPaperCategories({ title });
        EventBus.$emit("UPDATE_CATEGORY");
        this.closeModal();
      } catch (error) {
        console.log("Failed to add Category: ", error);
      }
    },

    closeModal() {
      this.$emit("closeModal");
    },
  },
};
</script>

<style scoped lang="scss">
@import "style.scss";
</style>
