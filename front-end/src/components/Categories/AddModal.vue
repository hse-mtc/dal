<template>
  <div class="addModal">
    <el-form ref="form" :model="form" label-width="175px">
      <el-form-item label="Название категории">
        <el-input v-model="form.title" placeholder="Введите название" />
      </el-form-item>

      <el-form-item>
        <el-button :disabled="form.title.trim() === ''" type="primary" @click="onSubmit">
          Добавить
        </el-button>
        <el-button @click="closeModal">
          Отменить
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { addPaperCategories } from "@/api/paper_categories";

import EventBus from "@/components/EventBus";
import { mapState } from "vuex";
import { Message } from "element-ui";

export default {
  name: "AddModal",

  data() {
    return {
      form: {
        title: "",
      },
    };
  },

  computed: {
    ...mapState({
      categories: state => state.documents.categories,
    }),
  },

  methods: {
    async onSubmit() {
      const title = this.form.title.trim();
      if (this.categories.find(category => category.title.trim().toLowerCase() === title.trim().toLowerCase())) {
        Message({
          message: "Такая категория уже существует",
          type: "error",
        });
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
