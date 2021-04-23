<template>
  <div class="root">
    <PageHeader
      v-if="!(isMyLibrary || isFavoriteBooks)"
      title="Библиотека"
      button="+ Добавить учебник"
      :click="addNewBook"
    />
    <Modal
      v-if="showModal"
      :initData="modalData"
      :submit-callback="fetchData"
      :is-changing="!!changingId"
      @close-modal="onClose"
      @save="onSave"
    />
    <SearchBar
      v-if="!(isMyLibrary || isFavoriteBooks)"
      placeholder="Введите название книги"
      :search="searchBook"
      :delete="deleteSearchInput"
    />
    <CustomText
      v-if="!(isMyLibrary || isFavoriteBooks)"
      :mt="SIZES.m"
      variant="paragraph"
      >Найдено: {{ count || 0 }}</CustomText
    >
    <el-row>
      <el-col :span="18">
        <div class="sort mt-3 mb-3" v-if="!(isMyLibrary || isFavoriteBooks)">
          <CustomText variant="sub-header" :mr="SIZES.m"
            >Сортировать</CustomText
          >
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
              <Book
                @deleteFavBook="deleteFavBook"
                :data="item"
                :onEdit="() => onBookEdit(item)"
              />
            </div>
            <div v-if="books.length === 0 && isFavoriteBooks && !loading">
              <CustomText :mt="SIZES.m" variant="paragraph">
                У вас нет сохраненных учебников, добавить их можно в разделе
                <span class="link" @click="$router.push(`/library`)"
                  >Библиотека</span
                >
              </CustomText>
            </div>
          </div>
        </div>
        <div v-loading="loading" class="requests__loader"></div>
      </el-col>
      <el-col :span="5" :offset="1">
        <LibraryFilters :isMyLibrary="isMyLibrary" />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import moment from "moment";

import { SIZES } from "@/utils/appConsts";
import PageHeader from "@/common/PageHeader";
import SearchBar from "@/common/SearchBar";
import Modal from "./LibraryModal.vue";
import CustomText from "@/common/CustomText";
import LibraryFilters from "@/components/Library/LibraryFilters";
import Book from "@/components/Library/Book";
import {
  editBook,
  getBook,
  getBooks,
  uploadBook,
  getFavoriteBooks,
} from "@/api/books";
import { scrollMixin } from "@/mixins/scrollMixin";
import { mapState } from "vuex";

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
  props: {
    isMyLibrary: {
      type: Boolean,
      default: false,
    },
    isFavoriteBooks: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      SIZES,
      limit: 10,
      books: [],
      loading: false,
      count: null,
      sortTypes: [
        {
          key: "-publication_year",
          label: "По году ↓",
        },
        {
          key: "publication_year",
          label: "По году ↑",
        },
        {
          key: "-title",
          label: "По названию ↓",
        },
        {
          key: "title",
          label: "По названию ↑",
        },
      ],
      showModal: false,
      changingId: null,
      modalData: this.getInitBookData(),
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.app.userId,
    }),
    sort: {
      get() {
        return this.$route.query.sort || "-publication_year";
      },
      set(value) {
        this.$router.push({
          query: {
            ...this.$route.query,
            sort: value,
          },
        });
      },
    },
    search: {
      get() {
        return this.$route.query.search || "";
      },
      set(value) {
        this.$router.push({
          query: {
            ...this.$route.query,
            search: value,
          },
        });
      },
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    loadMore() {
      if (!this.loading) {
        this.fetchData();
      }
    },
    deleteFavBook(id) {
      if (this.isFavoriteBooks) {
        this.books = this.books.filter((item) => item.id !== id);
      }
    },
    fetchData() {
      if (this.books.length < this.count || this.count === null) {
        this.loading = true;
        const { author, subject, year } = this.$route.query;
        if (this.isFavoriteBooks) {
          getFavoriteBooks(
            this.lodash.pickBy({
              ordering: this.sort,
              authors: author,
              subjects: subject,
              end_year: year,
              start_year: year,
              search: this.search,
              limit: this.limit,
              offset: this.books.length,
              user: this.isMyLibrary ? this.userId : undefined,
            })
          ).then((res) => {
            this.count = res.data.count;
            this.books = [...this.books, ...res.data.results];
            this.loading = false;
          });
        } else {
          getBooks(
            this.lodash.pickBy({
              ordering: this.sort,
              authors: author,
              subjects: subject,
              end_year: year,
              start_year: year,
              search: this.search,
              limit: this.limit,
              offset: this.books.length,
              user: this.isMyLibrary ? this.userId : undefined,
            })
          ).then((res) => {
            this.count = res.data.count;
            this.books = [...this.books, ...res.data.results];
            this.loading = false;
          });
        }
      }
    },
    addNewBook() {
      this.showModal = true;
      this.changingId = null;
    },
    searchBook(value) {
      this.search = value;
    },
    deleteSearchInput() {
      this.search = "";
    },
    clearHandler() {
      console.log("clearHandler func");
    },
    getInitBookData() {
      return {
        authors: [],
        publishers: null,
        publishDate: null,
        bookName: "",
        annotation: "",
        pageCount: 0,
        subjects: [],
        book: [],
        bookCover: [],
      };
    },
    async onSave(data) {
      const { changingId } = this;
      const formData = new FormData();

      formData.set(
        "data",
        JSON.stringify(
          this.lodash.pickBy({
            title: data.bookName,
            annotation: data.annotation,
            publication_year: moment(data.publishDate).format("YYYY"),
            authors: data.authors,
            publishers: data.publishers,
            subjects: data.subjects,
            page_count: data.pageCount,
          })
        )
      );

      if (data.bookCover.length) {
        formData.set("image", data.bookCover[0].raw);
      }

      if (!changingId) {
        formData.set("content", data.book[0].raw);
      }

      try {
        if (changingId) {
          await editBook(changingId, formData);
        } else {
          await uploadBook(formData);
          this.books = [];
          this.count = null;
          this.fetchData();
        }
      } catch (e) {
        this.$message({
          message: `Не удалось ${
            changingId ? "отредактировать" : "сохранить"
          } книгу`,
          type: "error",
        });
        console.error(
          `Не удалось ${changingId ? "отредактировать" : "создать"} книгу:`,
          e
        );
      }

      if (changingId) {
        try {
          const bookData = (await getBook(changingId)).data;

          this.books = this.books.map((item) =>
            item.id === changingId ? bookData : item
          );
        } catch (e) {
          console.warn(`не удалось отобразить новые данные: ${e}`, e);
        }
      }
    },
    onBookEdit(item) {
      this.modalData = {
        authors: item.authors,
        publishers: item.publishers[0],
        publishDate: `${item.publication_year}`,
        bookName: item.title,
        annotation: item.annotation,
        pageCount: item.page_count,
        subjects: item.subjects,
        bookCover: [],
      };

      this.showModal = true;
      this.changingId = item.id;
    },
    onClose() {
      this.showModal = false;
      this.modalData = this.getInitBookData();
    },
  },
  watch: {
    isFavoriteBooks() {
      this.count = null;
      this.books = [];
      this.fetchData();
    },
    $route() {
      this.count = null;
      this.books = [];
      this.fetchData();
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.root {
}

.link {
  color: $darkBlue;
  cursor: pointer;
}

.sort {
  display: flex;
  align-items: center;
}

.content {
  margin-top: $l;
}
</style>
