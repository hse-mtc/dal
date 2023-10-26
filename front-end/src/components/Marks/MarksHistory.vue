<template>
  <el-dialog
    width="90%"
    :visible="visible"
    @close="$emit('close')"
  >
    <span slot="title" style="font-size: 20pt">
      История изменения оценок: {{ subjectName }}
    </span>

    <div>
      <table class="lesson-info-table">
        <tbody>
          <tr>
            <td class="field-name">
              Взвод:
            </td>
            <td>{{ milgroupTitle }}</td>
          </tr>
          <tr>
            <td class="field-name">
              Период:
            </td>
            <td>{{ formatDateRange(dateRange) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <PrimeTable :value="historyMarksData">
      <PrimeColumn
        header="Дата изменения"
        :rowspan="2"
        :field="(row) => formatDateTime(row.update_date)"
        column-key="date"
        header-style="width: 180px"
      />
      <PrimeColumn
        header="Дата занятия"
        :rowspan="2"
        :field="(row) => formatDate(row.lesson_date)"
        column-key="lessondate"
        header-style="width: 160px"
      />
      <PrimeColumn
        header="Студент"
        :rowspan="2"
        :field="(row) => row.student_fullname"
        column-key="student"
      />
      <PrimeColumn
        header="Оценка до"
        :rowspan="2"
        :field="(row) => row.before"
        column-key="before"
        header-style="width: 160px"
      >
        <template #body="{ data }">
          <div class="mark-journal-cell" style="justify-content: left">
            <div>
              <el-tag
                v-for="m in data.before"
                :key="m"
                effect="dark"
                disable-transitions
                class="margin-all"
                :type="tagByMark(m)"
              >
                {{ m }}
              </el-tag>
            </div>
          </div>
        </template>
      </PrimeColumn>
      <PrimeColumn
        header="Оценка после"
        :rowspan="2"
        :field="(row) => row.after"
        column-key="after"
        header-style="width: 160px"
      >
        <template #body="{ data }">
          <div class="mark-journal-cell" style="justify-content: left">
            <div>
              <el-tag
                v-for="m in data.after"
                :key="m"
                effect="dark"
                disable-transitions
                class="margin-all"
                :type="tagByMark(m)"
              >
                {{ m }}
              </el-tag>
            </div>
          </div>
        </template>
      </PrimeColumn>
      <PrimeColumn
        header="Изменил"
        :rowspan="2"
        :field="(row) => row.changed_by_fullname"
        column-key="teacher"
      />
    </PrimeTable>
  </el-dialog>
</template>

<script>
import moment from "moment";
import { getMarkHistory } from "@/api/mark";
import { ReferenceModule } from "@/store";

export default {
  name: "MarksHistory",
  props: {
    visible: {
      type: Boolean,
      default: true,
    },
    mg: {
      type: Number,
      default: 0,
    },
    dateRange: {
      type: Array[Date],
      default: () => [
        moment()
          .add(-3, "months")
          .format("YYYY-MM-DD"),
        moment().format("YYYY-MM-DD"),
      ],
    },
    subjectId: {
      type: Number,
      default: 0,
    },
    subjectName: {
      type: String,
      default: "subjectName",
    },
  },
  data() {
    return {
      subjects: [],
      historyMarksData: [],
    };
  },
  computed: {
    milgroupTitle() {
      const curMilgroup = ReferenceModule.milgroups.filter(milgroup => milgroup.id === this.mg);
      if (curMilgroup.length > 0) {
        return curMilgroup[0].title;
      }
      return "";
    },
    infoData() {
      return [
        { field_name: "Взвод", value: this.milgroupTitle },
        { field_name: "Период", value: this.dateRange },
      ];
    },
  },
  watch: {
    visible(newValue) {
      if (newValue) {
        getMarkHistory({
          milgroup: this.mg,
          subject: this.subjectId,
          date_from: this.dateRange[0],
          date_to: this.dateRange[1],
          history: true,
        })
          .then(response => {
            this.historyMarksData = response.data;
          });
      }
    },
  },
  methods: {
    formatDate: d => moment(d).format("DD.MM.YY"),
    formatDateTime: d => moment(d).format("DD.MM.YY HH:mm"),
    tagByLessonType(type) {
      switch (type) {
        case "LE":
          return "primary";
        case "SE":
          return "danger";
        case "GR":
          return "warning";
        case "PR":
          return "success";
        case "FI":
          return "info";
        case "EX":
          return "info";
        default:
          return "info";
      }
    },
    tagByMark(mark) {
      switch (mark) {
        case 5:
          return "primary";
        case 4:
          return "success";
        case 3:
          return "warning";
        case 2:
          return "danger";
        default:
          return "info";
      }
    },
    getSubjectTitle(subjectId) {
      return this.subjects.filter(item => item.id === subjectId)[0]?.title || "";
    },
    formatDateRange(dataRange) {
      const startDate = moment(dataRange[0]);
      const endDate = moment(dataRange[1]);
      return `с ${startDate.format("DD.MM.yyyy")} по ${endDate.format("DD.MM.yyyy")}`;
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
