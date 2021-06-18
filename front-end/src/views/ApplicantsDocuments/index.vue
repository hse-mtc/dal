<template>
  <div :class="$style.root">
    <h1>Прием документов</h1>

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
        <el-col :span="4">
          <el-alert
            type="info"
            class="text-center"
            :closable="false"
            :title="'Всего абитуриентов: ' + entriesAmount"
          />
        </el-col>
        <el-col v-if="!isStudyOffice" :span="4">
          <el-button type="success" plain @click="getExcel">
            <i class="el-icon-download" /> Экспорт в Excel
          </el-button>
        </el-col>
      </el-row>

      <InfoTable
        :key="`${currentPage}-${entriesAmount}`"
        :class="$style.table"
        :data="data"
        :start-index="(currentPage - 1) * pageSize"
        @update="onUpdate"
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
import { mapGetters } from "vuex";

import { getApplicationsStudents, updateStudentApplicationInfo, getApplicationsExcelDownloadLink } from "@/api/students";
import { getPrograms } from "@/api/reference-book";

import { TextInput } from "@/common/inputs";
import InfoTable from "@/components/@ApplicantsDocuments/Table.vue";

export default {
  name: "ApplicantsDocuments",
  components: {
    InfoTable,
    TextInput,
  },
  filters: {
    campusFilter(campus) {
      switch (campus) {
        case "MO":
          return "Москва";
        case "SP":
          return "Санкт-Петербург";
        case "NN":
          return "Нижний Новгород";
        case "PE":
          return "Пермь";
        default:
          return "Ошибка";
      }
    },
  },
  data() {
    const selectedCampus = this.$store.state.user.campuses.length > 0
      ? this.$store.state.user.campuses[0]
      : "MO";
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
    };
  },
  computed: {
    isStudyOffice() {
      // TODO(gakhromov): remove this check when permissions are done
      return this.$store.state.user.email.includes("study.office");
    },
    ...mapGetters(["campuses"]),
  },
  created() {
    this.loading = true;
    this.fetchPrograms();
    this.fetchData();
  },
  methods: {
    getExcel() {
      window.location.href = getApplicationsExcelDownloadLink(this.selectedCampus);
    },
    async fetchPrograms() {
      this.programs = (await getPrograms()).data;
    },
    async changeProgram(program) {
      this.selectedProgram = program;
      this.$router.push({ query: { program } });
      await this.fetchData();
    },
    async changeCampus(campus) {
      this.selectedCampus = campus;
      await this.fetchData();
    },
    async fetchData(page = 1) {
      this.currentPage = page || 1;
      this.loading = true;
      const { data } = await getApplicationsStudents(
        this.currentPage,
        this.pageSize,
        {
          search: this.searchQuery,
          campus: this.selectedCampus,
          program: this.selectedProgram,
        },
      );
      this.data = data.results.map(item => ({
        id: item.id,
        fullname: item.full_name,
        birthday: moment(item.birth_date).format("DD.MM.yyyy"),
        passport: item.passport,
        program: item.program_code,
        faculty: item.faculty,
        ...item.application_process,
      }));
      this.entriesAmount = data.count;
      this.loading = false;
    },

    async onPageSizeChange(pageSize) {
      this.pageSize = pageSize;
      await this.fetchData();
    },

    async onUpdate({ id, key, value }) {
      try {
        await updateStudentApplicationInfo(id, { [key]: value });
      } catch (e) {
        console.error("Не удалось обновить данные студента о поступлении: ", e);
        this.$message.error(
          "Не удалось обновить данные, рекомендуем перезагрузить страницу",
        );
      }
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

/deep/.el-alert__title {
  font-size: 1em;
}

.el-alert {
  background: transparent;
  border-style: solid;
  border-color: rgb(220, 223, 230);
  border-width: 1px;
}
</style>
