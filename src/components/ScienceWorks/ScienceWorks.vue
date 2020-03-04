<template>
  <div>
    <el-col :offset="2" :span="20" class="scienceWork">
      <el-row class="pageTitle">
        <el-col>
          Военно-научная работа
        </el-col>
      </el-row>
      <el-row class="selectWork">
        <el-col :span="4">
          <div id="scienceArticles" class="selectWork-item selected" @click="selectClick($event)">
            Научные статьи
          </div>
        </el-col>
        <el-col :span="8" :offset="1">
          <div id="scienceWorks" class="selectWork-item" @click="selectClick($event)">
            Научно-исследовательские работы
          </div>
        </el-col>
      </el-row>
      <el-row class="search ">
        <el-col :span="14">
          <Search placeholder="Введите ключевые слова" />
          <div class="add-document" @click="addModal=true">+ <span>Добавить публикацию</span></div>
          <AdvancedSearch class="advanced-search" />
          <Documents class="documents" />
        </el-col>
        <el-col :offset="2" :span="8">
          <FunctionalCalendar
                  v-model="calendarData"
                  :is-date-range="true"
                  :change-month-function="true"
                  :change-year-function="true"
          />
        </el-col>
      </el-row>
    </el-col>
    <AddModalWindow v-if="addModal" v-on:closeModal="addModal = false" />
    <div v-if="addModal" class="background" @click="addModal = false"></div>
  </div>
</template>

<script>
import Search from '../Search/Search'
import AdvancedSearch from '../AdvancedSearch/AdvancedSearch'
import Documents from '../Documents/Documents'
import { FunctionalCalendar } from 'vue-functional-calendar'
import AddModalWindow from "../AddModalWindow/AddModalWindow";

export default {
  name: '',
  components: {
    AddModalWindow,
    Search,
    AdvancedSearch,
    Documents,
    FunctionalCalendar
  },
  data() {
    return {
      calendarData: undefined,
      documents: [],
      count: undefined,
      addModal: false,
    }
  },
  created() {
    this.$router.replace({ name: 'Science Articles', query: { section: 'scienceArticles' }})
  },
  methods: {
    selectClick(event) {
      Array.from(document.getElementsByClassName(event.target.className)).forEach(item => item.classList.remove('selected'))
      event.target.classList.add('selected')
      this.$router.replace({ name: 'Science Articles', query: { section: event.target.id }})
    }
  }
}
</script>

<style scoped lang="scss">
  @import "style";
</style>
