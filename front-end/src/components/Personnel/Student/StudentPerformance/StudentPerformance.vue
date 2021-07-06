<template>
  <ExpandBox title="Успеваемость" @toggled="toggled">
    <PrimeTable
      :value="performance"
      scrollable
      scroll-height="200"
      class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
    >
      <PrimeColumn
        column-key="discipline"
        header="Дисциплина"
        :field="(row) => row.discipline"
      />
      <PrimeColumn header="Средний балл" body-style="text-align: center;">
        <template #body="{ data }">
          <el-tag :type="tagVariantByAverageMark(data.average_mark)">
            {{ data.average_mark }}
          </el-tag>
        </template>
      </PrimeColumn>
      <PrimeColumn header="Кол-во пропусков" body-style="text-align: center;">
        <template #body="{ data }">
          <el-tag :type="tagVariantByAbsences(data.absences)">
            {{ data.absences }}
          </el-tag>
        </template>
      </PrimeColumn>
    </PrimeTable>
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
    };
  },
  computed: {
    id() {
      return this.$route.params.studentId;
    },
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
