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
    this.author = Number(this.$route.query.author)
    this.subject = Number(this.$route.query.subject)
    this.year = Number(this.$route.query.year)
  },
  mounted() {

  },
  methods: {
    fetchData() {

    },
    updateQuery() {
      const query = {
        sort: this.sort
      };

      this.$router.push({query: {...this.$route.query, ...query}});
    },
    addNewBook() {
      console.log('addNewBook func')
    },
    searchBook() {
      console.log('searchBook func')
    },
    deleteSearchInput() {
      console.log('deleteSearchInput func')
    },
    clearHandler() {
      console.log('clearHandler func')
    }
  }
}
</script>

<style scoped lang="scss">
.root {

}

.sort {
  display: flex;
  align-items: center;
}
</style>
