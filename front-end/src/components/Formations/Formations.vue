<template>
  <div v-loading="loading" class="formations">
    <header class="formation-page-heading">
      <div>
        <div class="formation-eyebrow">
          {{ isHead ? "Учёт личного состава" : "Сведения взвода" }}
        </div>
        <h1>{{ isHead ? "Построения" : "Численность на построении" }}</h1>
        <p class="formation-muted">
          {{ isHead ? "Сведения взводов и замечания с построения" : "Заполните сведения о своём взводе" }}
        </p>
      </div>
      <el-date-picker
        v-model="date"
        type="date"
        format="dd.MM.yyyy"
        value-format="yyyy-MM-dd"
        :clearable="false"
        :editable="false"
        :disabled="busy"
        placeholder="Дата построения"
        @change="loadReports"
      />
    </header>

    <div v-if="loadError" class="formation-empty" role="alert">
      <strong>{{ loadError }}</strong>
      <el-button @click="initialize">
        Повторить загрузку
      </el-button>
    </div>
    <template v-else>
      <section v-if="isHead" class="formation-summary" aria-label="Сводка по поданным сведениям">
        <div>
          <strong>{{ filledCount ? totals.present_count : "—" }}</strong>
          <span class="formation-muted">в строю<span v-if="filledCount"> из {{ totals.roster_count }}</span></span>
        </div>
        <div>
          <strong>{{ filledCount ? totals.absent_count : "—" }}</strong>
          <span class="formation-muted">отсутствуют</span>
        </div>
        <span v-if="!isHistoricalDate && filledCount < groups.length" class="formation-status">Неполный итог</span>
        <div class="formation-coverage">
          <div class="formation-panel-heading">
            <span class="formation-muted">{{ isHistoricalDate ? "Сохранено отчётов" : "Сведения поданы" }}</span>
            <b>{{ filledCount }}<template v-if="!isHistoricalDate"> / {{ groups.length }}</template></b>
          </div>
          <div v-if="!isHistoricalDate" class="formation-progress" aria-hidden="true">
            <span :style="{ width: `${groups.length ? filledCount / groups.length * 100 : 0}%` }" />
          </div>
        </div>
      </section>

      <div v-if="!groups.length && !loading" class="formation-empty">
        <i class="el-icon-user" aria-hidden="true" />
        <strong>Нет доступных взводов</strong>
        <p>Здесь появятся сведения взводов, к которым у вас есть доступ.</p>
      </div>

      <div v-else class="formation-workbench" :class="{ commander: !isHead }">
        <aside v-if="isHead" class="formation-platoons" aria-label="Выбор взвода">
          <div class="formation-rail-heading">
            <span>{{ isHistoricalDate ? "СОХРАНЁННЫЕ ОТЧЁТЫ" : "ВЗВОДЫ" }}</span>
            <span>{{ summaryRows.length }}</span>
          </div>
          <div class="formation-platoon-list">
            <button
              v-for="row in summaryRows"
              :key="row.id"
              type="button"
              class="formation-platoon"
              :aria-pressed="selectedGroupId === row.id"
              :disabled="busy"
              @click="chooseGroup(row.id)"
            >
              <span class="formation-platoon-title">
                <strong>{{ row.title }}</strong>
                <span v-if="row.report" class="formation-muted">
                  {{ row.report.present_count }}/{{ row.report.roster_count }}
                </span>
              </span>
              <span class="formation-platoon-state" :class="{ submitted: row.report }">
                {{ row.report ? "Сведения поданы" : "Нет сведений" }}
              </span>
            </button>
          </div>
          <p v-if="isHistoricalDate && !summaryRows.length" class="formation-muted">
            За эту дату сведений пока нет.
          </p>
          <el-select
            v-if="isHistoricalDate"
            :value="selectedGroupId"
            class="formation-other-group"
            :disabled="busy"
            filterable
            placeholder="Выберите взвод"
            aria-label="Взвод для ввода за прошлую дату"
            @change="chooseGroup"
          >
            <el-option
              v-for="group in groups"
              :key="group.id"
              :value="group.id"
              :label="group.title"
            />
          </el-select>
        </aside>

        <div class="formation-content">
          <el-select
            v-if="!isHead && groups.length > 1"
            :value="selectedGroupId"
            class="formation-group-picker"
            :disabled="busy"
            aria-label="Выберите взвод"
            @change="chooseGroup"
          >
            <el-option
              v-for="group in groups"
              :key="group.id"
              :value="group.id"
              :label="group.title"
            />
          </el-select>
          <div
            v-if="selectedGroup && form"
            class="formation-detail-grid"
            :class="{ 'without-remarks': !canViewRemarks }"
          >
            <FormationHeadcount
              :key="contextKey"
              :value="form"
              :group="selectedGroup"
              :report="report"
              :date="date"
              :wizard="!isHead"
              :saving="saving"
              :disabled="savingRemark || !canEditReport"
              @input="setForm"
              @save="saveReport"
            />
            <FormationRemarks
              v-if="canViewRemarks"
              :key="`remarks-${contextKey}`"
              ref="remarks"
              :report="report"
              :categories="categories"
              :students="students"
              :students-loading="studentsLoading"
              :busy="busy"
              :can-add="canAddRemark"
              :can-delete="canDeleteRemark"
              @add="addRemark"
              @remove="removeRemark"
            />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import moment from "moment";
import { UserModule, ReferenceModule } from "@/store";
import { getStudent } from "@/api/students";
import { hasPermission } from "@/utils/permissions";
import {
  getFormationReports, getFormationRosterCount, createFormationReport, updateFormationReport,
  getFormationCategories, createFormationRemark, deleteFormationRemark,
} from "@/api/formations";
import FormationHeadcount from "./FormationHeadcount.vue";
import FormationRemarks from "./FormationRemarks.vue";

const formFromReport = report => ({
  roster_count: report ? report.roster_count : null,
  excused_count: report ? report.excused_count : 0,
  unexcused_count: report ? report.unexcused_count : 0,
  unknown_count: report ? report.unknown_count : 0,
  comment: report ? report.comment : "",
});

export default {
  name: "Formations",
  components: { FormationHeadcount, FormationRemarks },
  data() {
    return {
      date: moment().format("YYYY-MM-DD"),
      selectedGroupId: null,
      reports: [],
      drafts: {},
      draftSources: {},
      students: [],
      categories: [],
      loading: true,
      loadError: "",
      studentsLoading: false,
      reportRequest: 0,
      studentRequest: 0,
      saving: false,
      savingRemark: false,
    };
  },
  computed: {
    isHead() {
      return hasPermission(["formation-reports.get.milfaculty"]);
    },
    isHistoricalDate() {
      return this.date < moment().format("YYYY-MM-DD");
    },
    groups() {
      const groups = ReferenceModule.milgroups.filter(group => !group.archived
        || this.reports.some(report => report.milgroup === group.id));
      if (hasPermission(["formation-reports.get.all"])) {
        return groups;
      }
      if (this.isHead) {
        return groups.filter(group => group.milfaculty.id === +UserModule.personMilfaculty);
      }
      return groups.filter(group => UserModule.personMilgroups.includes(group.id));
    },
    selectedGroup() {
      return this.groups.find(group => group.id === this.selectedGroupId);
    },
    report() {
      return this.reports.find(item => item.milgroup === this.selectedGroupId) || null;
    },
    contextKey() {
      return `${this.date}/${this.selectedGroupId}`;
    },
    form() {
      return this.drafts[this.contextKey];
    },
    summaryRows() {
      const groups = this.isHistoricalDate
        ? this.groups.filter(group => this.reports.some(report => report.milgroup === group.id))
        : this.groups;
      return groups.map(group => ({
        id: group.id,
        title: group.title,
        report: this.reports.find(item => item.milgroup === group.id),
      }));
    },
    filledCount() {
      return this.summaryRows.filter(row => row.report).length;
    },
    totals() {
      return this.reports
        .filter(report => this.groups.some(group => group.id === report.milgroup))
        .reduce((total, report) => ({
          roster_count: total.roster_count + report.roster_count,
          present_count: total.present_count + report.present_count,
          absent_count: total.absent_count + report.absent_count,
        }), { roster_count: 0, present_count: 0, absent_count: 0 });
    },
    busy() {
      return this.saving || this.savingRemark;
    },
    canEditReport() {
      return hasPermission([`formation-reports.${this.report ? "patch" : "post"}.milgroup`]);
    },
    canViewRemarks() {
      return this.isHead && hasPermission(["formation-remarks.get.milfaculty"]);
    },
    canAddRemark() {
      return hasPermission(["formation-remarks.post.milfaculty"]);
    },
    canDeleteRemark() {
      return hasPermission(["formation-remarks.delete.milfaculty"]);
    },
  },
  created() {
    this.initialize();
  },
  methods: {
    async initialize() {
      this.loading = true;
      this.loadError = "";
      try {
        await UserModule.getUser();
        await ReferenceModule.fetchMilgroups();
        if (this.canViewRemarks) {
          this.categories = Object.values((await getFormationCategories()).data);
        }
        await this.loadReports();
      } catch (error) {
        this.loadError = "Не удалось загрузить построения";
        this.showError(error, this.loadError);
      } finally {
        this.loading = false;
      }
    },
    showError(error, fallback) {
      const data = error.response && error.response.data;
      const message = data && (data.detail || (data.non_field_errors && data.non_field_errors[0]));
      this.$message.error(message || fallback);
    },
    setForm(form) {
      this.$set(this.drafts, this.contextKey, form);
    },
    fillForm() {
      const source = this.draftSources[this.contextKey];
      const unchanged = source && Object.keys(source).every(field => this.form[field] === source[field]);
      if (this.selectedGroup && (!this.form || unchanged)) {
        const form = formFromReport(this.report);
        this.setForm(form);
        this.$set(this.draftSources, this.contextKey, form);
      }
    },
    async prefillRosterCount() {
      if (!this.selectedGroup || this.report || !this.canEditReport) {
        return;
      }
      const { contextKey, form } = this;
      if (!form || form.roster_count !== null) {
        return;
      }
      try {
        const { data } = await getFormationRosterCount(this.selectedGroupId);
        if (data.count > 0 && this.contextKey === contextKey
          && !this.report && this.form === form) {
          this.setForm({ ...form, roster_count: data.count });
        }
      } catch (_) {
        this.$message.warning("Не удалось подсчитать численность; введите её вручную");
      }
    },
    async loadReports() {
      if (!this.date) {
        return;
      }
      const { date } = this;
      this.reportRequest += 1;
      const request = this.reportRequest;
      this.loading = true;
      this.loadError = "";
      try {
        const { data } = await getFormationReports({ date });
        if (request !== this.reportRequest) {
          return;
        }
        this.reports = data;
        if (!this.groups.some(group => group.id === this.selectedGroupId)) {
          const group = this.summaryRows[0] || this.groups[0];
          this.selectedGroupId = group ? group.id : null;
        }
        this.fillForm();
        this.prefillRosterCount();
        if (this.canViewRemarks) {
          await this.loadStudents();
        }
      } catch (error) {
        if (request === this.reportRequest) {
          this.loadError = "Не удалось загрузить сведения за выбранную дату";
          this.showError(error, this.loadError);
        }
      } finally {
        if (request === this.reportRequest) {
          this.loading = false;
        }
      }
    },
    async loadStudents() {
      const groupId = this.selectedGroupId;
      this.studentRequest += 1;
      const request = this.studentRequest;
      this.students = [];
      this.studentsLoading = !!groupId;
      if (!groupId) {
        return;
      }
      try {
        const { data } = await getStudent({ milgroup: groupId });
        if (request === this.studentRequest && this.selectedGroupId === groupId) {
          this.students = data;
        }
      } catch (error) {
        if (request === this.studentRequest && this.selectedGroupId === groupId) {
          this.showError(error, "Не удалось загрузить студентов");
        }
      } finally {
        if (request === this.studentRequest) {
          this.studentsLoading = false;
        }
      }
    },
    async chooseGroup(id) {
      if (this.busy || id === this.selectedGroupId) {
        return;
      }
      this.selectedGroupId = id;
      this.fillForm();
      this.prefillRosterCount();
      if (this.canViewRemarks) {
        await this.loadStudents();
      }
    },
    async saveReport(payload) {
      if (this.busy || !this.canEditReport) {
        return;
      }
      const { contextKey, selectedGroupId, date } = this;
      this.saving = true;
      try {
        const { data } = this.report
          ? await updateFormationReport(this.report.id, payload)
          : await createFormationReport({ ...payload, milgroup: selectedGroupId, date });
        const index = this.reports.findIndex(report => report.id === data.id);
        if (index === -1) {
          this.reports.push(data);
        } else {
          this.$set(this.reports, index, data);
        }
        this.$set(this.drafts, contextKey, formFromReport(data));
        this.$set(this.draftSources, contextKey, formFromReport(data));
        this.$message.success("Сведения сохранены");
      } catch (error) {
        this.showError(error, "Не удалось сохранить сведения");
      } finally {
        this.saving = false;
      }
    },
    async addRemark(payload) {
      if (this.busy || !this.report || !this.canAddRemark) {
        return;
      }
      const { report } = this;
      this.savingRemark = true;
      try {
        const { data } = await createFormationRemark({ ...payload, report: report.id });
        report.remarks.push(data);
        this.$refs.remarks.reset();
        this.$message.success("Замечание добавлено");
      } catch (error) {
        this.showError(error, "Не удалось добавить замечание");
      } finally {
        this.savingRemark = false;
      }
    },
    async removeRemark(id) {
      if (this.busy || !this.report || !this.canDeleteRemark) {
        return;
      }
      const { report } = this;
      try {
        await this.$confirm("Удалить это замечание?", "Удаление замечания", {
          confirmButtonText: "Удалить", cancelButtonText: "Отмена", type: "warning",
        });
      } catch (_) {
        return;
      }
      this.savingRemark = true;
      try {
        await deleteFormationRemark(id);
        report.remarks = report.remarks.filter(remark => remark.id !== id);
        this.$message.success("Замечание удалено");
      } catch (error) {
        this.showError(error, "Не удалось удалить замечание");
      } finally {
        this.savingRemark = false;
      }
    },
  },
};
</script>

<style lang="scss">
@import "style";
</style>
