<template>
  <div>
    <div class="my-advanced-search" @click="advancedClick">
      <div class="d-flex align-items-center">
        <div class="my-advanced-search-text" style="cursor: pointer">
          Расширенный поиск
        </div>
        <img
          src="../../assets/scienceWorks/dropdown.svg"
          alt=""
          class="my-advanced-search-arrow ml-2"
        >
      </div>
    </div>
    <div class="filters mt-3 pt-3 pb-3" style="display: none">
      <el-row class="">
        <el-col :span="10" :offset="1">
          <div class="filters-title pl-1">
            Автор
          </div>
          <el-select
            v-model="author"
            clearable
            filterable
            placeholder="Все авторы"
            class="filters-select"
            @change="updateQuery"
          >
            <el-option
              v-for="item in authors"
              :key="item.id"
              :value="item.id"
              :label="surnameWithInitials(item)"
            />
          </el-select>
        </el-col>
        <el-col :span="10" :offset="1">
          <div class="filters-title pl-1">
            Размещение
          </div>
          <el-select
            v-model="publisher"
            clearable
            filterable
            placeholder="Все размещения"
            class="filters-select"
            @change="updateQuery"
          >
            <el-option
              v-for="{ id, name } in publishers"
              :key="id"
              :value="id"
              :label="name"
            />
          </el-select>
        </el-col>
      </el-row>
      <el-row class="mt-3">
        <el-col :offset="1" :span="10">
          <div class="filters-title pl-1">
            Период публикации
          </div>
          <el-date-picker
            v-model="valueDate"
            type="daterange"
            align="right"
            unlink-panels
            start-placeholder="Начало"
            end-placeholder="Конец"
            :picker-options="{ firstDayOfWeek: 1 }"
            @change="updateQuery"
          />
        </el-col>
      </el-row>

      <!-- Динамические фильтры для категории -->
      <div v-if="currentCategoryFilters.length > 0" class="mt-4">
        <div class="filters-title pl-1 mb-3">
          <strong>Фильтры категории "{{ currentCategory.title }}"</strong>
        </div>
        <el-row
          v-for="(filter, index) in currentCategoryFilters"
          :key="index"
          :class="index > 0 ? 'mt-3' : ''"
        >
          <el-col :offset="1" :span="10">
            <div class="filters-title pl-1">
              {{ filter.filtername }}
            </div>

            <!-- Поле для строкового фильтра -->
            <el-input
              v-if="filter.type === 'string'"
              v-model="categoryFilters[filter.filtername]"
              :placeholder="`Введите ${filter.filtername.toLowerCase()}`"
              clearable
              @input="updateQuery"
            />

            <!-- Поле для числового фильтра -->
            <el-input-number
              v-else-if="filter.type === 'number'"
              v-model="categoryFilters[filter.filtername]"
              :placeholder="`Введите ${filter.filtername.toLowerCase()}`"
              style="width: 100%"
              @input="updateQuery"
            />
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { Component, Vue, Watch } from "vue-property-decorator";
import moment from "moment";
import { surnameWithInitials } from "@/utils/person";
import { PapersModule } from "@/store";

@Component({
  name: "AdvancedPaperSearch",
})
class AdvancedPaperSearch extends Vue {
  author = null
  publisher = null
  valueDate = ""
  categoryFilters = {}

  get publishers() { return PapersModule.publishers; }
  get authors() { return PapersModule.authors; }
  get categories() { return PapersModule.categories; }

  // Получаем текущую категорию на основе route параметра
  get currentCategory() {
    const categoryId = this.$route.query.category;
    if (!categoryId) { return null; }
    return this.categories.find(cat => cat.id === parseInt(categoryId, 10)) || null;
  }

  // Получаем фильтры из JSON Schema формата
  get currentCategoryFilters() {
    if (!this.currentCategory || !this.currentCategory.filters || !this.currentCategory.filters.properties) {
      return [];
    }

    return Object.keys(this.currentCategory.filters.properties).map(propertyName => ({
      filtername: propertyName,
      type: this.currentCategory.filters.properties[propertyName].type,
    }));
  }

  surnameWithInitials = surnameWithInitials

  // Отслеживаем изменение route для обновления фильтров категории
  @Watch("$route")
  onRouteChange() {
    this.initializeCategoryFilters();
  }

  advancedClick() {
    const filters = document.querySelector(".filters");
    const array = document.querySelector(".my-advanced-search-arrow");
    if (filters.style.display === "none") {
      filters.style.display = "block";
      array.style.transform = "rotate(180deg)";
    } else {
      filters.style.display = "none";
      array.style.transform = "rotate(0deg)";
    }
  }

  created() {
    // Инициализируем фильтры категории из query параметров
    this.initializeCategoryFilters();

    // Инициализируем стандартные фильтры
    this.author = this.$route.query.authors ? parseInt(this.$route.query.authors, 10) : null;
    this.publisher = this.$route.query.publishers ? parseInt(this.$route.query.publishers, 10) : null;

    // Инициализируем дату из query параметров
    if (this.$route.query.start_date && this.$route.query.end_date) {
      this.valueDate = [
        new Date(this.$route.query.start_date),
        new Date(this.$route.query.end_date),
      ];
    }
  }

  initializeCategoryFilters() {
    this.categoryFilters = {};
    if (this.currentCategoryFilters.length > 0) {
      this.currentCategoryFilters.forEach(filter => {
        const paramKey = `filter_${filter.filtername}`;
        const queryValue = this.$route.query[paramKey];

        if (queryValue) {
          if (filter.type === "number") {
            this.categoryFilters[filter.filtername] = parseFloat(queryValue);
          } else {
            this.categoryFilters[filter.filtername] = queryValue;
          }
        }
      });
    }
  }

  updateQuery() {
    const query = {
      authors: this.author,
      category: this.$route.query.category,
      publishers: this.publisher,
      search: this.$route.query.search,
    };

    if (this.valueDate) {
      query.start_date = moment(this.valueDate[0]).format("YYYY-MM-DD");
      query.end_date = moment(this.valueDate[1]).format("YYYY-MM-DD");
    }

    // Добавляем фильтры категории в query
    if (this.currentCategoryFilters.length > 0) {
      this.currentCategoryFilters.forEach(filter => {
        const filterValue = this.categoryFilters[filter.filtername];
        if (filterValue !== null && filterValue !== undefined && filterValue !== "") {
          query[`filter_${filter.filtername}`] = filterValue;
        }
      });
    }

    this.$router.push({ query });
  }
}

export default AdvancedPaperSearch;
</script>

<style scoped lang="scss">
@import "papers-advanced";
</style>
