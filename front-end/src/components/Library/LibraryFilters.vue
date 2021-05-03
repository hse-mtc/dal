<template>
  <div class="filters">
    <div class="filters-header">
      <div class="d-flex align-items-center">
        <img src="@/assets/icons/filter.svg" alt="">
        <CustomText variant="sub-header" :ml="SIZES.xs">
          Фильтры
        </CustomText>
      </div>
      <div @click="clear">
        <CustomText
          variant="paragraph"
          :custom-style="{cursor: 'pointer'}"
          :color="COLORS.darkBlue"
        >
          Сбросить
        </CustomText>
      </div>
    </div>
    <div v-if="!isMyLibrary" class="filter">
      <div class="filters-title pl-1 mb-2">
        Автор
      </div>
      <el-select
        v-model="author"
        clearable
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
    </div>

    <div class="filter">
      <div class="filters-title pl-1 mb-2">
        Год издания
      </div>
      <el-select
        v-model="year"
        clearable
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
      <div class="filters-title pl-1 mb-2">
        Предмет
      </div>
      <el-select
        v-model="subject"
        clearable
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
import { SIZES, COLORS } from "@/utils/appConsts";
import CustomText from "@/common/CustomText";
import { mapState } from "vuex";
import { surnameWithInitials } from "@/utils/person";

export default {
  name: "LibraryFilters",
  components: { CustomText },
  props: {
    isMyLibrary: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      SIZES,
      COLORS,
      author: undefined,
      year: undefined,
      years: Array(
        new Date().getUTCFullYear() - (new Date().getUTCFullYear() - 100),
      )
        .fill("")
        .map((v, idx) => new Date().getUTCFullYear() - idx),
      subject: undefined,
    };
  },
  computed: {
    ...mapState({
      authors: state => state.documents.authors,
      subjects: state => state.subjects.subjects,
    }),
  },
  created() {
    this.author = this.$route.query.author
      ? Number(this.$route.query.author)
      : undefined;
    this.subject = this.$route.query.subject
      ? Number(this.$route.query.subject)
      : undefined;
    this.year = this.$route.query.year
      ? Number(this.$route.query.year)
      : undefined;
  },
  methods: {
    surnameWithInitials,
    updateQuery() {
      const query = {
        author: this.author,
        subject: this.subject,
        year: this.year,
      };

      this.$router.push({ query: { ...this.$route.query, ...query } });
    },
    clear() {
      this.author = undefined;
      this.subject = undefined;
      this.year = undefined;
      this.updateQuery();
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.filters {
  margin-top: $l;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter {
  margin-top: $l;
}

.filters-select {
  width: 100%;
}
</style>
