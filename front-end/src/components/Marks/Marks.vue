<template>
  <div>
    <el-col :offset="1" :span="22" class="Marks">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-row class="filterRow" style="margin-bottom: 15px" :gutter="20">
        <el-col :offset="6" :span="3">
          <!-- Marks history -->
          <el-button type="text" style="margin-left: 40px" @click="showMarksHistory">
            История изменения оценок
          </el-button>
          <el-dialog width="80%" :visible.sync="dialogHistoryVisible">
            <span slot="title" style="font-size: 16pt">История изменения оценок</span>
            <PrimeTable :value="historyMarksData" style="margin-top: -20px">
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
              >
                <template #body="{ data }">
                  <div class="mark-journal-cell" style="justify-content: left">
                    <el-tag
                      v-for="m in data.before"
                      :key="m"
                      effect="dark"
                      disable-transitions
                      class="margin-x"
                      :type="tagByMark(m)"
                    >
                      {{ m }}
                    </el-tag>
                  </div>
                </template>
              </PrimeColumn>
              <PrimeColumn
                header="Оценка после"
                :rowspan="2"
                :field="(row) => row.after"
                column-key="after"
              >
                <template #body="{ data }">
                  <div class="mark-journal-cell" style="justify-content: left">
                    <div>
                      <el-tag
                        v-for="m in data.after"
                        :key="m"
                        effect="dark"
                        disable-transitions
                        class="margin-x"
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
                :field="(row) => row.teacher_fullname"
                column-key="teacher"
              />
              <PrimeColumn
                header="Дата изменения"
                :rowspan="2"
                :field="(row) => formatDate(row.date)"
                column-key="date"
              />
            </PrimeTable>
          </el-dialog>
        </el-col>
        <el-col :offset="1" :span="6">
          <el-select
            v-model="filter.subject_id"
            filterable
            placeholder="Дисциплина"
            style="display: block"
            @change="fetchData({ resetSubjectsOrder: false })"
          >
            <el-option
              v-for="item in subjects"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            />
          </el-select>
        </el-col>
        <el-col :span="7">
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            align="right"
            unlink-panels
            :clearable="false"
            range-separator="по"
            start-placeholder="Начальная дата"
            end-placeholder="Конечная дата"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
            @change="fetchData({ resetSubjectsOrder: false })"
          />
        </el-col>
      </el-row>
      <el-tabs
        v-model="filter.mg"
        tab-position="left"
        class="my-tabs"
        @tab-click="fetchData({ resetSubjectsOrder: true })"
      >
        <el-tab-pane
          v-for="mg in milgroups"
          :key="mg.id"
          :label="mg.title"
          :name="mg.id.toString()"
        >
          <el-row>
            <el-col :span="22">
              <PrimeTable
                :value="journal.students"
                scroll-height="730"
                scrollable
                sort-field="ordinal"
                :sort-order="1"
                class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
              >
                <PrimeColumnGroup type="header">
                  <PrimeRow>
                    <PrimeColumn
                      header="ФИО"
                      :rowspan="2"
                      column-key="fullname-header"
                    />
                    <PrimeColumn
                      v-for="d in journal.dates"
                      :key="d"
                      :column-key="`${d}-header`"
                      :header="formatDate(d)"
                      header-style="text-align: center"
                      :colspan="
                        journal.lessons.filter((x) => x.date === d).length
                      "
                    />
                  </PrimeRow>

                  <PrimeRow>
                    <template v-for="d in journal.dates">
                      <PrimeColumn
                        v-for="item in journal.lessons.filter(
                          (x) => x.date === d,
                        )"
                        :key="`${item.id}-header`"
                      >
                        <template #header>
                          <el-popover placement="top" trigger="hover">
                            <div class="header-template">
                              <el-tag
                                :type="tagByLessonType(item.type)"
                                disable-transitions
                              >
                                {{ lessonTypeLabelFromValue(item.type) }}
                              </el-tag>
                              <span>
                                <svg-icon icon-class="map-marker-outline" />
                                {{ item.room.title }}
                              </span>
                              <div>
                                <AZGuard
                                  :permissions="
                                    getPermissions('patch', 'lessons')
                                  "
                                >
                                  <el-button
                                    size="mini"
                                    icon="el-icon-edit"
                                    type="info"
                                    circle
                                    @click="onEditLesson(item)"
                                  />
                                </AZGuard>
                                <AZGuard
                                  :permissions="
                                    getPermissions('delete', 'lessons')
                                  "
                                >
                                  <el-button
                                    size="mini"
                                    icon="el-icon-delete"
                                    type="danger"
                                    circle
                                    @click="handleDeleteLesson(item.id)"
                                  />
                                </AZGuard>
                              </div>
                            </div>
                            <div slot="reference" class="header-template">
                              <span> {{ item.ordinal }} пара </span>
                            </div>
                          </el-popover>
                        </template>
                      </PrimeColumn>
                    </template>
                  </PrimeRow>
                </PrimeColumnGroup>

                <PrimeColumn
                  header="ФИО"
                  field="fullname"
                  width="250"
                  column-key="fullname"
                />
                <template v-for="d in journal.dates">
                  <PrimeColumn
                    v-for="item in journal.lessons.filter((x) => x.date === d)"
                    :key="item.id"
                  >
                    <template #body="{ data }">
                      <div class="mark-journal-cell">
                        <div
                          v-for="m in getMarksByLesson(data.marks, item.id)"
                          :key="m"
                        >
                          <el-tag
                            :type="tagByMark(m)"
                            effect="dark"
                            disable-transitions
                            class="margin-x"
                            :class="{
                              'is-clickable': hasPermission(
                                getPermissions('patch', 'marks'),
                              ),
                            }"
                            @click="
                              hasPermission(getPermissions('patch', 'marks'))
                                ? onEdit(
                                  data.marks.find(
                                    (x) => x.lesson === item.id,
                                  ),
                                  data,
                                )
                                : null
                            "
                          >
                            {{ m }}
                          </el-tag>
                        </div>
                        <AZGuard
                          :permissions="
                            data.marks.some((x) => x.lesson === item.id)
                              ? getPermissions('put', 'marks')
                              : getPermissions('post', 'marks')
                          "
                        >
                          <el-button
                            type="text"
                            icon="el-icon-plus"
                            class="create-mark-btn"
                            @click="
                              onCreate(
                                data,
                                item,
                                data.marks.find((x) => x.lesson === item.id),
                              )
                            "
                          />
                        </AZGuard>
                      </div>
                    </template>
                  </PrimeColumn>
                </template>
              </PrimeTable>
            </el-col>
            <AZGuard :permissions="getPermissions('post', 'lessons')">
              <el-col :span="2" class="new-lesson-col">
                <el-button
                  type="primary"
                  icon="el-icon-plus"
                  circle
                  @click="onCreateLesson()"
                />
              </el-col>
            </AZGuard>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-dialog
      :title="editMarkFullname"
      :visible.sync="dialogVisible"
      width="20%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="100px"
        size="mini"
        :model="editMark"
      >
        <el-form-item label="Оценка: " required>
          <el-input-number
            v-model="editMark.value"
            controls-position="right"
            :min="2"
            :max="5"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <AZGuard :permissions="getPermissions('delete', 'marks')">
          <el-button
            v-if="editMarkId"
            type="danger"
            @click="handleDelete(editMarkId)"
          >
            Удалить
          </el-button>
        </AZGuard>
        <el-button type="primary" @click="handleAccept()">Применить</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="editLessonFullname"
      :visible.sync="lessonDialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editLesson"
      >
        <el-form-item label="Дата: " required>
          <el-date-picker
            v-model="editLesson.date"
            type="date"
            placeholder="Выберите дату"
            style="width: 100%"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
            :picker-options="{ firstDayOfWeek: 1 }"
          />
        </el-form-item>
        <el-form-item label="Номер занятия: " required>
          <el-input-number
            v-model="editLesson.ordinal"
            size="mini"
            controls-position="right"
            :min="1"
            :max="10"
            style="width: 100%"
          />
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
              :key="item.id"
              :label="item.title"
              :value="item.id"
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
              v-for="type in lessonTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="lessonDialogVisible = false">Отмена</el-button>
        <el-button type="primary" @click="handleAcceptLesson()">
          Применить
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import moment from "moment";
import {
  getMarkJournal,
  patchMark,
  postMark,
  putMark,
  deleteMark,
  getMark,
  getMarkHistory,
} from "@/api/mark";
import { getSubjects } from "@/api/subjects-lms";
import { postLesson, patchLesson, deleteLesson } from "@/api/lesson";
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
import { hasPermission } from "@/utils/permissions";
import { LessonTypesMixin } from "@/mixins/lessons";

export default {
  name: "Marks",
  mixins: [LessonTypesMixin],
  data() {
    return {
      dialogHistoryVisible: false,
      lessonDialogVisible: false,
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
      drawer: false,
      drawerTitle: "",
      dialogVisible: false,
      editMarkFullname: "",
      editMark: {
        id: 0,
        student: {},
        lesson: {
          id: 0,
          title: "",
        },
        mark: 0,
      },
      editMarkId: 0,
      editMarkMethod: "POST",
      filter: {
        subject_id: 0,
        mg: 0,
        dateRange: [
          moment()
            .add(-3, "months")
            .format("YYYY-MM-DD"),
          moment().format("YYYY-MM-DD"),
        ],
      },
      subjects: [],
      journal: {},
      pickerOptions: {
        firstDayOfWeek: 1,
        shortcuts: [
          {
            text: "Неделя",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "Месяц",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "3 месяца",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
      historyMarksData: [],
    };
  },

  computed: {
    rooms() {
      return ReferenceModule.rooms;
    },
    milgroups() {
      if (!UserModule.isSuperuser) {
        return ReferenceModule.milgroups.filter(milgroup => UserModule.personMilgroups.indexOf(milgroup.id) > -1);
      }
      return ReferenceModule.milgroups;
    },
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    userMilgroups() {
      return UserModule.personMilgroups;
    },
  },

  watch: {
    milgroups(newValue) {
      if (localStorage.milgroupUpdate) {
        this.filter.mg = localStorage.milgroupUpdate;
        this.filter.subject_id = parseInt(localStorage.subjectUpdate, 10);
        this.fetchData({ resetSubjectsOrder: false });
      } else {
        this.filter.mg = this.milgroups[0]?.id.toString();
        this.fetchData({ resetSubjectsOrder: true });
      }
      if (localStorage.dataRange0) {
        this.filter.dateRange[0] = localStorage.dataRange0;
        this.filter.dateRange[1] = localStorage.dataRange1;
      }
    },
  },

  async created() {
    if (localStorage.milgroupUpdate) {
      this.filter.mg = localStorage.milgroupUpdate;
      this.filter.subject_id = parseInt(localStorage.subjectUpdate, 10);
      this.fetchData({ resetSubjectsOrder: false });
    } else {
      this.filter.mg = this.milgroups[0]?.id.toString();
      if (this.filter.mg !== undefined) {
        await this.fetchData({ resetSubjectsOrder: true });
      }
    }
    if (localStorage.dataRange0) {
      this.filter.dateRange[0] = localStorage.dataRange0;
      this.filter.dateRange[1] = localStorage.dataRange1;
    }
    await this.getSubjects();
    this.filter.subject_id = this.subjects[0].id;
  },

  methods: {
    hasPermission,
    getPermissions(method, entity) {
      return [
        `${entity}.${method}.all`,
        {
          codename: `${entity}.${method}.milfaculty`,
          validator: () => this.userMilfaculty === this.journal.milgroup.milfaculty,
        },
        {
          codename: `${entity}.${method}.milgroup`,
          validator: () => this.userMilgroups.some(x => x === this.journal.milgroup.id),
        },
      ];
    },
    getMarksByLesson(marks, lessonId) {
      const m = marks.find(x => x.lesson === lessonId);
      if (m) {
        return m.values;
      }
      return [];
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
    async fetchData(options) {
      await this.getSubjects();
      if (options.resetSubjectsOrder) {
        this.filter.subject_id = this.subjects[0].id;
      }
      if (typeof this.filter.subject_id === "string") {
        this.filter.subject_id = this.subjects.filter(subject => subject.title === this.filter.subject_id)[0].id;
      }
      if (this.filter.mg > 0 && this.filter.subject_id > 0) {
        getMarkJournal({
          milgroup: this.filter.mg,
          subject: this.filter.subject_id,
          date_from: this.filter.dateRange[0],
          date_to: this.filter.dateRange[1],
        })
          .then(response => {
            this.journal = response.data;
          })
          .catch(err => getError("оценок", err.response.status));
      }
      localStorage.milgroupUpdate = this.filter.mg;
      localStorage.subjectUpdate = parseInt(this.filter.subject_id, 10);
      // eslint-disable-next-line prefer-destructuring
      localStorage.dataRange0 = this.filter.dateRange[0];
      // eslint-disable-next-line prefer-destructuring
      localStorage.dataRange1 = this.filter.dateRange[1];
    },
    async getSubjects() {
      try {
        const response = await getSubjects();
        // eslint-disable-next-line max-len
        const milspecialty = this.milgroups.filter(milgroup => milgroup.id === parseInt(this.filter.mg, 10))[0].milspecialty.id;
        // eslint-disable-next-line max-len
        this.subjects = response.data.filter(subject => subject.milspecialty === milspecialty);
      } catch (err) {
        getError("дисциплин", err.response.status);
      }
    },

    onCreate(student, lesson, mark) {
      if (student.marks.some(x => x.lesson === lesson.id)) {
        this.editMarkMethod = "PUT";
        this.editMarkId = mark.id;
        this.editMark = {
          value: 5,
        };
      } else {
        this.editMarkMethod = "POST";
        this.editMarkId = null;
        this.editMark = {
          student: student.id,
          lesson: lesson.id,
          value: 5,
        };
      }
      this.editMarkFullname = student.fullname;
      this.dialogVisible = true;
    },
    onEdit(mark, student) {
      this.editMarkMethod = "PATCH";
      this.editMark = {
        value: mark.values[mark.values.length - 1],
      };
      this.editMarkId = mark.id;
      this.editMarkFullname = student.fullname;
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
          this.lessonDialogVisible = false;
        });
    },
    handleAccept() {
      if (this.editMarkMethod === "PATCH") {
        patchMark(this.editMark, this.editMarkId)
          .then(() => {
            patchSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) { this.fetchData({ resetSubjectsOrder: false }); }
          })
          .catch(err => patchError("оценки", err.response.status));
      } else if (this.editMarkMethod === "POST") {
        postMark(this.editMark)
          .then(() => {
            postSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) { this.fetchData({ resetSubjectsOrder: false }); }
          })
          .catch(err => postError("оценки", err.response.status));
      } else if (this.editMarkMethod === "PUT") {
        putMark(this.editMark, this.editMarkId)
          .then(() => {
            patchSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) { this.fetchData({ resetSubjectsOrder: false }); }
          })
          .catch(err => patchError("оценки", err.response.status));
      }
    },
    handleDelete(id) {
      this.$confirm("Вы уверены, что хотите удалить оценку?", "Подтверждение", {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      }).then(() => {
        deleteMark({ id })
          .then(() => {
            deleteSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg > 0) { this.fetchData({ resetSubjectsOrder: false }); }
          })
          .catch(err => deleteError("оценки", err.response.status));
      });
    },
    onCreateLesson() {
      this.editLesson = {
        milgroup: this.filter.mg,
        subject: this.filter.subject_id,
        ordinal: 1,
        date: moment().format("YYYY-MM-DD"),
      };
      this.editLessonFullname = "Новое занятие";
      this.lessonDialogVisible = true;
    },
    onEditLesson(row) {
      this.editLesson = { ...row };
      this.editLesson.milgroup = this.editLesson.milgroup.id;
      this.editLesson.subject = this.editLesson.subject.id;
      this.editLessonFullname = "Редактирование занятия";
      this.editLesson.room = this.journal.lessons[0].room.title;
      this.lessonDialogVisible = true;
    },
    handleAcceptLesson() {
      if (typeof this.editLesson.room === "string") {
        this.editLesson.room = this.journal.lessons[0].room.id;
      }

      if (this.editLesson.id) {
        patchLesson(this.editLesson)
          .then(() => {
            patchSuccess("занятия");
            this.lessonDialogVisible = false;
            if (this.filter.mg) {
              this.fetchData({ resetSubjectsOrder: false });
              localStorage.milgroupUpdate = this.filter.mg;
              localStorage.subjectUpdate = this.filter.subject_id;
              window.location.reload();
            }
          })
          .catch(err => patchError("занятия", err.response.status));
      } else {
        postLesson(this.editLesson)
          .then(() => {
            postSuccess("занятия");
            this.lessonDialogVisible = false;
            if (this.filter.mg) {
              this.fetchData({ resetSubjectsOrder: false });
              localStorage.milgroupUpdate = this.filter.mg;
              localStorage.subjectUpdate = this.filter.subject_id;
              window.location.reload();
            }
          })
          .catch(err => postError("занятия", err.response.status));
      }
    },
    handleDeleteLesson(id) {
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
            if (this.filter.mg > 0) { this.fetchData({ resetSubjectsOrder: false }); }
          })
          .catch(err => deleteError("занятия", err.response.status));
      });
    },
    openDrawer() {
      this.drawer = true;
      // fetch data
    },
    showMarksHistory() {
      this.dialogHistoryVisible = true;
      getMarkHistory({
        milgroup: this.filter.mg,
        subject: this.filter.subject_id,
        date_from: this.filter.dateRange[0],
        date_to: this.filter.dateRange[1],
        history: true,
      })
        .then(response => {
          const historymark = response.data;
          this.historyMarksData = historymark;
        })
        .catch(err => getError("оценок", err.response.status));
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
