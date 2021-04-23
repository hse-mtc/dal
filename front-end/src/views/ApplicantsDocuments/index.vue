<template>
  <div :class="$style.root">
    <h1>Прием документов</h1>

    <TextInput
      :class="$style.input"
      v-model="searchQuery"
      placeholder="Введите ФИО студента"
      @change="search"
    />

    <InfoTable
      :key="`${currentPage}-${entriesAmount}`"
      :class="$style.table"
      :data="data"
      :start-index="(currentPage - 1) * PAGE_SIZE"
      @update="onUpdate"
    />

    <div :class="$style.pagination">
      <el-pagination
        layout="prev, pager, next, jumper"
        :total="entriesAmount"
        :current-page="currentPage"
        :page-size="PAGE_SIZE"
        @current-change="fetchData"
      />
    </div>
  </div>
</template>

<script>
import _debounce from "lodash/debounce";
import moment from "moment";

import { getApplicationsStudents } from "@/api/students";
import { updateStudentApplicationInfo } from "@/api/student";

import { TextInput } from "@/common/inputs";
import InfoTable from "@/components/@ApplicantsDocuments/Table.vue";

export default {
  name: "ApplicantsDocuments",
  components: {
    InfoTable,
    TextInput,
  },
  created() {
    this.fetchData(1);
  },
  data() {
    return {
      data: [],
      entriesAmount: 0,
      currentPage: 1,
      searchQuery: "",
      PAGE_SIZE: 50,
    };
  },
  methods: {
    async fetchData(page) {
      this.currentPage = page ? page : 1;
      const { data } = await getApplicationsStudents(page, this.PAGE_SIZE, {
        search: this.searchQuery,
      });
      this.data = data.results.map((item) => ({
        id: item.id,
        fullname: item.full_name,
        birthday: moment(item.birth_date).format("DD.MM.yyyy"),
        passport: item.passport,
        program: item.program_code,
        faculty: item.faculty,
        ...item.application_process,
      }));
      this.entriesAmount = data.count;
    },

    async onUpdate({ id, key, value }) {
      try {
        await updateStudentApplicationInfo(id, { [key]: value });
      } catch (e) {
        console.error("Не удалось обновить данные студента о поступлении: ", e);
        this.$message.error(
          "Не удалось обновить данные, рекомендуем перезагрузить страницу"
        );
      }
    },

    search: _debounce(function () {
      this.currentPage = 1;
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
.input {
  margin-top: 20px;
}

.table {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
}
</style>
