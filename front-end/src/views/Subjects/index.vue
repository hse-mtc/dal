<template>
  <div :class="$style.root">
    <h1>Учебно-методические материалы</h1>
    <div v-if="personType !== 'student'" style="margin-top: 25px">
      <el-row class="filterRow" :gutter="20">
        <el-col :span="6">
          <span style="margin-right: 15px; font-weight: bold">ВУС</span>
          <el-select
            v-model="milspecialty"
            filterable
            placeholder="ВУС"
          >
            <el-option
              v-for="item in milspecialties"
              :key="item.id"
              :label="item.code"
              :value="item.id"
            />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <div :class="$style.cardsWrapper">
      <SubjectsCards
        v-if="subjects.length"
        :cards="subjects"
      />
      <div v-else>
        Предметов с такой ВУС не найдено.
      </div>
    </div>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";

import { SubjectsModule, UserModule } from "@/store";
import { getMilSpecialties } from "@/api/reference-book";
import SubjectsCards from "@/components/@Subjects/SubjectsPage/SubjectsCards.vue";

@Component({
  name: "SubjectsPage",
  components: { SubjectsCards },
  data() {
    return {
      milspecialty: "",
      milspecialties: [],
    };
  },
  computed: {
    personType() {
      return UserModule.personType;
    },
  },
})
class SubjectsPage extends Vue {
  async mounted() {
    this.milspecialties = (await getMilSpecialties()).data;
    this.milspecialty = this.milspecialties[0].id;
  }

  get searchQuery() { return this.$route.query.subjectsSearch || ""; }
  set searchQuery(newValue) {
    this.$router.replace({
      query: {
        subjectsSearch: newValue,
      },
    });
  }

  get subjects() {
    const milSpecSubjects = SubjectsModule.subjects.filter(
      subj => subj.milspecialty === this.milspecialty,
    );
    if (!this.searchQuery) { return milSpecSubjects; }

    const words = this.searchQuery.toLowerCase().split();
    return milSpecSubjects.filter(({ title, annotation, user: { email } }) => {
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
  margin-top: 35px;

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
