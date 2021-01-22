<template>
  <div class="filters">
    <div class="filters-header">
      <div class="d-flex align-items-center">
        <img src="@/assets/icons/filter.svg" alt=""/>
        <CustomText variant="sub-header" :ml="SIZES.xs">Фильтры</CustomText>
      </div>
      <div @click="clear">
        <CustomText variant="paragraph" :custom-style="{cursor: 'pointer'}" :color="COLORS.darkBlue">Сбросить
        </CustomText>
      </div>
    </div>
    <div class="filter">
      <div class="filters-title pl-1 mb-2">Автор</div>
      <el-select
          clearable
          v-model="author"
          placeholder="Все авторы"
          class="filters-select"
          @change="updateQuery"
      >
        <el-option
            v-for="item in authors"
            :key="item.id"
            :value="item.id"
            :label="`${item.surname} ${item.name[0]}. ${item.patronymic[0]}.`"
        />
      </el-select>
    </div>

    <div class="filter">
      <div class="filters-title pl-1 mb-2">Год издания</div>
      <el-select
          clearable
          v-model="year"
          placeholder="Все года"
          class="filters-select"
          @change="updateQuery"
      >
        <el-option
            v-for="item in years"
            :key="item"
            :value="item"
            :label="item"
        />
      </el-select>
    </div>

    <div class="filter">
      <div class="filters-title pl-1 mb-2">Предмет</div>
      <el-select
          clearable
          v-model="subject"
          placeholder="Все предметы"
          class="filters-select"
          @change="updateQuery"
      >
        <el-option
            v-for="item in subjects"
            :key="item.id"
            :value="item.id"
            :label="item.title"
        />
      </el-select>
    </div>
  </div>
</template>

<script>
import {SIZES, COLORS} from "@/utils/appConsts"
import CustomText from "@/common/CustomText";
import {mapState} from "vuex";

export default {
  name: "LibraryFilters",
  components: {CustomText},
  created() {
    this.author = Number(this.$route.query.author)
    this.subject = Number(this.$route.query.subject)
    this.year = Number(this.$route.query.year)
  },
  methods: {
    updateQuery() {
      const query = {
        author: this.author,
        subject: this.subject,
        year: this.year,
      };

      this.$router.push({query: {...this.$route.query, ...query}});
    },
    clear() {
      this.author = undefined
      this.subject = undefined
      this.year = undefined
      this.updateQuery()
    }
  },
  computed: {
    ...mapState({
      authors: (state) => state.documents.authors,
      subjects: (state) => state.subjects.subjects,
    }),
  },
  data() {
    return {
      SIZES,
      COLORS,
      author: undefined,
      year: undefined,
      years: Array(new Date().getUTCFullYear() - (new Date().getUTCFullYear() - 100)).fill('').map((v, idx) => new Date().getUTCFullYear() - idx),
      subject: undefined,
    }
  },
  watch: {
    $route() {
      console.log(this.$route.query)
    },
  },
}
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.filters {

}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter {
  margin-top: $l
}

.filters-select {
  width: 100%;
}

</style>
