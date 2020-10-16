<template>
  <div class="addModal">
    <el-form ref="form" :model="document" label-width="175px">
      <el-form-item label="Название документа*">
        <el-input v-model="form.title" placeholder="Введите название"></el-input>
      </el-form-item>

      <el-form-item label="Аннотация">
        <el-input type="textarea" placeholder="Введите текст аннотации" v-model="form.annotation"
                  :autosize="{ minRows: 2}"></el-input>
      </el-form-item>

      <!--            <el-form-item label="Автор">-->
      <!--                <el-select clearable v-model="form.author" placeholder="Выберите автора">-->
      <!--                    <el-option-->
      <!--                            v-for="item in authors"-->
      <!--                            :key="item.value"-->
      <!--                            :value="item.id"-->
      <!--                            :label="item.value"-->

      <!--                    />-->
      <!--                </el-select>-->
      <!--            </el-form-item>-->

      <el-form-item label="Автор">
        <el-select
            v-model="form.selectedAuthors"
            multiple
            collapse-tags
            placeholder="Выберите авторов"
            style="width: 300px"
        >
          <el-option
              v-for="item in authors"
              :key="item.id"
              :label="`${item.last_name} ${item.first_name[0]}. ${item.patronymic[0]}`"
              :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>


      <!--            <div v-if="form.selectedAuthors.includes(-1)" class="add-author">-->
      <!--                <el-form-item label="Фамилия">-->
      <!--                    <el-input v-model="form.newAuthorLastName" placeholder="Введите фамилию"></el-input>-->
      <!--                </el-form-item>-->
      <!--                <el-form-item label="Имя">-->
      <!--                    <el-input v-model="form.newAuthorName" placeholder="Введите имя"></el-input>-->
      <!--                </el-form-item>-->
      <!--                <el-form-item label="Отчество">-->
      <!--                    <el-input v-model="form.newAuthorPatronymic" placeholder="Введите отчество"></el-input>-->
      <!--                </el-form-item>-->
      <!--            </div>-->

      <el-form-item label="Размещение">
        <el-select clearable v-model="form.publisher" placeholder="Выберите журнал">
          <el-option
              v-for="item in publishers"
              :key="item.id"
              :value="item.id"
              :label="item.name"
          />
        </el-select>
      </el-form-item>

      <div v-if="document.publisher === -1" class="add-publishers">
        <el-form-item label="Название размещения">
          <el-input v-model="form.newPublisher" placeholder="Введите имя"></el-input>
        </el-form-item>
      </div>

      <el-form-item label="Дата публикации">
        <el-date-picker
            v-model="form.publicationDate"
            type="date"
            placeholder="Выберите дату"
            format="dd.MM.yyyy">
        </el-date-picker>
      </el-form-item>

      <el-form-item label="Категория документа*">
        <el-select clearable v-model="form.currentCategory" placeholder="Выберите категорию">
          <el-option
              v-for="item in categories"
              :key="item.id"
              :value="item.id"
              :label="item.title"

          />
        </el-select>
      </el-form-item>

      <el-form-item label="Ключевые слова">
        <tags-input element-id="tags"
                    v-model="form.selectedTags"
                    :existing-tags="existingTags"
                    :typeahead="true"
                    placeholder="Добавить ключевое слово"
                    :typeahead-hide-discard="true"
                    class="add-tags">
        </tags-input>
      </el-form-item>

      <!--            <el-form-item>-->
      <!--                <div class="add-files">-->
      <!--                    <div class="add-files-title">Загрузите новый материал</div>-->
      <!--                    <div class="add-files-subtitle">Файл в формате: pdf, pptx, doc, docx, xls, xlsx</div>-->
      <!--                    <div class="add-files-container">-->
      <!--                        <input type="file" id="files" ref="files" v-on:change="handleFilesUpload()"/>-->
      <!--                        <div class="large-12 medium-12 small-12 cell">-->
      <!--                            <div v-for="(file, key) in form.files" class="file-listing">-->
      <!--                                {{ file.name }} <span class="remove-file" v-on:click="removeFile( key )">Удалить</span>-->
      <!--                            </div>-->
      <!--                        </div>-->
      <!--                        <div class="large-12 medium-12 small-12 cell">-->
      <!--                            <button v-on:click="addFiles()">Добавить файл</button>-->
      <!--                        </div>-->
      <!--                    </div>-->
      <!--                </div>-->
      <!--            </el-form-item>-->

      <el-form-item>
        <el-upload
            class="upload-demo"
            action="‍"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :on-change="addFile"
            ref="upload"
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="form.fileList"
            :auto-upload="false">
          <el-button size="small" type="primary" style="outline: none" :disabled="form.fileList.length > 0">Добавить файл</el-button>
          <div slot="tip" class="el-upload__tip"></div>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Отправить</el-button>
        <el-button @click="closeModal">Отменить</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {getExistingTags} from "../../api/existingTags";
import axios from "axios";
import moment from 'moment'
import EventBus from '../EventBus';
import {updateDocs} from "../../api/upload";
import {mapState} from "vuex";


export default {
  name: "EditDocumentModalWindow",
  data() {
    return {
      form: {
        title: '',
        author: '',
        selectedAuthors: [],
        annotation: '',
        publicationDate: '',
        newAuthorName: '',
        newAuthorLastName: '',
        newAuthorPatronymic: '',
        publisher: '',
        newPublisher: '',
        selectedTags: [],
        fileList: [],
        currentCategory: ''
      },
      ifFileChanged: false,
      existingTags: [
        {key: 1, value: 'Стратегия'},
        {key: 2, value: 'Тактика'},
      ],
      publishers: [{name: 'Добавить новое', id: -1}, ...this.$store.getters.publishers],
    }
  },
  props: {
    document: {
      type: Object,
      required: true
    }
  },
  created() {
    this.fetchData()
  },
  updated() {
    console.log(this.form.fileList)
  },
  mounted() {
    console.log(this.document, '--------')
    this.form = {
      title: this.document.title,
      author: '',
      selectedAuthors: this.document.authors.map(item => item.id),
      annotation: this.document.annotation,
      publicationDate: this.document.publication_date,
      newAuthorName: '',
      newAuthorLastName: '',
      newAuthorPatronymic: '',
      publisher: this.document.publishers[0],
      newPublisher: '',
      selectedTags: this.document.tags.map(item => {
        return {key: item, value: item}
      }),
      fileList: [this.document.file],
      currentCategory: this.categories.find(item => {
        console.log(item.id)
        return item.id == this.document.category
      }).id
    }
    console.log(this.form, '=========')
  },
  computed: {
    ...mapState({
      categories: state => state.documents.categories,
      authors: state => state.documents.authors,
    })
  },
  methods: {
    fetchData() {
      getExistingTags()
          .then(tags => {
            this.existingTags = tags
          }).catch(() => {
        console.log('Данные по тегам не указаны')
      })
    },
    onSubmit() {
      const self = this
      if (this.form.title !== '' && this.form.currentCategory !== '') {
        let formData = new FormData();
        formData.append('title', this.form.title);
        if (this.form.annotation !== '') formData.append('annotation', this.form.annotation);

        for (const id of this.form.selectedAuthors) {
          formData.append("authors", id);
        }

        if (this.form.publisher !== '') {
          formData.append('publishers', this.form.publisher);
        }

        if (this.form.publicationDate !== '') {
          formData.append('publication_date', moment(this.form.publicationDate).format('YYYY-MM-DD'));
        }

        formData.append('category', this.form.currentCategory);

        for (const tag of this.form.selectedTags.map(tag => tag.value)) {
          formData.append('tags', tag);
        }

        if (this.form.fileList.length !== 0) {
          if (this.ifFileChanged) {
            formData.append('content', this.form.fileList[0].raw);
          }
          updateDocs(formData, this.document.id)
              .then(function () {
                EventBus.$emit('UPDATE_EVENT');
                self.$emit('closeModal');
              }).catch(function () {
            console.log('FAILURE!!');
          });
        } else {
          this.$message.error(`Приложите файл`);
        }

        for (var key of formData.entries()) {
          console.log(key[0] + ', ' + key[1])
        }


      } else {
        this.$message.error(`Заполните поля со звездочкой`);
      }
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
      this.form.fileList = this.form.fileList.filter(item => item.uid !== file.uid)
    },
    handlePreview(file) {
      console.log(file);
    },
    addFile(file, fileList) {
      console.log(file, 'add')
      this.ifFileChanged = true
      this.form.fileList.push(file)
    },
    handleExceed(files, fileList) {
      this.$message.warning(`Вы можете выбрать максимум 1 файл.`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`Удалить ${file.name} ?`);
    },
    closeModal() {
      this.$emit('closeModal');
    }
  }
}
</script>

<style scoped lang="scss">
@import "style.scss";

.el-tag + .el-tag {
  margin-left: 10px;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>
