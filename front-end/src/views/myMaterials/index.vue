<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <PageHeader title="Мои материалы" />
      <Statistics />
    </el-col>
    <el-col :span="24">
      <div class="tabs">
        <div
          class="tab"
          v-for="item in tabs"
          :class="{ active: activeTab === item.value }"
          :key="item.value"
          @click="changeTab(item.value)"
        >
          {{ item.label }}
        </div>
      </div>
    </el-col>
    <el-col :span="20" :offset="2">
      <div v-if="activeTab === 'disciplines'">
        <MyDisciplines />
      </div>
      <div v-if="activeTab === 'works'">
        <MyDocuments />
      </div>
      <div v-if="activeTab === 'library'">
        <Library :isMyLibrary="true" />
      </div>
      <div v-if="activeTab === 'books'">
        <Library :isFavoriteBooks="true" />
      </div>
    </el-col>
  </el-row>
</template>

<script>
import { mapGetters } from "vuex";
import Statistics from "@/components/MyMaterials/Statistics";
import PageHeader from "@/common/PageHeader";
import MyDisciplines from "@/components/MyMaterials/MyDisciplines";
import MyDocuments from "@/components/MyMaterials/MyDocuments";
import Library from "@/components/Library/Library";

export default {
  name: "MyMaterials",
  components: {
    Library,
    MyDisciplines,
    MyDocuments,
    Statistics,
    PageHeader,
  },
  computed: {
    ...mapGetters(["name"]),
  },
  data() {
    return {
      activeTab: "disciplines",
      tabs: [
        { label: "Дисциплины", value: "disciplines" },
        { label: "Военно-научные работы", value: "works" },
        { label: "Библиотека", value: "library" },
        { label: "Сохраненные учебники", value: "books" },
      ],
    };
  },
  methods: {
    changeTab(value) {
      this.activeTab = value;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.tabs {
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: $lightGray;
  padding: $m;
}

.tab {
  cursor: pointer;
  font-family: ProximaNovaRegular;
  font-style: normal;
  font-weight: normal;
  font-size: 24px;
  line-height: 29px;
}

.active {
  font-weight: bold;
}
</style>
