<template>
  <div class="addModal">
    <el-form ref="form" :model="form" label-width="175px">
      <el-form-item label="Название категории">
        <el-input v-model="form.title" placeholder="Введите название" />
      </el-form-item>

      <!-- Секция фильтров -->
      <el-form-item label="Фильтры" class="filters-form-item">
        <div class="filters-section">
          <!-- Существующие фильтры -->
          <div v-for="(filter, index) in form.filters" :key="index" class="filter-item">
            <el-row :gutter="10">
              <el-col :span="10">
                <el-input
                  v-model="filter.filtername"
                  placeholder="Название фильтра"
                  size="small"
                />
              </el-col>
              <el-col :span="8">
                <el-select
                  v-model="filter.type"
                  placeholder="Тип"
                  size="small"
                >
                  <el-option label="Строка" value="string" />
                  <el-option label="Число" value="number" />
                </el-select>
              </el-col>
              <el-col :span="6">
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  size="small"
                  circle
                  @click="removeFilter(index)"
                />
              </el-col>
            </el-row>
          </div>

          <!-- Кнопка добавления фильтра -->
          <el-button
            type="text"
            icon="el-icon-plus"
            class="add-filter-btn"
            @click="addFilter"
          >
            Добавить фильтр
          </el-button>
        </div>
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

import type { Category, CategoryFilter } from "@/types/category";

type Form = {
  title: string;
  filters: CategoryFilter[];
};

@Component({
  name: "AddModal",
})
class AddModal extends Vue {
  form: Form = {
    title: "",
    filters: [],
  };

  get categories(): Category[] {
    return PapersModule.categories;
  }

  addFilter(): void {
    this.form.filters.push({
      filtername: "",
      type: "string",
    });
  }

  removeFilter(index: number): void {
    this.form.filters.splice(index, 1);
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

    // Валидация фильтров
    const validFilters = this.form.filters.filter(filter => filter.filtername.trim() !== "");

    // Преобразуем фильтры в JSON Schema формат
    const jsonSchemaProperties = {};
    validFilters.forEach(filter => {
      jsonSchemaProperties[filter.filtername] = {
        type: filter.type,
      };
    });

    const jsonSchema = {
      type: "object",
      properties: jsonSchemaProperties,
    };

    const categoryData = {
      title,
      filters: jsonSchema,
    };

    console.log("Отправляемые данные категории:", categoryData);
    console.log("JSON Schema фильтров:", JSON.stringify(jsonSchema, null, 2));

    await PapersModule.addCategory(categoryData);
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
