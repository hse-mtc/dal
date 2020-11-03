<template>
  <div class="addModal">
    <ElForm
      ref="paperForm"
      :model="paperForm"
      :rules="rules"
      label-width="180px"
    >
      <ElFormItem label="Название документа" prop="title">
        <ElInput placeholder="Введите название" v-model="paperForm.title" />
      </ElFormItem>

      <ElFormItem label="Аннотация">
        <ElInput
          placeholder="Введите текст аннотации"
          v-model="paperForm.annotation"
          type="textarea"
          :autosize="{ minRows: 2 }"
        />
      </ElFormItem>

      <ElFormItem label="Авторы">
        <ElSelect
          placeholder="Выберите авторов"
          v-model="paperForm.authors"
          multiple
          collapse-tags
          style="width: 300px"
        >
          <ElOption
            v-for="author in authors"
            :key="author.id"
            :label="`${author.last_name} ${author.first_name[0]}. ${author.patronymic[0]}`"
            :value="author.id"
          />
        </ElSelect>
      </ElFormItem>

      <ElFormItem label="Размещения">
        <ElSelect
          placeholder="Выберите журналы"
          v-model="paperForm.publishers"
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
          placeholder="Выберите категорию"
          v-model.number="paperForm.category"
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

      <TagsInput label="Ключевые слова" v-model="paperForm.tags" />

      <ElFormItem label="Файл" prop="files">
        <ElUpload
          action=""
          ref="upload"
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
        <ElButton type="primary" @click="submitForm('paperForm')"
          >Отправить</ElButton
        >
        <ElButton @click="closeModal">Отменить</ElButton>
      </ElFormItem>
    </ElForm>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import moment from "moment";
import isEmpty from "lodash/isEmpty";

import EventBus from "@/components/EventBus";
import TagsInput from "@/components/Tags/TagsInput";

import { patchPaper, postPaper } from "@/api/papers";

import PaperForm from "@/utils/PaperForm";

export default {
  name: "UpsertPaperModal",
  components: { TagsInput },

  props: {
    paper: {
      type: Object,
      default: () => {},
    },
    action: {
      type: String,
      required: true,
      validator: (value) => {
        return ["add", "edit"].indexOf(value) > -1;
      },
    },
  },

  data() {
    const paper = this.paper;
    const empty = isEmpty(paper);
    const paperForm = empty
      ? new PaperForm()
      : new PaperForm(
          paper.annotation,
          paper.authors.map((a) => a.id),
          paper.category,
          [paper.file],
          paper.publication_date,
          paper.publishers.map((p) => p.id),
          paper.tags,
          paper.title
        );

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
    today() {
      return moment().format(this.dateFormat.toUpperCase());
    },
    ...mapGetters(["authors", "categories", "publishers"]),
  },

  methods: {
    async submitForm(name) {
      let formValid = this.paperForm.files.length > 0;
      this.$refs[name].validate((valid) => {
        return (formValid &= valid);
      });
      if (!formValid) {
        return;
      }

      const { data, content } = this.paperForm.split(this.action);
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
      this.$emit("closeModal");
    },
  },
};
</script>

<style scoped lang="scss">
@import "modal-style";

.paperFileUploaded /deep/ .el-upload {
  display: block !important;
}
</style>
