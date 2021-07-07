<template>
  <div class="root">
    <div v-if="statistics" class="statistics">
      <div
        v-for="(item, index) in Object.keys(statistics)"
        :key="index"
        class="statistics-card"
        :style="{ background: cards[item].color }"
      >
        <div class="statistics-card-number">
          <CustomText :color="COLORS.white" variant="header">
            {{
              statistics[item]
            }}
          </CustomText>
        </div>
        <CustomText :color="COLORS.white" variant="paragraph">
          {{ cards[item].name }}
        </CustomText>
      </div>
    </div>
  </div>
</template>

<script>
import { SIZES, COLORS } from "@/utils/appConsts";
import { getStatistics } from "@/api/statistics";
import CustomText from "@/common/CustomText";
import { UserModule } from "@/store";

// TODO make one component with Subjects for ex if u have a param,
// than hide title and search and do a request with user id
export default {
  name: "MyMaterials",
  components: {
    CustomText,
  },
  data() {
    return {
      SIZES,
      COLORS,
      statistics: null,
      cards: {
        paper_count: { color: "#0061D9", name: "Материалов загружено" },
        subject_count: { color: "#3CA0EA", name: "Дисцплин разработано" },
        book_count: { color: "#3D9E3B", name: "Книг в библиотеке" },
      },
    };
  },
  computed: {
    userId() { return UserModule.userId; },
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      getStatistics(this.userId)
        .then(res => {
          this.statistics = res.data;
        })
        .catch(() => {
          console.log("Проблема с загрузкой данных");
        });
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.statistics {
  display: flex;
  margin-bottom: $xxxxl;
  &-card {
    flex: none;
    margin-right: $xxxxl;
    align-items: center;
    color: $white;
    width: 241px;
    height: 92px;
    display: flex;
    padding: 12px;
    box-shadow: 0px 4px 10px rgba(0, 97, 217, 0.25);
    border-radius: 12px;

    &-number {
      flex: none;
      margin-right: $m;
      display: flex;
      justify-content: center;
      align-items: center;
      width: 85px;
      height: 68px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 12px;
    }
  }
}
</style>
