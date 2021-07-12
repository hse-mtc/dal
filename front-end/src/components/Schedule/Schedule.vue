<template>
  <div>
    <el-col :offset="1" :span="22" class="Schedule">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-row class="filterRow" style="margin-bottom: 15px">
        <el-col :offset="17" :span="5">
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            align="right"
            unlink-panels
            :clearable="false"
            range-separator="по"
            start-placeholder="Начальная дата"
            end-placeholder="Конечная дата"
            :picker-options="pickerOptions"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
            @change="fetchData"
          />
        </el-col>
      </el-row>
      <el-tabs
        v-model="filter.mg"
        tab-position="left"
        class="my-tabs"
        @tab-click="fetchData()"
      >
        <el-tab-pane
          v-for="mg in milgroups"
          :key="mg.milgroup"
          :label="mg.milgroup"
          :name="mg.milgroup"
        >
          <PrimeTable
            :value="schedule.ordinals"
            scroll-height="730px"
            sort-field="ordinal"
            :sort-order="1"
            class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
          >
            <PrimeColumn
              header="№"
              field="ordinal"
              frozen
              column-key="ordinal"
              header-style="width: 50px; text-align: center;"
              body-style="width: 50px; text-align: center;"
            />
            <PrimeColumn
              v-for="d in schedule.dates"
              :key="d"
              :column-key="d"
              :header="formatDate(d)"
              min-width="250"
              header-style="text-align: center;"
              body-style="text-align: center;"
            >
              <template #body="{ data }">
                <div class="lesson-journal-cell">
                  <AZGuard
                    v-if="data.lessons.some((x) => x.date === d)"
                    v-slot="{ disabled }"
                    :permissions="[
                      ...getPermissions('patch'),
                      ...getPermissions('delete'),
                    ]"
                    disable
                    :tooltip="false"
                  >
                    <el-popover
                      :disabled="disabled"
                      placement="right"
                      trigger="hover"
                    >
                      <div class="text-center">
                        <AZGuard :permissions="getPermissions('patch')">
                          <el-button
                            size="mini"
                            icon="el-icon-edit"
                            type="info"
                            circle
                            @click="
                              onEdit(data.lessons.find((x) => x.date === d))
                            "
                          />
                        </AZGuard>
                        <AZGuard :permissions="getPermissions('delete')">
                          <el-button
                            size="mini"
                            icon="el-icon-delete"
                            type="danger"
                            circle
                            @click="
                              handleDelete(
                                data.lessons.find((x) => x.date === d).id,
                              )
                            "
                          />
                        </AZGuard>
                      </div>
                      <div slot="reference">
                        <div>
                          <svg-icon icon-class="notebook-outline" />
                          {{
                            data.lessons.find((x) => x.date === d).subject.title
                          }}
                        </div>

                        <div>
                          <svg-icon icon-class="map-marker-outline" />
                          {{ data.lessons.find((x) => x.date === d).room }}
                        </div>

                        <el-tag
                          :type="
                            tagByLessonType(
                              data.lessons.find((x) => x.date === d).type,
                            )
                          "
                          disable-transitions
                        >
                          {{
                            data.lessons.find((x) => x.date === d).type
                              | typeFilter
                          }}
                        </el-tag>
                      </div>
                    </el-popover>
                  </AZGuard>
                  <AZGuard v-else :permissions="getPermissions('post')">
                    <el-button
                      type="text"
                      icon="el-icon-plus"
                      class="create-lesson-btn"
                      @click="onCreate(data.ordinal, d)"
                    />
                  </AZGuard>
                </div>
              </template>
            </PrimeColumn>
          </PrimeTable>
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-dialog
      :title="editLessonFullname"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editLesson"
      >
        <el-form-item label="Дисциплина: " required>
          <el-select
            v-model="editLesson.subject"
            filterable
            value-key="id"
            placeholder="Выберите дисциплину"
            style="display: block"
          >
            <el-option
              v-for="item in subjects"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Аудитория: " required>
          <el-select
            v-model="editLesson.room"
            filterable
            placeholder="Выберите аудиторию"
            style="display: block"
          >
            <el-option
              v-for="item in rooms"
              :key="item.room"
              :label="item.room"
              :value="item.room"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Тип занятия: " required>
          <el-select
            v-model="editLesson.type"
            placeholder="Выберите тип занятия"
            style="display: block"
          >
            <el-option
              v-for="item in lessonTypes"
              :key="item.code"
              :label="item.label"
              :value="item.code"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Отмена</el-button>
        <el-button type="primary" @click="handleAccept()">Применить</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import moment from "moment";
import {
  getLessonJournal,
  patchLesson,
  postLesson,
  deleteLesson,
} from "@/api/lesson";
import { getSubjects } from "@/api/subjects-lms";
import {
  getError,
  postError,
  patchError,
  deleteError,
  postSuccess,
  patchSuccess,
  deleteSuccess,
} from "@/utils/message";
import { ReferenceModule, UserModule } from "@/store";

export default {
  name: "Schedule",
  filters: {
    typeFilter(value) {
      switch (value) {
        case "LE":
          return "Лекция";
        case "SE":
          return "Семинар";
        case "GR":
          return "Групповое занятие";
        case "PR":
          return "Практическое занятие";
        case "FI":
          return "Зачет";
        case "EX":
          return "Экзамен";
        default:
          return "Ошибка";
      }
    },
  },
  data() {
    return {
      dialogVisible: false,
      editLessonFullname: "",
      editLesson: {
        id: 0,
        subject: {
          id: 0,
          title: "",
        },
        milgroup: {
          milgroup: null,
          milfaculty: "",
        },
        date: "",
        ordinal: 0,
        type: "",
        room: "",
      },
      filter: {
        mg: null,
        dateRange: [
          moment().format("YYYY-MM-DD"),
          moment()
            .add(1, "months")
            .format("YYYY-MM-DD"),
        ],
      },
      lessonTypes: [
        { label: "Семинар", code: "SE" },
        { label: "Лекция", code: "LE" },
        { label: "Групповое занятие", code: "GR" },
        { label: "Практическое занятие", code: "PR" },
        { label: "Зачет", code: "FI" },
        { label: "Экзамен", code: "EX" },
      ],
      subjects: [],
      schedule: {},
      pickerOptions: {
        shortcuts: [
          {
            text: "Неделя",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              end.setTime(start.getTime() + 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "Месяц",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              end.setTime(start.getTime() + 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "3 месяца",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              end.setTime(start.getTime() + 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
    };
  },
  computed: {
    rooms() {
      return ReferenceModule.rooms;
    },
    milgroups() {
      return ReferenceModule.milgroups;
    },
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    userMilgroups() {
      return UserModule.personMilgroups;
    },
  },
  created() {
    this.filter.mg = this.milgroups[0].milgroup;
    this.fetchData();
  },
  methods: {
    getPermissions(method) {
      return [
        `lessons.${method}.all`,
        {
          codename: `lessons.${method}.milfaculty`,
          validator: () => this.userMilfaculty === this.schedule.milgroup.milfaculty,
        },
        {
          codename: `lessons.${method}.milgroup`,
          validator: () => this.userMilgroups.some(
            x => x === this.schedule.milgroup.milgroup,
          ),
        },
      ];
    },
    formatDate: d => moment(d).format("DD.MM.YY"),
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
    limitDateRange() {
      let main;
      let other;
      const maxMonths = 6;

      if (
        moment().diff(this.filter.dateRange[1])
        > moment().diff(this.filter.dateRange[0])
      ) {
        main = 1;
        other = 0;
      } else {
        main = 0;
        other = 1;
      }
      const diff = moment(this.filter.dateRange[main]).diff(
        this.filter.dateRange[other],
        "months",
        true,
      );
      if (Math.abs(diff) > maxMonths) {
        this.filter.dateRange[other] = moment(this.filter.dateRange[main])
          .add(Math.sign(diff) * maxMonths, "months")
          .format("YYYY-MM-DD");
      }
    },
    fetchData() {
      if (this.filter.mg > 0) {
        this.limitDateRange();
        getLessonJournal({
          milgroup: this.filter.mg,
          date_from: this.filter.dateRange[0],
          date_to: this.filter.dateRange[1],
        })
          .then(response => {
            this.schedule = response.data;
          })
          .catch(err => getError("расписания", err.response.status));
      }
    },
    getSubjects() {
      getSubjects()
        .then(response => {
          this.subjects = response.data;
        })
        .catch(err => getError("дисциплин", err.response.status));
    },

    onCreate(ordinal, date) {
      this.editLesson = {
        ordinal,
        date,
        milgroup: this.filter.mg,
      };
      this.editLessonFullname = "Новое занятие";
      this.getSubjects();
      this.dialogVisible = true;
    },
    onEdit(row) {
      this.editLesson = { ...row };
      this.editLesson.milgroup = this.editLesson.milgroup.milgroup;
      this.editLesson.subject = this.editLesson.subject.id;
      this.editLessonFullname = "Редактирование занятия";
      this.getSubjects();
      this.dialogVisible = true;
    },
    handleClose() {
      this.$confirm(
        "Вы уверены, что хотите закрыть окно редактирования?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      )
        .then(() => {
          this.dialogVisible = false;
        })
        .catch(() => {});
    },
    handleAccept() {
      if (this.editLesson.id) {
        patchLesson(this.editLesson)
          .then(() => {
            patchSuccess("занятия");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch(err => patchError("занятия", err.response.status));
      } else {
        postLesson(this.editLesson)
          .then(() => {
            postSuccess("занятия");
            this.dialogVisible = false;
            if (this.filter.mg) this.fetchData();
          })
          .catch(err => postError("занятия", err.response.status));
      }
    },
    handleDelete(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить занятие?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(() => {
        deleteLesson({ id })
          .then(() => {
            deleteSuccess("занятия");
            if (this.filter.mg > 0) this.fetchData();
          })
          .catch(err => deleteError("занятия", err.response.status));
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
