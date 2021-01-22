<template>
  <ModalWindow
    :opened="opened"
    v-on="$listeners"
  >
    <el-form
      ref="form"
      :model="formValues"
      :rules="rules"
    >
      <el-form-item prop="authors">
        <SelectInput
          :options="authors"
          title="Автор"
          multiple
          filterable
          v-model="formValues.authors"
        />
      </el-form-item>

      <el-form-item prop="publishers">
        <SelectInput
          :options="publishers"
          title="Издательство"
          filterable
          v-model="formValues.publishers"
        />
      </el-form-item>

      <el-form-item>
        <el-col :span="11">
          <el-form-item prop="publishDate">
            <DateInput
              title="Год издания"
              type="year"
              v-model="formValues.publishDate"
            />
          </el-form-item>
        </el-col>

        <el-col :span="2">&nbsp;</el-col>

        <el-col :span="11">
          <el-form-item>
            <NumberInput
              title="Количество страниц"
              v-model="formValues.pagesCount"
            />
          </el-form-item>
        </el-col>
      </el-form-item>

      <el-form-item prop="bookName">
        <TextInput
          title="Название книги"
          v-model="formValues.bookName"
          isTextArea
        />
      </el-form-item>

      <el-form-item>
        <TextInput
          title="Аннотация"
          v-model="formValues.annotation"
          isTextArea
        />
      </el-form-item>

      <el-form-item>
        <SelectInput
          title="Предметы"
          v-model="formValues.subjects"
          multiple
          filterable
          :options="subjects"
        />
      </el-form-item>

      <el-form-item>
        <FileInput
          title="Загрузите обложку для книги"
          v-model="formValues.bookCover"
          :limit="1"
          :filesTypes="['.png', '.jpg']"
        />
      </el-form-item>

      <el-form-item prop="book">
        <FileInput
          title="Загрузите текст книги"
          v-model="formValues.book"
          :limit="1"
          :filesTypes="['.pdf', '.djvu', '.epub', '.fb2', '.rtf', '.docx']"
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
import { mapState } from 'vuex'

import SelectInput from '@/common/inputs/Select'
import DateInput from '@/common/inputs/Date'
import TextInput from '@/common/inputs/Text'
import NumberInput from '@/common/inputs/Number'
import FileInput from '@/common/inputs/File'
import ModalWindow from "@/components/ModalWindow/ModalWindow.vue"

import { uploadBook } from '@/api/books'

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
      default: () => () => {}
    },
    opened: {type: Boolean, default: false}
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
      formValues: this.getInitData(),
    }
  },
  computed: {
    ...mapState({
      authors: (state) => state.documents.authors.map(author => ({
        label: `${author.surname} ${author.name} ${author.patronymic}`,
        value: author.id
      })),
      subjects: (state) => state.subjects.subjects.map(subject => ({
        label: subject.title,
        value: subject.id,
      })),
      publishers: (state) => state.documents.publishers.map(publisher => ({
        label: publisher.name,
        value: publisher.id,
      })),
    })
  },
  methods: {
    async onSubmit() {
      this.$refs.form.validate(async (valid) => {
        if (!valid || !this.formValues.book.length) return false

        const formData = new FormData()
        const data = this.formValues

        formData.set('data', JSON.stringify(this.lodash.pickBy({
          title: data.bookName,
          annotation: data.annotation,
          publication_year: data.publishDate,
          authors: data.authors,
          publishers: data.publishers,
          subjects: data.subjects,
          pages_count: data.pagesCount,
        })))

        if (data.bookCover.length) {
          formData.set('cover', this.formValues.bookCover[0].raw)
        }

        formData.set('content', this.formValues.book[0].raw)

        try {
          await uploadBook(formData)
          this.close()
          this.submitCallback()
        } catch(e) {
          this.$message({
            message: 'Не удалось сохранить книгу',
            type: "error",
          });
          console.error('Не удалось создать книгу:', e)
        }
      })
    },
    getInitData() {
      return {
        authors: [],
        publishers: null,
        publishDate: null,
        bookName: '',
        annotation: '',
        pagesCount: 0,
        subjects: [],
        book: [],
        bookCover: [],
      }
    },
    close() {
      this.formValues = this.getInitData()
      this.$emit('close-modal')
    }
  }
}
</script>

<style lang="scss" module>
</style>
