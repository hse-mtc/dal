<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <PageHeader title="Мои материалы" />
      <Statistics />
    </el-col>
    <el-col :span="24">
      <div v-if="personType !== 'student'" class="tabs">
        <div
          v-for="item in tabs"
          :key="item.value"
          class="tab"
          :class="{ active: activeTab === item.value }"
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
        <Library :is-my-library="true" />
      </div>
      <div v-if="activeTab === 'books'">
        <Library :is-favorite-books="true" />
      </div>
    </el-col>
  </el-row>
</template>

<script>
import Statistics from "@/components/MyMaterials/Statistics";
import PageHeader from "@/common/PageHeader";
import MyDisciplines from "@/components/MyMaterials/MyDisciplines";
import MyDocuments from "@/components/MyMaterials/MyDocuments";
import Library from "@/components/Library/Library";
import { UserModule } from "@/store";
import { hasPermission } from "@/utils/permissions";

export default {
  name: "MyMaterials",
  components: {
    Library,
    MyDisciplines,
    MyDocuments,
    Statistics,
    PageHeader,
  },
  data() {
    return {
      activeTab: "",
      tabs: [],
    };
  },
  computed: {
    personType() {
      return UserModule.personType;
    },
  },

  mounted() {
    if (hasPermission(["subjects.post.self"])) {
      this.tabs.push({ label: "Дисциплины", value: "disciplines" });
    }

    if (hasPermission(["papers.post.self"])) {
      this.tabs.push({ label: "Военно-научные работы", value: "works" });
    }

    if (hasPermission(["books.post.self"])) {
      this.tabs.push({ label: "Электронная библиотека", value: "library" });
    }

    if (hasPermission(["favorite-books.post.self"])) {
      this.tabs.push({ label: "Сохраненные книги", value: "books" });
    }

    if (this.personType === "student") {
      this.activeTab = "books";
    } else {
      this.activeTab = this.tabs[0].value;
    }
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
