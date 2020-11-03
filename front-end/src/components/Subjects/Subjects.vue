<template>
  <div>
    <el-row v-if="filteredSubjects.length !== 0" class="subjects mt-0">
      <el-col
        :span="8"
        v-for="(item, index) in filteredSubjects"
        :key="index"
        class="subjects-wrapper mt-5"
      >
        <el-col>
          <div
            class="subjects-card"
            :id="item.id"
            v-bind:class="{ 'm-0': ++index % 3 === 0 }"
            @click="selectSubject"
          >
            {{ item.title }}
          </div>
        </el-col>
      </el-col>
    </el-row>
    <div v-else>Предметов с таким названием не найдено.</div>
  </div>
</template>

<script>
import { getSubjects } from "@/api/subjects";

export default {
  name: "",
  components: {},
  data() {
    return {
      subjects: [],
      filteredSubjects: [],
    };
  },
  created() {
    if (this.$store.getters.subjects.length === 0) {
      getSubjects()
        .then((response) => {
          this.subjects = response.data;
          this.filteredSubjects = response.data;
          this.$store.dispatch("projectData/addSubjects", this.subjects);
          this.$router.replace({ name: "Teaching Materials" });
        })
        .catch(() => {
          // eslint-disable-next-line no-console
          console.log("Данные по предметам не указаны");
        });
    } else {
      this.subjects = this.$store.getters.subjects;
      this.filteredSubjects = this.$store.getters.subjects;
    }
  },
  mounted() {},
  methods: {
    selectSubject(event) {
      // eslint-disable-next-line no-console
      this.$router.push({
        query: {
          subjectId: event.target.id,
        },
      });
    },
  },
  watch: {
    $route(to, from) {
      if (this.$route.query.subjectsSearch) {
        const subjectsSearch = this.$route.query.subjectsSearch;
        if (subjectsSearch.trim()) {
          this.filteredSubjects = this.subjects.filter((item) =>
            item.title.toUpperCase().includes(subjectsSearch.toUpperCase())
          );
        } else {
          this.filteredSubjects = this.subjects;
        }
      } else {
        this.filteredSubjects = this.subjects;
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
