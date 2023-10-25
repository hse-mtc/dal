<template>
  <div>
    <MarksHistory
      :mg="parseInt(filter.mg)"
      :subject-id="parseInt(filter.subject_id)"
      :date-range="filter.dateRange"
      :subject-name="getSubjectTitle(filter.subject_id)"
      :visible="dialogHistoryVisible"
      @close="dialogHistoryVisible = false"
    />
    {{ filter.dateRange }}
    {{ selectedMilgroup }}
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
        </el-col>
        <el-col :offset="1" :span="6">
          <el-select
            v-model="filter.subject_id"
            filterable
            placeholder="Дисциплина"
            style="display: block"
          >
            <el-option
              v-for="item in selectableSubjects"
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
            :picker-options="datePickerOptions"
          />
        </el-col>
      </el-row>
      <el-tabs
        v-model="filter.mg"
        tab-position="left"
        class="my-tabs"
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
                            class="margin-all"
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
            :picker-options="datePickerOptions"
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
  deleteMark, getMarkJournal, patchMark, postMark, putMark,
} from "@/api/mark";
import { getSubjects } from "@/api/subjects-lms";
import { deleteLesson, patchLesson, postLesson } from "@/api/lesson";
import {
  deleteError, deleteSuccess, getError, patchError, patchSuccess, postError, postSuccess,
} from "@/utils/message";
import { ReferenceModule, UserModule } from "@/store";
import { hasPermission } from "@/utils/permissions";
import { LessonTypesMixin } from "@/mixins/lessons";
import MarksHistory from "@/components/Marks/MarksHistory.vue";

export default {
  name: "Marks",
  components: {
    MarksHistory,
  },
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
      allSubjects: [],
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
    selectedMilgroup() {
      const selectedMilgroupId = parseInt(this.filter.mg, 10);
      return this.milgroups.filter(
        milgroup => milgroup.id === selectedMilgroupId,
      )[0];
    },
    selectableSubjects() {
      if (!this.milgroups || this.milgroups.length === 0) {
        return [];
      }
      const selectedMilgroupMilspecId = this.selectedMilgroup?.milspecialty?.id;
      return this.allSubjects.filter(subject => subject.milspecialty === selectedMilgroupMilspecId);
    },
    filterKey() {
      return `${this.filter.mg}-${this.filter.subject_id}-${this.filter.dateRange[0]}-${this.filter.dateRange[1]}`;
    },
    datePickerOptions() {
      return {
        firstDayOfWeek: 1,
        disabledDate: this.dateDisabled,
      };
    },
  },

  watch: {
    milgroups(newValue) {
      console.log("Milgroups updated to value", JSON.stringify(newValue));
      if (!localStorage.journalMilgroupSelected) {
        // Only once, after ReferenceBook loaded
        // and value is not stored in localStorage
        this.filter.mg = this.milgroups[0].id.toString();
      }
    },
    "filter.mg": function(newValue) {
      console.log("Filter MG updated to value", JSON.stringify(newValue));
      // Every time when another milgroup selected
      // Assert this applies before filterKey change; otherwise there are one unused query!
      if (
        this.selectableSubjects.length > 0
        && !this.selectableSubjects.find(subject => subject.id === this.filter.subject_id)) {
        this.filter.subject_id = this.selectableSubjects[0].id;
      }
    },
    filterKey(newValue) {
      console.log("Filter key updated to value", JSON.stringify(newValue));
      // Every time some filter value is changed
      this.setFiltersToLocalStorage();
      this.fetchData();
    },
  },

  async created() {
    await this.getSubjects();
    this.getFiltersFromLocalStorage();
  },

  methods: {
    hasPermission,
    getPermissions(method, entity) {
      return [
        `${entity}.${method}.all`,
        {
          codename: `${entity}.${method}.milfaculty`,
          validator: () => this.userMilfaculty === this.journal?.milgroup?.milfaculty,
        },
        {
          codename: `${entity}.${method}.milgroup`,
          validator: () => this.userMilgroups.some(x => x === this.journal?.milgroup?.id),
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
    getSubjectTitle(subjectId) {
      if (!this.allSubjects || this.allSubjects.length === 0) {
        return "";
      }
      return this.allSubjects.filter(item => item.id === subjectId)[0]?.title || "";
    },
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
    async fetchData(options) {
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
    },
    async getSubjects() {
      try {
        this.allSubjects = (await getSubjects()).data;
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
            if (this.filter.mg) { this.fetchData(); } // todo
          })
          .catch(err => patchError("оценки", err.response.status));
      } else if (this.editMarkMethod === "POST") {
        postMark(this.editMark)
          .then(() => {
            postSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) { this.fetchData(); } // todo
          })
          .catch(err => postError("оценки", err.response.status));
      } else if (this.editMarkMethod === "PUT") {
        putMark(this.editMark, this.editMarkId)
          .then(() => {
            patchSuccess("оценки");
            this.dialogVisible = false;
            if (this.filter.mg) { this.fetchData(); } // todo
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
            if (this.filter.mg > 0) { this.fetchData(); } // todo
          })
          .catch(err => deleteError("оценки", err.response.status));
      });
    },
    onCreateLesson() {
      this.editLesson = {
        milgroup: this.filter.mg,
        subject: this.filter.subject_id,
        ordinal: 1,
        date: this.nextMilitaryDay(),
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
              this.fetchData(); // todo
              this.setFiltersToLocalStorage();
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
              this.fetchData(); // todo
              this.setFiltersToLocalStorage();
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
            if (this.filter.mg > 0) { this.fetchData(); } // todo
          })
          .catch(err => deleteError("занятия", err.response.status));
      });
    },
    openDrawer() {
      this.drawer = true;
      // fetch data
    },
    getFiltersFromLocalStorage() {
      if (!localStorage.journalMilgroupSelected) {
        return;
      }
      this.filter.mg = localStorage.journalMilgroupSelected;

      if (!localStorage.journalSubjectSelected) {
        return;
      }
      this.filter.subject_id = parseInt(localStorage.journalSubjectSelected, 10);

      if (!localStorage.dataRange0Selected || !localStorage.dataRange1Selected) {
        return;
      }
      this.filter.dateRange = ["", ""];
      this.filter.dateRange[0] = localStorage.dataRange0Selected;
      this.filter.dateRange[1] = localStorage.dataRange1Selected;
    },
    setFiltersToLocalStorage() {
      if (!this.filter.mg) {
        return;
      }
      localStorage.journalMilgroupSelected = this.filter.mg;
      if (!this.filter.subject_id) {
        return;
      }
      localStorage.journalSubjectSelected = this.filter.subject_id.toString();
      [localStorage.dataRange0Selected, localStorage.dataRange1Selected] = this.filter.dateRange;
    },
    showMarksHistory() {
      this.dialogHistoryVisible = true;
    },
    dateDisabled(date) {
      return date.getDay() !== (this.selectedMilgroup.weekday + 1) % 7;
    },
    nextMilitaryDay() {
      const now = moment();
      const daysToMilDate = (this.selectedMilgroup.weekday + 7 - now.weekday()) % 7;
      return now.add(daysToMilDate, "days").format("YYYY-MM-DD");
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
