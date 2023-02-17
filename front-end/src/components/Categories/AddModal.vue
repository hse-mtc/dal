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

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import { Message } from "element-ui";

import { PapersModule } from "@/store";

import type { Category } from "@/types/category";

type Form = {
  title: string;
};

@Component({
  name: "AddModal",
})
class AddModal extends Vue {
  form: Form = { title: "" };

  get categories(): Category[] {
    return PapersModule.categories;
  }

  async onSubmit(): Promise<void> {
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
    this.$emit("closeModal", true);
  }

  closeModal(): void {
    this.$emit("closeModal", true);
  }
}

export default AddModal;
</script>

<style scoped lang="scss">
@import "style.scss";
</style>
