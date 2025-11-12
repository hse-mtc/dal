<template>
  <div class="addModal">
    <ElForm
      ref="paperForm"
      :model="paperForm"
      :rules="rules"
      label-width="180px"
    >
      <ElFormItem label="Название документа" prop="title">
        <ElInput v-model="paperForm.title" placeholder="Введите название" />
      </ElFormItem>

      <ElFormItem label="Аннотация">
        <ElInput
          v-model="paperForm.annotation"
          placeholder="Введите текст аннотации"
          type="textarea"
          :autosize="{ minRows: 2 }"
        />
      </ElFormItem>

      <ElFormItem label="Авторы">
        <ElSelect
          v-model="paperForm.authors"
          placeholder="Выберите авторов"
          multiple
          collapse-tags
          style="width: 300px"
        >
          <ElOption
            v-for="author in authors"
            :key="author.id"
            :label="surnameWithInitials(author)"
            :value="author.id"
          />
        </ElSelect>
      </ElFormItem>

      <ElFormItem label="Размещения">
        <ElSelect
          v-model="paperForm.publishers"
          placeholder="Выберите журналы"
          multiple
          collapse-tags
          style="width: 300px"
        >
          <ElOption
            v-for="{ id, name } in publishers"
            :key="id"
            :value="id"
            :label="name"
          />
        </ElSelect>
      </ElFormItem>

      <ElFormItem label="Дата публикации">
        <ElDatePicker
          v-model="paperForm.publicationDate"
          type="date"
          :placeholder="today"
          :format="dateFormat"
        />
      </ElFormItem>

      <ElFormItem label="Категория документа" prop="category">
        <ElSelect
          v-model.number="paperForm.category"
          placeholder="Выберите категорию"
          clearable
        >
          <ElOption
            v-for="{ id, title } in categories"
            :key="id"
            :value="id"
            :label="title"
          />
        </ElSelect>
      </ElFormItem>

      <!-- Фильтры категории -->
      <div v-if="currentCategoryFilters.length > 0" class="category-filters-section">
        <h3>Фильтры категории</h3>
        <ElFormItem
          v-for="filter in currentCategoryFilters"
          :key="filter.filtername"
          :label="filter.filtername"
        >
          <ElInput
            v-if="filter.type === 'string'"
            v-model="paperForm.categoryFilters[filter.filtername]"
            :placeholder="`Введите ${filter.filtername.toLowerCase()}`"
          />
          <ElInputNumber
            v-else
            v-model="paperForm.categoryFilters[filter.filtername]"
            :placeholder="`Введите ${filter.filtername.toLowerCase()}`"
            style="width: 300px"
          />
        </ElFormItem>
      </div>

      <TagsInput v-model="paperForm.tags" label="Ключевые слова" />

      <ElFormItem label="Файл" prop="files">
        <ElUpload
          ref="upload"
          action=""
          :auto-upload="false"
          :limit="1"
          :file-list="paperForm.files"
          :on-change="handleChange"
          :on-exceed="handleExceed"
          :before-remove="beforeRemove"
          :on-remove="handleRemove"
          :class="{ paperFileUploaded: paperForm.files.length }"
        >
          <ElButton
            v-if="!paperForm.files.length"
            slot="trigger"
            size="small"
            type="primary"
          >
            Загрузить...
          </ElButton>
        </ElUpload>
      </ElFormItem>

      <ElFormItem>
        <ElButton type="primary" @click="submitForm('paperForm')">
          Отправить
        </ElButton>
        <ElButton @click="closeModal">
          Отменить
        </ElButton>
      </ElFormItem>
    </ElForm>
  </div>
</template>

<script>
import moment from "moment";
import isEmpty from "lodash/isEmpty";

import EventBus from "@/components/EventBus";
import TagsInput from "@/components/Tags/TagsInput";

import { patchPaper, postPaper } from "@/api/papers";

import PaperForm from "@/utils/PaperForm";
import { surnameWithInitials } from "@/utils/person";
import { PapersModule } from "@/store";

export default {
  name: "UpsertPaperModal",
  components: { TagsInput },

  props: {
    paper: {
      type: Object,
      default: () => ({}),
    },
    action: {
      type: String,
      required: true,
      validator: value => ["add", "edit"].indexOf(value) > -1,
    },
  },

  data() {
    const { paper } = this;
    const empty = isEmpty(paper);

    // Инициализируем фильтры категории из существующего документа
    const categoryFilters = {};
    if (!empty && paper) {
      if (paper.additional_fields && typeof paper.additional_fields === "object") {
        Object.assign(categoryFilters, paper.additional_fields);
      }
      Object.keys(paper).forEach(key => {
        if (key.startsWith("filter_")) {
          const filterName = key.replace("filter_", "");
          if (categoryFilters[filterName] === undefined) {
            categoryFilters[filterName] = paper[key];
          }
        }
      });
    }

    const paperForm = empty
      ? new PaperForm()
      : new PaperForm(
        paper.annotation,
        paper.authors,
        paper.category,
        [paper.file],
        paper.publication_date,
        paper.publishers,
        paper.tags,
        paper.title,
        {},
      );

    // Инициализируем categoryFilters как реактивное свойство после создания формы
    if (categoryFilters && Object.keys(categoryFilters).length > 0) {
      paperForm.categoryFilters = categoryFilters;
    } else {
      paperForm.categoryFilters = {};
    }

    const required = { required: true, message: "Обязательное поле" };

    return {
      paperForm,
      dateFormat: "dd.MM.yyyy",
      rules: {
        title: [required],
        category: [required],
        files: [required],
      },
    };
  },

  computed: {
    authors() { return PapersModule.authors; },
    categories() { return PapersModule.categories; },
    publishers() { return PapersModule.publishers; },

    today() {
      return moment().format(this.dateFormat.toUpperCase());
    },

    // Получаем фильтры для текущей категории из JSON Schema
    currentCategoryFilters() {
      if (!this.paperForm.category) { return []; }
      const category = this.categories.find(cat => cat.id === this.paperForm.category);

      // Если filters это JSON Schema, преобразуем в массив фильтров
      if (category?.filters && category.filters.properties) {
        return Object.keys(category.filters.properties).map(propertyName => ({
          filtername: propertyName,
          type: category.filters.properties[propertyName].type,
        }));
      }

      return [];
    },
  },

  watch: {
    // Сброс фильтров при смене категории
    "paperForm.category": function(newCategoryId, oldCategoryId) {
      if (newCategoryId !== oldCategoryId) {
        this.$set(this.paperForm, "categoryFilters", {});
      }
    },
  },

  async created() {
    if (PapersModule && typeof PapersModule.reloadCategories === "function") {
      await PapersModule.reloadCategories();
    }
  },

  methods: {
    surnameWithInitials,

    async submitForm(name) {
      let formValid = this.paperForm.files.length > 0;
      // eslint-disable-next-line no-bitwise
      this.$refs[name].validate(valid => { formValid &= valid; });
      if (!formValid) {
        return;
      }

      const { data, content } = this.paperForm.split(this.action);
      console.log("Sending data to server:", data); // Отладка
      const formData = new FormData();
      formData.set("data", JSON.stringify(data));
      if (content) {
        formData.set("content", content);
      }

      try {
        if (this.action === "add") {
          await postPaper(formData);
        }
        if (this.action === "edit") {
          await patchPaper(this.paper.id, formData);
        }

        EventBus.$emit("UPDATE_EVENT");
        this.closeModal();
      } catch (error) {
        console.log("Failed to upsert Paper: ", error);
      }
    },

    handleChange(_, fileList) {
      this.paperForm.files = fileList;
    },
    handleExceed() {
      this.$message.warning("Вы можете приложить только один файл");
    },

    beforeRemove(file) {
      return this.$confirm(`Удалить ${file.name}?`);
    },
    handleRemove(_, fileList) {
      this.paperForm.files = fileList;
    },

    closeModal() {
      this.$emit("closeModal", true);
    },
  },
};
</script>

<style scoped lang="scss">
@import "upsert-modal";

.paperFileUploaded ::v-deep .el-upload {
  display: block !important;
}

.category-filters-section {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  background-color: #fafafa;

  h3 {
    margin: 0 0 15px 0;
    font-size: 16px;
    color: #606266;
    font-weight: 600;
  }
}
</style>
