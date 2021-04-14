<template>
  <ModalWindow :opened="true" v-on="$listeners">
    <el-form ref="form" :model="formValues" :rules="rules">
      <el-form-item v-for="(value, key) in formValues" :key="key" :prop="key">
        <SelectInput
          v-if="key === 'authors'"
          :options="authors"
          title="Автор"
          multiple
          filterable
          v-model="formValues.authors"
        />

        <SelectInput
          v-else-if="key === 'publishers'"
          :options="publishers"
          title="Издательство"
          filterable
          v-model="formValues.publishers"
        />

        <template v-else-if="key === 'publishDate'">
          <el-col :span="11">
            <el-form-item prop="publishDate">
              <DateInput
                title="Год издания"
                type="year"
                v-model="formValues.publishDate"
                format="yyyy"
                value-format="yyyy"
              />
            </el-form-item>
          </el-col>

          <el-col :span="2">&nbsp;</el-col>

          <el-col :span="11">
            <el-form-item>
              <NumberInput
                title="Количество страниц"
                v-model="formValues.pageCount"
              />
            </el-form-item>
          </el-col>
        </template>

        <TextInput
          v-else-if="key === 'bookName'"
          title="Название книги"
          v-model="formValues.bookName"
          isTextArea
        />

        <TextInput
          v-else-if="key === 'annotation'"
          title="Аннотация"
          v-model="formValues.annotation"
          isTextArea
        />

        <SelectInput
          v-else-if="key === 'subjects'"
          title="Предметы"
          v-model="formValues.subjects"
          multiple
          filterable
          :options="subjects"
        />

        <FileInput
          v-else-if="key === 'bookCover'"
          title="Загрузите обложку для книги"
          v-model="formValues.bookCover"
          :limit="1"
          :filesTypes="['.png', '.jpg']"
        />

        <FileInput
          v-else-if="key === 'book'"
          title="Загрузите текст книги"
          v-model="formValues.book"
          :limit="1"
          :filesTypes="['.pdf', '.djvu', '.epub', '.fb2', '.rtf', '.docx']"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit"> Сохранить </el-button>
        <el-button type="info" @click="close"> Закрыть </el-button>
      </el-form-item>
    </el-form>
  </ModalWindow>
</template>

<script>
import { mapState } from "vuex";

import SelectInput from "@/common/inputs/Select";
import DateInput from "@/common/inputs/Date";
import TextInput from "@/common/inputs/Text";
import NumberInput from "@/common/inputs/Number";
import FileInput from "@/common/inputs/File";
import ModalWindow from "@/components/ModalWindow/ModalWindow.vue";

export default {
  name: "LibraryModal",
  components: {
    ModalWindow,
    SelectInput,
    DateInput,
    TextInput,
    NumberInput,
    FileInput,
  },
  props: {
    submitCallback: {
      type: Function,
      default: () => () => {},
    },
    opened: { type: Boolean, default: false },
    initData: { type: Object, required: true },
    isChanging: { type: Boolean, default: false },
  },
  data() {
    const required = [{ required: true, message: "Обязательное поле" }];
    return {
      rules: {
        authors: required,
        publishers: required,
        bookName: required,
        book: required,
        publishDate: required,
      },
      formValues: this.lodash.cloneDeep(this.initData),
    };
  },
  computed: {
    ...mapState({
      authors: (state) =>
        state.documents.authors.map((author) => ({
          label: `${author.surname} ${author.name} ${author.patronymic}`,
          value: author.id,
        })),
      subjects: (state) =>
        state.subjects.subjects.map((subject) => ({
          label: subject.title,
          value: subject.id,
        })),
      publishers: (state) =>
        state.documents.publishers.map((publisher) => ({
          label: publisher.name,
          value: publisher.id,
        })),
    }),
  },
  methods: {
    onSubmit() {
      this.$refs.form.validate((valid) => {
        console.log("this.formValues.book", this.formValues.book);
        if (!valid || (!this.isChanging && !this.formValues.book.length))
          return false;

        this.$emit("save", this.formValues);
        this.$emit("close-modal");
      });
    },
    close() {
      this.$emit("close-modal");
    },
  },
  watch: {
    initData(nextValue, prevValue) {
      if (!this.lodash.isEqual(nextValue, prevValue)) {
        this.formValues = this.lodash.cloneDeep(nextValue);
      }
    },
  },
};
</script>

<style lang="scss" module></style>
