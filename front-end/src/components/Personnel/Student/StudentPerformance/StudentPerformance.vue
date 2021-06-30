<template>
  <ExpandBox title="Успеваемость" @toggled="toggled">
    <el-table :data="performance" max-height="200" size="mini">
      <el-table-column prop="discipline" label="Дисциплина" />
      <el-table-column label="Средний балл">
        <template #default="{ row }">
          <el-tag :type="tagVariantByMean(row.mean)">
            {{ row.mean }}
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

export default {
  name: "StudentPerformance",
  components: { ExpandBox },
  data() {
    return {
      performance: [
        {
          discipline: "ТСП",
          mean: 5,
          absences: 3,
        },
        {
          discipline: "ВСП",
          mean: 2,
          absences: 1,
        },
        {
          discipline: "СП",
          mean: 3.5,
          absences: 2,
        },
        {
          discipline: "ОП",
          mean: 4.3,
          absences: 0,
        },
      ],
    };
  },
  methods: {
    tagVariantByMean(mean) {
      if (mean >= 4.5) {
        return "primary";
      }
      if (mean >= 3.5) {
        return "success";
      }
      if (mean >= 2.5) {
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
    fetchData() {},
    toggled(expanded) {
      if (expanded) {
        this.fetchData();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
