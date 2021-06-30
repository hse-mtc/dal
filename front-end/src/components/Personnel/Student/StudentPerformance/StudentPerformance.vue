<template>
  <ExpandBox title="Успеваемость" @toggled="toggled">
    <el-table :data="performance" max-height="200" size="mini">
      <el-table-column prop="discipline" label="Дисциплина" />
      <el-table-column label="Средний балл">
        <template #default="{ row }">
          <el-tag :type="tagVariantByAverageMark(row.average_mark)">
            {{ row.average_mark }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Кол-во пропусков">
        <template #default="{ row }">
          <el-tag :type="tagVariantByAbsences(row.absences)">
            {{ row.absences }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import { findStudentPerformance } from "@/api/students";
import { getError } from "@/utils/message";

export default {
  name: "StudentPerformance",
  components: { ExpandBox },
  data() {
    return {
      performance: [],
      loading: false,
      id: this.$route.params.studentId,
    };
  },
  methods: {
    tagVariantByAverageMark(average) {
      if (average >= 4.5) {
        return "primary";
      }
      if (average >= 3.5) {
        return "success";
      }
      if (average >= 2.5) {
        return "warning";
      }
      return "danger";
    },
    tagVariantByAbsences(absences) {
      if (absences === 0) {
        return "success";
      }
      if (absences <= 2) {
        return "warning";
      }
      return "danger";
    },
    async fetchInfo() {
      try {
        this.loading = true;
        this.performance = (await findStudentPerformance(this.id)).data;
      } catch (err) {
        getError("информации об успеваемости студента", err);
      } finally {
        this.loading = false;
      }
    },
    toggled(expanded) {
      if (expanded) {
        this.fetchInfo();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
