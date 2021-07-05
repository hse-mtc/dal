<template>
  <ExpandBox title="Дисциплина" @toggled="toggled">
    <div class="discipline-info">
      <div class="discipline-table">
        <span class="title"> Поощрения </span>
        <PrimeTable
          :value="encouragements"
          scrollable
          scroll-height="200px"
          class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
        >
          <PrimeColumn column-key="date" header="Дата" :field="dateField" />
          <PrimeColumn
            column-key="reason"
            header="Причина"
            :field="(row) => row.reason"
          />
          <template #empty>
            Нет данных.
          </template>
        </PrimeTable>
        <div class="separator" />
      </div>
      <div class="discipline-table">
        <span class="title"> Текущие взыскания </span>
        <PrimeTable
          :value="currentPunishments"
          scrollable
          scroll-height="200px"
          class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
        >
          <PrimeColumn column-key="date" header="Дата" :field="dateField" />
          <PrimeColumn
            column-key="reason"
            header="Причина"
            :field="(row) => row.reason"
          />
          <template #empty>
            Нет данных.
          </template>
        </PrimeTable>
        <div class="separator" />
      </div>
      <div class="discipline-table">
        <span class="title"> Снятые взыскания </span>
        <PrimeTable
          :value="removedPunishments"
          scrollable
          scroll-height="200px"
          class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
        >
          <PrimeColumn column-key="date" header="Дата" :field="dateField" />
          <PrimeColumn
            column-key="remove_date"
            header="Дата снятия"
            :field="dateField"
          />
          <PrimeColumn
            column-key="reason"
            header="Причина"
            :field="(row) => row.reason"
          />
          <template #empty>
            Нет данных.
          </template>
        </PrimeTable>
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
    dateField: row => moment(row.date).format("DD.MM.YYYY"),
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
