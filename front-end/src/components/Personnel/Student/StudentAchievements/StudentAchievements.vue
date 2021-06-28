<template>
  <ExpandBox title="Умения и достижения" @toggled="toggled">
    <div class="achievements-info">
      <div class="achievements-table">
        <span class="title"> Достижения </span>
        <el-table :data="achievements" max-height="200" size="mini">
          <el-table-column prop="date" label="Дата" :formatter="formatDate" />
          <el-table-column label="Тип">
            <template slot-scope="{ row }">
              <el-tag :type="tagVariantByType(row.achievement_type)">
                {{ row.achievement_type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="text" label="Описание" show-overflow-tooltip />
        </el-table>
        <div class="separator" />
      </div>
      <div class="achievements-table">
        <span class="title"> Умения </span>
        <el-table :data="skills" max-height="200" size="mini">
          <el-table-column prop="title" label="Наименование" />
        </el-table>
        <div class="separator" />
      </div>
    </div>
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import moment from "moment";
import { getAchievement } from "@/api/achievement";
import { getError } from "@/utils/message";
import { findStudentSkills } from "@/api/students";

export default {
  name: "StudentAchievements",
  components: { ExpandBox },
  data() {
    return {
      achievements: [],
      skills: [],
      loading: false,
      id: this.$route.params.studentId,
    };
  },
  methods: {
    formatDate: row => (moment(row.date).isValid()
      ? moment(row.date).format("DD.MM.YYYY")
      : "---"),
    tagVariantByType(type) {
      switch (type) {
        case "Спортивные":
          return "danger";
        case "Научные":
          return "primary";
        default:
          return "";
      }
    },
    async fetchInfo() {
      try {
        this.loading = true;
        this.achievements = (await getAchievement({ student: this.id })).data;
        this.skills = (await findStudentSkills(this.id)).data;
      } catch (err) {
        getError("информации о достижениях студента", err);
      } finally {
        this.loading = false;
      }
    },
    async toggled(expanded) {
      if (expanded) {
        await this.fetchInfo();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
