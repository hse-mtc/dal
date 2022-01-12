<template>
  <div :class="$style.root">
    <h1>Методические материалы</h1>

    <div :class="$style.searchWrapper">
      <input
        v-model="searchQuery"
        :class="$style.wordsSearch"
        placeholder="Введите название предмета, аннотацию или email"
      >
      <i
        :class="['el-icon-close', $style.deleteCross]"
        @click="searchQuery = ''"
      />
      <i :class="['el-icon-search', $style.searchIcon]" />
    </div>

    <div :class="$style.cardsWrapper">
      <SubjectsCards
        v-if="subjects.length"
        :cards="subjects"
      />
      <div v-else>
        Предметов с таким названием не найдено.
      </div>
    </div>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";

import { SubjectsModule } from "@/store";

import SubjectsCards from "@/components/@Subjects/SubjectsPage/SubjectsCards.vue";

@Component({
  name: "SubjectsPage",
  components: { SubjectsCards },
})
class SubjectsPage extends Vue {
  get searchQuery() { return this.$route.query.subjectsSearch || ""; }
  set searchQuery(newValue) {
    this.$router.replace({
      query: {
        subjectsSearch: newValue,
      },
    });
  }

  get subjects() {
    if (!this.searchQuery) { return SubjectsModule.subjects; }

    const words = this.searchQuery.toLowerCase().split();
    return SubjectsModule.subjects.filter(({ title, annotation, user: { email } }) => {
      const subjectKey = `${title} ${annotation} ${email}`.toLowerCase();

      return words.reduce(
        (memo, word) => memo && (!word || subjectKey.includes(word)),
        true,
      );
    });
  }
}

export default SubjectsPage;
</script>

<style lang="scss" module>
.root {
  padding: 50px;

  @media screen and (max-width: 640px) {
    padding: 10px;
  }
}

.cardsWrapper {
  margin-top: 50px;

  @media screen and (max-width: 640px) {
    margin-top: 20px;
  }
}

.searchWrapper {
  display: flex;
  margin-top: 20px;
  border-bottom: 1px solid #a7a7ab;
  align-items: center;

  .wordsSearch {
    width: 100%;
    background-color: inherit;
    border: none;
    padding-bottom: 10px;
    &:focus {
      outline: none;
    }
  }

  .searchIcon {
    margin-bottom: 10px;
    font-size: 25px;
    font-weight: bold;
    line-height: 25px;
    color: #0f65cc;
  }

  .deleteCross {
    display: none;
    margin-bottom: 10px;
    margin-right: 10px;
    font-size: 20px;
    font-weight: bold;
    line-height: 20px;
    cursor: pointer;
  }

  &:hover {
    .deleteCross {
      display: flex;
    }
  }
}

</style>
