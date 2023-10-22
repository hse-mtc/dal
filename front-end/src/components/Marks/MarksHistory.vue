<template>
  <el-dialog
    width="90%"
    :visible="visible"
    @close="$emit('close')"
  >
    <span slot="title" style="font-size: 20pt">
      История изменения оценок: {{ subjectName }}
    </span>
    <PrimeTable :value="historyMarksData" style="margin-top: -20px">
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
import { getMarkHistory, getMarkJournal } from "@/api/mark";

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
  created() {
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
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
