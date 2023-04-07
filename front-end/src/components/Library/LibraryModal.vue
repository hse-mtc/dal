<template>
  <ModalWindow :opened="true" v-on="$listeners">
    <el-form ref="form" :model="formValues" :rules="rules">
      <el-form-item v-for="(value, key) in formValues" :key="key" :prop="key">
        <TextInput
          v-if="key === 'bookName'"
          v-model="formValues.bookName"
          title="Название"
          is-text-area
        />

        <TextInput
          v-else-if="key === 'annotation'"
          v-model="formValues.annotation"
          title="Аннотация"
          is-text-area
        />

        <SelectInput
          v-else-if="key === 'authors'"
          v-model="formValues.authors"
          :options="authors"
          title="Авторы"
          multiple
          filterable
        />

        <SelectInput
          v-else-if="key === 'publishers'"
          v-model="formValues.publishers"
          :options="publishers"
          title="Издательство"
          filterable
        />

        <template v-else-if="key === 'publishDate'">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item prop="publishDate">
                <span class="InputsBase_title_1SHIu">Год издания</span>
                <el-date-picker
                  v-model="formValues.publishDate"
                  type="date"
                  :picker-options="{
                    disabledDate(time) {
                      return time.getTime() > Date.now();
                    },
                    firstDayOfWeek: 1,
                  }"
                  format="dd.MM.yyyy"
                  value-format="yyyy-MM-dd"
                  placeholder="Выберите дату"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item>
                <span class="InputsBase_title_1SHIu">Количество страниц</span>
                <el-input-number
                  v-model="formValues.pageCount"
                  :controls="false"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </template>

        <SelectInput
          v-else-if="key === 'subjects'"
          v-model="formValues.subjects"
          title="Предметы"
          multiple
          filterable
          :options="subjects"
          style="margin-top: -22px"
        />

        <FileInput
          v-else-if="key === 'bookCover'"
          v-model="formValues.bookCover"
          title="Загрузите обложку для книги"
          :limit="1"
          :files-types="['.png', '.jpg']"
        />

        <FileInput
          v-else-if="key === 'book'"
          v-model="formValues.book"
          title="Загрузите текст книги"
          :limit="1"
          :files-types="['.pdf', '.djvu', '.epub', '.fb2', '.rtf', '.docx']"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">
          Сохранить
        </el-button>
        <el-button type="info" @click="close">
          Закрыть
        </el-button>
      </el-form-item>
    </el-form>
  </ModalWindow>
</template>

<script>
import {
  SelectInput,
  TextInput,
  FileInput,
} from "@/common/inputs";

import ModalWindow from "@/components/ModalWindow/ModalWindow.vue";
import {PapersModule, ReferenceModule, SubjectsModule} from "@/store";

export default {
  name: "LibraryModal",
  components: {
    ModalWindow,
    SelectInput,
    TextInput,
    FileInput,
  },
  props: {
    submitCallback: {
      type: Function,
      default: () => () => ({}),
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
    subjects() {
      let milspecialties = ReferenceModule.milspecialties;
      return SubjectsModule.subjects.map(subject => ({
        label: `${subject.title} ${milspecialties.find(x => x.id === subject.milspecialty).code}`,
        value: subject.id,
      }));
    },
    authors() {
      return PapersModule.authors.map(author => ({
        label: `${author.surname} ${author.name} ${author.patronymic}`,
        value: author.id,
      }));
    },
    publishers() {
      return PapersModule.publishers.map(publisher => ({
        label: publisher.name,
        value: publisher.id,
      }));
    },
  },
  watch: {
    initData(nextValue, prevValue) {
      if (!this.lodash.isEqual(nextValue, prevValue)) {
        this.formValues = this.lodash.cloneDeep(nextValue);
      }
    },
  },
  methods: {
    onSubmit() {
      this.$refs.form.validate(valid => {
        if (!valid || (!this.isChanging && !this.formValues.book.length)) { return false; }

        this.$emit("save", this.formValues);
        this.$emit("close-modal", true);

        return true;
      });
    },
    close() {
      this.$emit("close-modal", true);
    },
  },
};
</script>

<style lang="scss" module></style>
