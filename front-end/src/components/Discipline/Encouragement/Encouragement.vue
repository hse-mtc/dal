<template>
  <div>
    <el-row class="filterRow" :gutter="20">
      <el-col :span="8">
        <el-date-picker
          v-model="filter.dateRange"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="по"
          start-placeholder="Начальная дата"
          end-placeholder="Конечная дата"
          :picker-options="pickerOptions"
          format="dd.MM.yyyy"
          value-format="yyyy-MM-dd"
          style="width: auto"
          @change="onFilter"
          @clear="onFilter"
        />
      </el-col>
      <el-col :span="5">
        <el-input
          v-model="filter.search"
          clearable
          placeholder="Поиск..."
          @clear="onFilter"
          @keyup.native.enter="onFilter"
        />
      </el-col>
      <el-col :span="5">
        <el-select
          v-model="filter.mg"
          value-key="id"
          clearable
          placeholder="Выберите взвод"
          style="display: block"
          @change="onFilter"
        >
          <el-option
            v-for="item in milgroups"
            :key="item.id"
            :label="item.title"
            :value="item"
          >
            <span style="float: left">{{ item.title }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{
              item.milfaculty.abbreviation
            }}</span>
          </el-option>
        </el-select>
      </el-col>
      <el-col :span="6">
        <el-select
          v-model="filter.type"
          clearable
          placeholder="Выберите тип поощрения"
          style="display: block"
          @change="onFilter"
        >
          <el-option
            v-for="type in encouragementTypes"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          />
        </el-select>
      </el-col>
    </el-row>
    <AZGuard
      :permissions="[
        'encouragements.post.all',
        'encouragements.post.milfaculty',
        'encouragements.post.milgroup',
        'encouragements.post.self',
      ]"
    >
      <el-row class="addRow">
        <el-col :span="24">
          <el-button
            class="addBtn"
            type="primary"
            icon="el-icon-plus"
            @click="onCreate"
          >
            Новое поощрение
          </el-button>
        </el-col>
      </el-row>
    </AZGuard>
    <el-row>
      <PrimeTable
        :value="encouragements"
        :sort-field="dateField"
        :sort-order="-1"
        scrollable
        scroll-height="680px"
        class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
      >
        <PrimeColumn
          sortable
          header="Дата"
          header-style="width: 100px"
          body-style="width: 100px"
          :field="dateField"
          column-key="date"
        />
        <PrimeColumn
          :field="(row) => row.student.fullname"
          column-key="student.fullname"
          sortable
          header="Студент"
        />
        <PrimeColumn
          :field="(row) => row.teacher.fullname"
          sortable
          header="Преподаватель"
          column-key="teacher.fullname"
        />
        <PrimeColumn
          :field="(row) => row.student.milgroup.title"
          column-key="milgroup"
          sortable
          header="Взвод"
          header-style="width: 100px"
          body-style="width: 100px"
        />
        <PrimeColumn header="Тип поощрения" column-key="type">
          <template #body="{ data }">
            <el-tag
              :type="tagByEncouragementType(data.type)"
              disable-transitions
            >
              {{ encouragementTypeLabelFromValue(data.type) }}
            </el-tag>
          </template>
        </PrimeColumn>
        <PrimeColumn field="reason" header="Причина" />
        <PrimeColumn
          header-style="width: 120px"
          body-style="width: 120px; text-align: center;"
          column-key="buttons"
        >
          <template #body="{ data }">
            <AZGuard
              v-slot="{ disabled }"
              :permissions="getPermissions('patch', data)"
              disable
            >
              <el-button
                size="mini"
                icon="el-icon-edit"
                type="info"
                circle
                :disabled="disabled"
                @click="onEdit(data)"
              />
            </AZGuard>
            <AZGuard
              v-slot="{ disabled }"
              :permissions="getPermissions('delete', data)"
              disable
            >
              <el-button
                size="mini"
                icon="el-icon-delete"
                type="danger"
                circle
                :disabled="disabled"
                @click="handleDelete(data.id)"
              />
            </AZGuard>
          </template>
        </PrimeColumn>
      </PrimeTable>
    </el-row>
    <el-dialog
      :title="editEncouragementFullname"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        label-position="right"
        label-width="150px"
        size="mini"
        :model="editEncouragement"
      >
        <el-form-item label="Дата" required>
          <el-date-picker
            v-model="editEncouragement.date"
            type="date"
            placeholder="Выберите дату"
            style="width: 100%"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item
          v-if="!(editEncouragement.id && editEncouragement.id > 0)"
          label="Студент"
          required
        >
          <el-select
            v-model="editEncouragement.student"
            value-key="id"
            placeholder="Выберите студента"
            filterable
            style="display: block"
          >
            <el-option
              v-for="st in students"
              :key="st.id"
              :label="st.fullname"
              :value="st.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Преподаватель" required>
          <AZGuard
            v-slot="{ disabled }"
            :permissions="[
              `punishments.${
                editEncouragement.id && editEncouragement.id > 0 ? 'patch' : 'post'
              }.all`,
              `punishments.${
                editEncouragement.id && editEncouragement.id > 0 ? 'patch' : 'post'
              }.milfaculty`,
            ]"
            disable
          >
            <el-select
              v-model="editEncouragement.teacher"
              value-key="id"
              placeholder="Выберите преподавателя"
              filterable
              style="display: block"
              :disabled="disabled"
            >
              <el-option
                v-for="t in teachers"
                :key="t.id"
                :label="t.fullname"
                :value="t.id"
              />
            </el-select>
          </AZGuard>
        </el-form-item>
        <el-form-item label="Тип поощрения: " required>
          <el-select
            v-model="editEncouragement.type"
            placeholder="Выберите тип поощрения"
            style="display: block"
          >
            <el-option
              v-for="type in encouragementTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Причина: " required>
          <el-input
            v-model="editEncouragement.reason"
            placeholder="Введите причину"
          />
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
import {
  getEncouragement,
  deleteEncouragement,
  patchEncouragement,
  postEncouragement,
} from "@/api/encouragement";
import {
  getError,
  postError,
  patchError,
  deleteError,
  postSuccess,
  patchSuccess,
  deleteSuccess,
} from "@/utils/message";
import { UserModule, ReferenceModule } from "@/store";

import moment from "moment";
import { getStudent, findStudent } from "@/api/students";
import { getTeacher, findTeacher } from "@/api/teachers";
import { getDisciplinePersonsFilters } from "@/utils/permissions";
import { EncouragementTypesMixin } from "@/mixins/encouragements";

export default {
  name: "Encouragement",
  mixins: [EncouragementTypesMixin],
  data() {
    return {
      editEncouragement: {
        id: 0,
        date: "",
        type: "",
        reason: "",
        student: 0,
        teacher: 0,
      },
      editEncouragementFullname: null,
      dialogVisible: false,
      encouragements: [],
      filter: {
        search: null,
        mg: null,
        dateRange: ["", ""],
        type: null,
      },
      students: [],
      teachers: [],
      pickerOptions: {
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
    };
  },
  computed: {
    milgroups() {
      return ReferenceModule.milgroups;
    },
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    userMilgroups() {
      return UserModule.personMilgroups;
    },
    userId() {
      return UserModule.personId;
    },
    usersPermissions() {
      return UserModule.permissions;
    },
    studentsFilter() {
      if (
        this.usersPermissions.some(
          x => x.codename === "encouragements.post.milfaculty"
            || x.codename === "encouragements.post.self",
        )
      ) {
        return {
          milfaculty: this.userMilfaculty,
        };
      }
      return {};
    },
  },
  created() {
    this.onFilter();
  },
  methods: {
    getPermissions(method, data) {
      return [
        `encouragements.${method}.all`,
        {
          codename: `encouragements.${method}.milfaculty`,
          validator: () => this.userMilfaculty === data.student.milgroup.milfaculty.id,
        },
        {
          codename: `encouragements.${method}.milgroup`,
          validator: () => this.userMilgroups.some(
            x => x === data.student.milgroup.id,
          ),
        },
        {
          codename: `encouragements.${method}.self`,
          validator: () => this.userId === data.teacher.id,
        },
      ];
    },
    dateField: row => moment(row.date).format("DD.MM.YY"),
    onFilter() {
      getEncouragement({
        date_from:
          this.filter.dateRange !== null ? this.filter.dateRange[0] : null,
        date_to:
          this.filter.dateRange !== null ? this.filter.dateRange[1] : null,
        type: this.filter.type,
        search: this.filter.search,
        milgroup: this.filter.mg?.id,
      })
        .then(response => {
          this.encouragements = response.data;
        })
        .catch(err => getError("поощрений", err.response.status));
    },
    // TODO(TmLev): Send this info from back-end in "choices/.../" views.
    tagByEncouragementType(type) {
      switch (type) {
        case "EN":
          return "";
        case "RE":
          return "success";
        default:
          return "";
      }
    },
    async onCreate() {
      this.editEncouragementFullname = "Новое поощрение";
      const { students, teachers } = getDisciplinePersonsFilters(
        "encouragements",
        "post",
      );
      this.students = students?.id
        ? [(await findStudent(students.id)).data]
        : (await getStudent(students)).data;
      this.teachers = teachers?.id
        ? [(await findTeacher(teachers.id)).data]
        : (await getTeacher(teachers)).data;
      this.editEncouragement = {
        student: null,
        teacher: this.teachers.find(x => x.id === this.userId)?.id,
        date: moment().format("YYYY-MM-DD"),
      };
      this.dialogVisible = true;
    },
    async onEdit(row) {
      this.editEncouragement = {
        ...row,
        student: row.student.id,
        teacher: row.teacher.id,
      };
      const { students, teachers } = getDisciplinePersonsFilters(
        "encouragements",
        "patch",
      );
      this.students = students?.id
        ? (await findStudent(students.id)).data
        : (await getStudent(students)).data;
      this.teachers = teachers?.id
        ? (await findTeacher(teachers.id)).data
        : (await getTeacher(teachers)).data;
      this.editEncouragementFullname = row.student.fullname;
      this.dialogVisible = true;
    },
    handleDelete(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить поощрение?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(() => {
        deleteEncouragement({ id })
          .then(() => {
            deleteSuccess("поощрения");
            this.onFilter();
          })
          .catch(err => deleteError("поощрения", err.response.status));
      });
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
      if (this.editEncouragement.id && this.editEncouragement.id > 0) {
        patchEncouragement(this.editEncouragement)
          .then(() => {
            patchSuccess("занятия");
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch(err => patchError("поощрения", err.response.status));
      } else {
        postEncouragement(this.editEncouragement)
          .then(() => {
            postSuccess("поощрения");
            this.dialogVisible = false;
            this.onFilter();
          })
          .catch(err => postError("поощрения", err.response.status));
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
