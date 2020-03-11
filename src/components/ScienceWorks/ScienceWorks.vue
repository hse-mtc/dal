<template>
  <div>
    <el-col :span="24" class="scienceWork">
      <el-row class="pageTitle">
        <el-col  :offset="2">
          Военно-научная работа
        </el-col>
      </el-row>
      <div class="categories-block" v-if="categories.length">
        <el-row class="select-work">
          <el-col :span="10" :offset="2">
            <span class="category-selected" @click="modalCategories = !modalCategories">{{this.selectedCategory.title}}</span>
            <img id="dark-arrow" src="../../assets/scienceWorks/dropdownBlack.svg" alt="" class="ml-2" style="cursor:pointer;" @click="openAllCategories">
          </el-col>
          <el-col :span="7">
            <div class="add-document-top" @click="openModal"><span>Добавить новый документ</span></div>
          </el-col>
        </el-row>
        <el-row v-if="modalCategories" class="categories-selector">
          <el-col :offset="2" :span="20" class="categories-title">
            <el-row style="width: 100%">
              <el-col :span="12" v-for="(category, index) in categories" :key="category.id" class="category-title" >
                <div><span style="cursor:pointer;" :id="category.id" @click="selectCategory($event)">{{category.title}}</span> <img @click="deleteCategory(category.id)" class="category-delete ml-2" height="10px" src="../../assets/scienceWorks/close.svg" alt=""></div>
              </el-col>
              <el-col :span="12" class="category-title" style="color: #0050B2">
                <span @click="addNewPaperCategory" style="cursor: pointer">Добавить новую категорию</span>
              </el-col>
            </el-row>
          </el-col>
          <el-col :span="1" class="cross-col">
            <img src="../../assets/scienceWorks/cross.svg" alt="" @click="modalCategories = false">
          </el-col>
        </el-row>
      </div>
<!--      <el-row class="selectWork">-->
<!--        <el-col :span="4">-->
<!--          <div id="scienceArticles" class="selectWork-item selected" @click="selectClick($event)">-->
<!--            Научные статьи-->
<!--          </div>-->
<!--        </el-col>-->
<!--        <el-col :span="8" :offset="1">-->
<!--          <div id="scienceWorks" class="selectWork-item" @click="selectClick($event)">-->
<!--            Научно-исследовательские работы-->
<!--          </div>-->
<!--        </el-col>-->
<!--      </el-row>-->
      <el-row class="search ">
        <el-col :span="12" :offset="2">
          <Search placeholder="Введите ключевые слова" />
<!--          <div class="add-document" @click="openModal">+ <span>Добавить публикацию</span></div>-->
          <AdvancedSearch class="advanced-search" />
          <Documents class="documents" />
        </el-col>
        <el-col :offset="1" :span="8">
          <FunctionalCalendar
                  v-model="calendarData"
                  :is-date-range="true"
                  :change-month-function="true"
                  :change-year-function="true"
          />
        </el-col>
      </el-row>
    </el-col>
    <AddCategoryModalWindow v-if="addNewCategory" v-on:closeModal="closeModal" />
    <AddModalWindow v-if="addModal" v-on:closeModal="closeModal" />
    <div v-if="addModal || addNewCategory" class="background" @click="closeModal"></div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
  import Search from '../Search/Search'
  import AdvancedSearch from '../AdvancedSearch/AdvancedSearch'
  import Documents from '../Documents/Documents'
  import { FunctionalCalendar } from 'vue-functional-calendar'
  import AddModalWindow from "../AddModalWindow/AddModalWindow";
  import {getPaperCategories, deletePaperCategories} from "../../api/paper_сategories";
  import AddCategoryModalWindow from "../AddCategoryModalWindow/AddCategoryModalWindow";
  import EventBus from "../EventBus";

export default {
  name: '',
  components: {
    AddCategoryModalWindow,
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
      selectedCategory: {},
      modalCategories: false,
      addNewCategory: false,
      // categories: [
      //   {
      //     title: 'Научно-исследовательские работы',
      //     id: 1
      //   },
      //   {
      //     title: 'Научные статьи',
      //     id: 2
      //   },
      //   {
      //     title: 'Хер',
      //     id: 3
      //   }
      // ]
    }
  },
  created() {
    this.fetchData()
  },
  mounted() {
    const self = this
    EventBus.$on('UPDATE_CATEGORY', function () {
      console.log('update')
      self.fetchData()
    })
  },
  computed: {
    ...mapState({
      categories: state => state.documents.categories
    })
  },
  methods: {
    ...mapActions({
      setCategories: 'documents/setCategories',
    }),
    openAllCategories() {
      this.modalCategories = !this.modalCategories
      this.modalCategories ? document.getElementById('dark-arrow').style.transform = 'rotate(180deg)' : document.getElementById('dark-arrow').style.transform = 'rotate(0deg)'
    },
    deleteCategory(id) {
      this.$confirm('Вы уверены?', 'Подтвердите действие', {
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отменить',
        type: 'warning'
      })
              .then(() => {
                deletePaperCategories({id: id}).then(response => {
                  this.categories.filter(item => {
                    item.id !== id
                  })
                  console.log('Категория удалена')
                  this.fetchData()
                  this.$message({
                    type: 'success',
                    message: 'Удаление завершено'
                  })
                }).catch(() => {
                  console.log('Ошибка удаления категории')
                })
              })
              .catch(() => { })
    },
    addNewPaperCategory() {
      this.addNewCategory = true
    },
    fetchData() {
      getPaperCategories()
              .then(response => {
                console.log(response.data)
                this.setCategories(response.data)
                this.selectedCategory = response.data[0]
              }).catch(() => {
                 console.log('Данных по категориям нет')
              })
    },
    closeModal() {
      this.addModal = false
      this.addNewCategory = false

      document.getElementById('main-container').classList.remove('stop-scrolling')
    },
    openModal() {
      this.addModal = true
      document.getElementById('main-container').classList.add('stop-scrolling')
    },
    selectCategory(event) {
      this.selectedCategory =  {
        title: this.categories.filter(item => item.id == event.target.id)[0].title,
        id: event.target.id
      }
      this.$router.replace({ name: 'Science Articles', query: { section: event.target.id }})
      this.modalCategories = false
    },
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
