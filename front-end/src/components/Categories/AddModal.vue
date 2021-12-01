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
import { Message } from "element-ui";
import { PapersModule } from "@/store";
import { addPaperCategory } from "@/api/paper_categories";

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
    categories() { return PapersModule.categories; },
  },

  methods: {
    async onSubmit() {
      const title = this.form.title.trim();

      const usedCategories = [...this.categories.map(category => category.title.trim().toLowerCase()), "Корзина".toLowerCase()];
      if (usedCategories.includes(title.toLowerCase())) {
        Message({
          message: "Категория с похожим названием уже существует.",
          type: "error",
        });
        return;
      }

      await PapersModule.addCategory({ title });
      this.closeModal();
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
