<template>
  <ExpandBox title="Дисциплина" @toggled="toggled">
    <div class="discipline-info">
      <div class="discipline-table">
        <span class="title"> Поощрения </span>
        <el-table :data="encouragements" max-height="200" size="mini">
          <el-table-column prop="date" label="Дата" :formatter="formatDate" />
          <el-table-column
            prop="reason"
            label="Причина"
            show-overflow-tooltip
          />
        </el-table>
        <div class="separator" />
      </div>
      <div class="discipline-table">
        <span class="title"> Текущие взыскания </span>
        <el-table :data="currentPunishments" max-height="200" size="mini">
          <el-table-column prop="date" label="Дата" :formatter="formatDate" />
          <el-table-column
            prop="reason"
            label="Причина"
            show-overflow-tooltip
          />
        </el-table>
        <div class="separator" />
      </div>
      <div class="discipline-table">
        <span class="title"> Снятые взыскания </span>
        <el-table :data="removedPunishments" max-height="200" size="mini">
          <el-table-column prop="date" label="Дата" :formatter="formatDate" />
          <el-table-column
            prop="remove_date"
            label="Дата снятия"
            :formatter="formatDate"
          />
          <el-table-column
            prop="reason"
            label="Причина"
            show-overflow-tooltip
          />
        </el-table>
      </div>
    </div>
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import { getError } from "@/utils/message";
import { getEncouragement } from "@/api/encouragement";
import { getPunishment } from "@/api/punishment";
import moment from "moment";

export default {
  name: "StudentDiscipline",
  components: { ExpandBox },
  data() {
    return {
      encouragements: [],
      currentPunishments: [],
      removedPunishments: [],
      loading: false,
    };
  },
  computed: {
    id() {
      return this.$route.params.studentId;
    },
  },
  methods: {
    formatDate: row => moment(row.date).format("DD.MM.YYYY"),
    async fetchInfo() {
      try {
        this.loading = true;
        this.encouragements = (
          await getEncouragement({ student: this.id })
        ).data;
        this.currentPunishments = (
          await getPunishment({ student: this.id, removed: false })
        ).data;
        this.removedPunishments = (
          await getPunishment({ student: this.id, removed: true })
        ).data;
      } catch (err) {
        getError("информации о дисциплине студента", err);
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
