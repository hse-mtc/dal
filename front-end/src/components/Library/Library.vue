<template>
  <div class="root">
    <PageHeader title="Библиотека" button="+ Добавить учебник" :click="addNewBook"/>
    <SearchBar placeholder="Введите название книги" :search="searchBook" :delete="deleteSearchInput"/>
    <CustomText :mt="SIZES.m" variant="paragraph">Найдено: {{ books.length }}</CustomText>
    <el-row>
      <el-col :span="18">
        <div class="sort mt-3">
          <CustomText variant="sub-header" :mr="SIZES.m">Сортировать</CustomText>
          <el-select
              v-model="sort"
              placeholder="Выберите тип причины"
              style="display: block"
              @change="updateQuery"
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
        <div class="content" v-loading="loading">

        </div>
      </el-col>
      <el-col :span="5" :offset="1">
        <LibraryFilters :clear="clearHandler" />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {SIZES} from "@/utils/appConsts"
import PageHeader from "@/common/PageHeader";
import SearchBar from "@/common/SearchBar";
import CustomText from "@/common/CustomText";
import LibraryFilters from "@/components/LibraryFilters";
import {getBooks} from "@/api/books";

export default {
  name: "Library",
  components: {
    LibraryFilters,
    CustomText,
    SearchBar,
    PageHeader
  },
  data() {
    return {
      SIZES,
      books: [],
      sort: '-publication_year',
      author: null,
      subject: null,
      year: null,
      search: '',
      loading: false,
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
      ]
    };
  },
  created() {
    this.sort = this.$route.query.sort ? this.$route.query.sort : '-publication_year'
    this.author = this.$route.query.author ? Number(this.$route.query.author) : undefined
    this.subject = this.$route.query.subject ? Number(this.$route.query.subject) : undefined
    this.year = this.$route.query.year ? Number(this.$route.query.year) : undefined
    this.search = this.$route.query.search ? this.$route.query.search : ''
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.loading = true
      this.author = this.$route.query.author ? Number(this.$route.query.author) : undefined
      this.subject = this.$route.query.subject ? Number(this.$route.query.subject) : undefined
      this.year = this.$route.query.year ? Number(this.$route.query.year) : undefined
      this.search = this.$route.query.search ? this.$route.query.search : undefined
      getBooks({ordering: this.sort, authors: this.author, subjects: this.subject, end_year: this.year, start_year: this.year, search: this.search})
      .then(res => {
        console.log('[BOOKS]: ', res.data)
        this.books = res.data
        this.loading = false
      })
    },
    updateQuery() {
      const query = {
        sort: this.sort,
        search: this.search
      };

      this.$router.push({query: {...this.$route.query, ...query}});
    },
    addNewBook() {
      console.log('addNewBook func')
    },
    searchBook(value) {
      this.search = value
      this.updateQuery()
    },
    deleteSearchInput() {
      this.search = ''
      this.updateQuery()
    },
    clearHandler() {
      console.log('clearHandler func')
    }
  },
  watch: {
    $route() {
      this.fetchData()
    },
  },
}
</script>

<style scoped lang="scss">
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
