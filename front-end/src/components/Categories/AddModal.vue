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
      const usedCategories = [...this.categories.map(category => category.title.trim().toLowerCase()), "Корзина"];
      if (usedCategories.includes(title.trim().toLowerCase())) {
        Message({
          message: "Такая категория уже существует",
          type: "error",
        });
        return;
      }

      try {
        const { data } = await addPaperCategory({ title });
        PapersModule.setCategories([...this.categories, data]);
        this.closeModal();
      } catch (error) {
        console.error("Failed to add Category: ", error);
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
