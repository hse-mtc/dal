<template>
  <div :class="$style.root">
    <h1>Учет поступления документов</h1>

    <div v-loading="loading">
      <el-row class="filter-row" :gutter="20">
        <el-col :span="8">
          <TextInput
            v-model="searchQuery"
            :class="$style.input"
            placeholder="Введите ФИО студента"
            @change="search"
          />
        </el-col>
        <el-col :span="4">
          <el-select
            v-model="selectedProgram"
            clearable
            filterable
            placeholder="Выберите код ОП"
            @change="changeProgram"
          >
            <el-option
              v-for="item in programs"
              :key="item.code"
              :label="item.code"
              :value="item.code"
            />
          </el-select>
        </el-col>
        <el-col v-if="campuses.length > 1" :span="4">
          <el-select
            v-model="selectedCampus"
            placeholder="Кампус"
            @change="changeCampus"
          >
            <el-option
              v-for="item in campuses"
              :key="item"
              :label="item | campusFilter"
              :value="item"
            />
          </el-select>
        </el-col>
        <el-col v-else :span="4">
          <el-alert
            type="info"
            class="text-center"
            :closable="false"
            :title="campuses[0] | campusFilter"
          />
        </el-col>
        <el-col :span="3">
          <el-alert
            type="info"
            class="text-center"
            :closable="false"
            :title="`Всего абитуриентов: ${entriesAmount}`"
          />
        </el-col>
        <el-col v-if="!isStudyOffice" :span="5">
          <el-dropdown
            split-button
            type="success"
            @command="handleExportOption"
          >
            <DownloadFile
              :url="makeExportLink()"
              :file-name="makeExportFilename()"
            >
              <i class="el-icon-download" /> Экспорт:
              {{ selectedExportOption }}
            </DownloadFile>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item
                icon="el-icon-document"
                command="DEF"
              >
                По умолчанию
              </el-dropdown-item>
              <el-dropdown-item
                icon="el-icon-document-copy"
                command="CSP"
              >
                Протокол конкурсного отбора
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-col>
      </el-row>

      <InfoTable
        :key="`${currentPage}-${entriesAmount}`"
        :class="$style.table"
        :data="data"
        :start-index="(currentPage - 1) * pageSize"
        :on-change="onUpdate"
      />

      <div :class="$style.pagination">
        <el-pagination
          layout="sizes, prev, pager, next, jumper"
          :total="entriesAmount"
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[5, 10, 20]"
          @current-change="fetchData"
          @size-change="onPageSizeChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import _debounce from "lodash/debounce";
import moment from "moment";

import {
  getApplicationsStudents,
  updateStudentApplicationInfo,
  APPLICATIONS_EXPORT_LINK,
  APPLICATIONS_CSP_EXPORT_LINK,
} from "@/api/applicants";
import { getPrograms } from "@/api/reference-book";

import { TextInput } from "@/common/inputs";
import InfoTable from "@/components/@ApplicantsDocuments/Table.vue";
import { UserModule } from "@/store";
import { CAMPUSES, APPLICATIONS_EXPORT_OPTIONS } from "@/utils/enums";
import DownloadFile from "@/common/DownloadFile";

export default {
  name: "ApplicantsDocuments",
  components: {
    DownloadFile,
    InfoTable,
    TextInput,
  },
  filters: {
    campusFilter(campus) {
      console.log("Campus = ", campus);
      return CAMPUSES[campus] || "Ошибка";
    },
  },
  data() {
    // FIXME(TmLev, i-oktav-i): `UserModule.campuses` is getter with async call.
    // Campuses are not being fetched on time, so `UserModule.campuses`
    // returns empty array, which always leads to default value being selected.
    // This is broken in so many ways :(
    const selectedCampus = UserModule.campuses.length > 0 ? UserModule.campuses[0] : null;
    return {
      data: [],
      programs: [],
      entriesAmount: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: "",
      loading: false,
      selectedCampus,
      selectedProgram: this.$route.query.program,
      selectedExportOption: APPLICATIONS_EXPORT_OPTIONS.DEF,
    };
  },
  computed: {
    isStudyOffice() {
      // TODO(gakhromov): remove this check when permissions are done
      return UserModule.email.includes("study.office");
    },
    campuses() {
      return UserModule.campuses;
    },
  },
  async beforeCreate() {
    // Try to fetch user campuses.
    const { campuses } = UserModule;
  },
  async created() {
    this.loading = true;

    const { campuses } = UserModule;
    await this.changeCampus(campuses[0]);

    await this.fetchPrograms();
    await this.fetchData();
  },
  methods: {
    async fetchPrograms() {
      try {
        this.programs = (await getPrograms()).data;
      } catch (e) {
        console.log("Не удалось загрузить программы", e);
      }
    },

    async changeProgram(program) {
      this.selectedProgram = program;
      this.$router.push({ query: { program_code: program } });
      await this.fetchData();
    },
    async changeCampus(campus) {
      this.selectedCampus = campus;
      await this.fetchData();
    },
    async fetchData(page = 1) {
      this.currentPage = page || 1;
      this.loading = true;

      let data;
      try {
        const response = await getApplicationsStudents(
          this.currentPage,
          this.pageSize,
          {
            search: this.searchQuery,
            campus: this.selectedCampus,
            program: this.selectedProgram,
          },
        );
        data = response.data;
      } catch (e) {
        console.log("Не удалось данные о студентах", e);
        return;
      } finally {
        this.loading = false;
      }

      this.data = data.results.map(item => ({
        birthday: moment(item.birth_date).format("DD.MM.yyyy"),
        faculty: item.faculty,
        fullname: item.fullname,
        id: item.id,
        passport: item.passport,
        program: item.program_code,
        ...item.application_process,
      }));
      this.entriesAmount = data.count;
    },

    async onPageSizeChange(pageSize) {
      this.pageSize = pageSize;
      await this.fetchData();
    },

    async onUpdate({ id, key, value }) {
      try {
        await updateStudentApplicationInfo(id, { [key]: value });
        return true;
      } catch (e) {
        console.error("Не удалось обновить данные студента о поступлении: ", e);
        this.$message.error(
          "Не удалось обновить данные, рекомендуем перезагрузить страницу",
        );
        return false;
      }
    },

    handleExportOption(type) {
      this.selectedExportOption = APPLICATIONS_EXPORT_OPTIONS[type];
    },

    makeExportLink() {
      switch (this.selectedExportOption) {
        case APPLICATIONS_EXPORT_OPTIONS.CSP:
          return `${APPLICATIONS_CSP_EXPORT_LINK}?campus=${this.selectedCampus}`;
        default:
          return `${APPLICATIONS_EXPORT_LINK}?campus=${this.selectedCampus}`;
      }
    },
    makeExportFilename() {
      return `${CAMPUSES[this.selectedCampus]}.xlsx`;
    },

    search: _debounce(function debouncedFetch() {
      this.fetchData();
    }, 750),
  },
};
</script>

<style lang="scss" module>
.root {
  padding: 50px;
}

.label {
  height: 150px;
  word-break: break-word !important;

  &.verticalText {
    writing-mode: vertical-rl;
  }
}

.table {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
}
</style>

<style lang="scss" scoped>
.filter-row {
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  align-items: center;
}

::v-deep .el-alert__title {
  font-size: 1em;
}

.el-alert {
  background: transparent;
  border-style: solid;
  border-color: rgb(220, 223, 230);
  border-width: 1px;
}
</style>
