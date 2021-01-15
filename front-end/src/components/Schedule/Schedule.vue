<template>
  <div>
    <el-tabs tab-position="left" v-model="filter.mg" @tab-click="fetchData()">
      <el-tab-pane
        v-for="mg in milgroups"
        :key="mg.milgroup"
        :label="mg.milgroup"
        :name="mg.milgroup"
      >
        <el-table
          :data="schedule.ordinals"
          style="width: 100%"
          height="680"
          :default-sort="{
            prop: 'ordinal',
            order: 'ascending',
          }"
          stripe
          border
        >
          <el-table-column
            label="№"
            prop="ordinal"
            align="center"
            width="100"
            fixed
          />
          <el-table-column
            v-for="d in schedule.dates"
            :key="d"
            :label="formatDate(d)"
            align="center"
            min-width="100"
          >
            <template slot-scope="scope">
              <div
                v-if="scope.row.lessons.some((x) => x.date == d)"
                class="schedule-cell"
              >
                {{ scope.row.lessons.find((x) => x.date == d).subject.title }}
                {{ scope.row.lessons.find((x) => x.date == d).lesson_type }}
                {{ scope.row.lessons.find((x) => x.date == d).room }}
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "Schedule",
  data() {
    return {
      filter: {
        mg: "1809", // TODO change to null later
        dateRange: [
          moment().add(-3, "months").format("YYYY-MM-DD"),
          moment().format("YYYY-MM-DD"),
        ],
      },
      milgroups: [
        {
          milgroup: "1807",
          milfaculty: "ВКС",
        },
        {
          milgroup: "1808",
          milfaculty: "ВКС",
        },
        {
          milgroup: "1809",
          milfaculty: "ВКС",
        },
      ],
      schedule: {
        // FOR TESTS
        milgroup: {
          milgroup: 1809,
          milfaculty: "ВКС",
          weekday: 4,
        },
        dates: [
          "2021-01-1",
          "2021-01-8",
          "2021-01-15",
          "2021-01-22",
          "2021-01-29",
        ],
        ordinals: [
          {
            ordinal: 1,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 1,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 1,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 1,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 1,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 1,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 2,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 2,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 2,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 2,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 2,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 2,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 3,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 3,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 3,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 3,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 3,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 3,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 4,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 4,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 4,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 4,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 4,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 4,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 5,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 5,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 5,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 5,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 5,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 5,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 6,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 6,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 6,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 6,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 6,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 6,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 7,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 7,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 7,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 7,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 7,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 7,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 8,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 8,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 8,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 8,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 8,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 8,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 9,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 9,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 9,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 9,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 9,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 9,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
          {
            ordinal: 10,
            lessons: [
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-1",
                ordinal: 10,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ТП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-8",
                ordinal: 10,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-15",
                ordinal: 10,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-22",
                ordinal: 10,
                lesson_type: "Семинар",
                room: "510",
              },
              {
                id: 1,
                subject: {
                  id: 0,
                  title: "ВИП",
                  annotation: "",
                },
                milgroup: {
                  milgroup: 1809,
                  milfaculty: "ВКС",
                  weekday: 4,
                },
                date: "2021-01-29",
                ordinal: 10,
                lesson_type: "Семинар",
                room: "510",
              },
            ],
          },
        ],
      },
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    formatDate: (d) => moment(d).format("DD.MM.YY"),
    fetchData() {},
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
