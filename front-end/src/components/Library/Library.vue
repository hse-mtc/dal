<template>
  <div class="root">
    <PageHeader title="Библиотека" button="+ Добавить учебник" :click="addNewBook"/>
    <Modal
      v-if="showModal"
      :initData="modalData"
      :submit-callback="fetchData"
      :is-changing="!!changingId"
      @close-modal="onClose"
      @save="onSave"
    />
    <SearchBar placeholder="Введите название книги" :search="searchBook" :delete="deleteSearchInput"/>
    <CustomText :mt="SIZES.m" variant="paragraph">Найдено: {{ count || 0 }}</CustomText>
    <el-row>
      <el-col :span="18">
        <div class="sort mt-3 mb-3">
          <CustomText variant="sub-header" :mr="SIZES.m">Сортировать</CustomText>
          <el-select
              v-model="sort"
              placeholder="Выберите тип причины"
              style="display: block"
          >
            <el-option
                v-for="item in sortTypes"
                :key="item.key"
                :label="item.label"
                :value="item.key"
            >
            </el-option>
          </el-select>
        </div>
        <div class="content">
          <div class="books">
            <div class="book" v-for="item in books" :key="item.id">
              <Book :data="item" :onEdit="() => onBookEdit(item)"/>
            </div>
          </div>
        </div>
        <div v-loading="loading" class="requests__loader"></div>
      </el-col>
      <el-col :span="5" :offset="1">
        <LibraryFilters/>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import moment from 'moment'

import {SIZES} from "@/utils/appConsts"
import PageHeader from "@/common/PageHeader";
import SearchBar from "@/common/SearchBar";
import Modal from "./LibraryModal.vue";
import CustomText from "@/common/CustomText";
import LibraryFilters from "@/components/Library/LibraryFilters";
import Book from "@/components/Library/Book";
import {editBook, getBook, getBooks, uploadBook} from "@/api/books";
import {scrollMixin} from "@/mixins/scrollMixin";

export default {
  name: "Library",
  components: {
    LibraryFilters,
    CustomText,
    SearchBar,
    PageHeader,
    Book,
    Modal,
  },
  mixins: [scrollMixin],
  data() {
    return {
      SIZES,
      limit: 10,
      books: [],
      loading: false,
      count: null,
      sortTypes: [
        {
          key: '-publication_year',
          label: 'По году ↓'
        },
        {
          key: 'publication_year',
          label: 'По году ↑'
        },
        {
          key: '-title',
          label: 'По названию ↓'
        },
        {
          key: 'title',
          label: 'По названию ↑'
        }
      ],
      showModal: false,
      changingId: null,
      modalData: this.getInitBookData()
    };
  },
  computed: {
    sort: {
      get() {
        return this.$route.query.sort || '-publication_year'
      },
      set(value) {
        this.$router.push({
          query: {
            ...this.$route.query,
            sort: value,
          }
        })
      }
    },
    search: {
      get() {
        return this.$route.query.search || ''
      },
      set(value) {
        this.$router.push({
          query: {
            ...this.$route.query,
            search: value,
          }
        })
      }
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    loadMore() {
      this.fetchData()
    },
    fetchData() {
      if (this.books.length < this.count || this.count === null) {
        this.loading = true
        const {author, subject, year} = this.$route.query
        getBooks(this.lodash.pickBy({
          ordering: this.sort,
          authors: author,
          subjects: subject,
          end_year: year,
          start_year: year,
          search: this.search,
          limit: this.limit,
          offset: this.books.length
        })).then(res => {
          this.count = res.data.count
          this.books = [...this.books, ...res.data.results]
          this.loading = false
        })
      }
    },
    addNewBook() {
      this.showModal = true
      this.changingId = null
    },
    searchBook(value) { this.search = value },
    deleteSearchInput() { this.search = '' },
    clearHandler() {
      console.log('clearHandler func')
    },
    getInitBookData() {
      return {
        authors: [],
        publishers: null,
        publishDate: null,
        bookName: '',
        annotation: '',
        pageCount: 0,
        subjects: [],
        book: [],
        bookCover: [],
      }
    },
    async onSave(data) {
      const { changingId } = this
      const formData = new FormData()

      formData.set('data', JSON.stringify(this.lodash.pickBy({
        title: data.bookName,
        annotation: data.annotation,
        publication_year: moment(data.publishDate).format('YYYY'),
        authors: data.authors,
        publishers: data.publishers,
        subjects: data.subjects,
        page_count: data.pageCount,
      })))

      if (data.bookCover.length) {
        formData.set('image', data.bookCover[0].raw)
      }
      
      if (!changingId) {
        formData.set('content', data.book[0].raw)
      }

      try {
        if (changingId) {
          await editBook(changingId, formData)
        } else {
          await uploadBook(formData)
          this.fetchData()
        }
      } catch(e) {
        this.$message({
          message: `Не удалось ${changingId ? 'отредактировать' : 'сохранить'} книгу`,
          type: "error",
        });
        console.error(`Не удалось ${changingId ? 'отредактировать' : 'создать'} книгу:`, e)
      }

      if (changingId) {
        try {
          const bookData = (await getBook(changingId)).data

          this.books = this.books.map(item => item.id === changingId ? bookData : item)
        } catch(e) {
          console.warn(`не удалось отобразить новые данные: ${e}`, e)
        }
      }
    },
    onBookEdit(item) {
      this.modalData = {
        authors: item.authors.map(item => item.id),
        publishers: item.publishers[0].id,
        publishDate: item.publication_year,
        bookName: item.title,
        annotation: item.annotation,
        pageCount: item.page_count,
        subjects: item.subjects.map(item => item.id),
        bookCover: [],
      }
      this.showModal = true
      this.changingId = item.id
    },
    onClose() {
      this.showModal = false
      this.modalData = this.getInitBookData()
    }
  },
  watch: {
    $route() {
      this.count = null
      this.books = []
      this.fetchData()
    },
  },
}
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.root {

}

.sort {
  display: flex;
  align-items: center;
}

.content {
  min-height: 50vh;
}
</style>
