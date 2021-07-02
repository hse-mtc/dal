<template>
  <el-col :offset="1" :span="22" class="scienceWork">
    <el-row class="pageTitle">
      <el-col :span="24">
        <div class="d-flex align-items-center justify-content-between">
          Методические материалы
        </div>
      </el-col>
    </el-row>

    <el-row class="search">
      <el-col :span="24">
        <SearchForSubjects placeholder="Введите название предмета" />
        <el-row
          v-if="filteredSubjects.length !== 0"
          class="subjects"
          :gutter="20"
        >
          <el-col
            v-for="(item, index) in filteredSubjects"
            :key="index"
            :span="12"
            class="subjects-wrapper mt-5"
          >
            <el-col>
              <SubjectCard
                :id="item.id"
                :annotation="item.annotation"
                :title="item.title"
                :is-my-subject="userId === item.user.id"
                :owner="`${item.user.email}`"
              />
            </el-col>
          </el-col>
        </el-row>
        <div v-else>
          Предметов с таким названием не найдено.
        </div>
      </el-col>
    </el-row>
  </el-col>
</template>

<script>
import { getSubjects } from "@/api/subjects";
import SubjectCard from "@/components/SubjectCard/SubjectCard";
import { mapState, mapActions } from "vuex";
import SearchForSubjects from "@/components/Search/SearchForSubjects";

export default {
  name: "",
  components: {
    SubjectCard,
    SearchForSubjects,
  },
  data() {
    return {};
  },
  computed: {
    ...mapState({
      userId: state => state.app.userId,
      subjects: state => state.subjects.subjects,
    }),
    filteredSubjects() {
      if (this.$route.query.subjectsSearch) {
        const { subjectsSearch } = this.$route.query;
        if (subjectsSearch.trim()) {
          return this.subjects
            .filter(item => item.title.toUpperCase().includes(subjectsSearch.toUpperCase()));
        }
        return this.subjects;
      }
      return this.subjects;
    },
  },
  created() {
    this.fetchData();
  },
  methods: {
    ...mapActions({
      setSubjects: "subjects/setSubjects",
    }),
    fetchData() {
      if (this.subjects.length === 0) {
        getSubjects()
          .then(response => {
            this.setSubjects(response.data);
          })
          .catch(() => {
            console.log("Данные по предметам не указаны");
          });
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
