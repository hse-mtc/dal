<template>
  <div>
    <el-col :span="24" class="scienceWork">
      <el-row class="pageTitle">
        <el-col :offset="2">
          Военно-научная работа
        </el-col>
      </el-row>

      <div class="categories-block" v-if="categories.length">
        <el-row class="select-work">
          <el-col :span="10" :offset="2">
            <span class="category-selected" @click="openAllCategories">{{ category.title }}</span>
            <img
                id="dark-arrow"
                src="../../assets/scienceWorks/dropdownBlack.svg"
                alt="Открыть список категорий"
                class="ml-2"
                style="cursor:pointer;"
                @click="openAllCategories"
            >
          </el-col>

          <el-col :span="7">
            <div class="add-document-top" @click="openPaperModal('add')">
              Добавить новый документ
            </div>
          </el-col>
        </el-row>

        <el-row v-if="modalCategories" class="categories-selector">
          <el-col :offset="2" :span="20" class="categories-title">
            <el-row style="width: 100%">
              <el-col
                  v-for="{id, title} in categories"
                  :key="id"
                  :span="12"
                  class="category-title"
              >
                <div>
                  <span style="cursor:pointer;" :id="id"
                        @click="selectCategory(id)">
                    {{ title }}
                  </span>
                  <img
                      @click="deleteCategory(id)"
                      class="category-delete ml-2"
                      height="10px"
                      src="../../assets/scienceWorks/close.svg"
                      alt="Удалить категорию"
                  />
                </div>
              </el-col>

              <el-col :span="12" class="category-title" style="color: #0050B2">
                <span @click="addNewPaperCategory" style="cursor: pointer">Добавить новую категорию</span>
              </el-col>
            </el-row>
          </el-col>

          <el-col :span="1" class="cross-col">
            <img src="../../assets/scienceWorks/cross.svg" alt="" @click="closeSelectCategory">
          </el-col>
        </el-row>
      </div>

      <el-row class="search ">
        <el-col :span="12" :offset="2">
          <Search placeholder="Введите ключевые слова"/>
          <AdvancedSearch class="advanced-search"/>
          <Documents
              class="documents"
              v-on:openPaperModal="openPaperModal"
          />
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

    <AddCategoryModalWindow
        v-if="addNewCategory"
        v-on:closeModal="closeModal"
    />
    <UpsertPaperModal
        v-if="paperAction"
        :action="paperAction"
        :paper="paperToEdit"
        v-on:closeModal="closeModal"
    />

    <div v-if="paperAction || addNewCategory" class="background" @click="closeModal"/>
  </div>
</template>

<script>
import {mapState, mapActions} from 'vuex'
import {FunctionalCalendar} from 'vue-functional-calendar'

import Documents from '@/components/Documents/Documents'
import UpsertPaperModal from "@/components/Documents/UpsertPaperModal"

import Search from '@/components/Search/Search'
import AdvancedSearch from '@/components/AdvancedSearch/AdvancedSearch'
import AddCategoryModalWindow from "@/components/AddCategoryModalWindow/AddCategoryModalWindow"

import {getPaperCategories, deletePaperCategory} from "@/api/paper_categories"
import EventBus from "@/components/EventBus"

export default {
  name: '',
  components: {
    AddCategoryModalWindow,
    AdvancedSearch,
    Documents,
    FunctionalCalendar,
    Search,
    UpsertPaperModal,
  },

  data() {
    return {
      calendarData: undefined,

      documents: [],
      count: undefined,

      paperAction: "",
      paperToEdit: {},

      category: {},
      modalCategories: false,
      addNewCategory: false,
    }
  },

  created() {
    this.$router.replace({name: 'Science Articles', query: {category: "1"}})
    this.fetchData()
  },
  mounted() {
    const self = this
    EventBus.$on('UPDATE_CATEGORY', function () {
      self.fetchData()
    })
  },

  computed: {
    ...mapState({
      categories: state => state.documents.categories,
    })
  },

  methods: {
    ...mapActions({
      setCategories: 'documents/setCategories',
    }),

    startScrolling() {
      document.getElementById('main-container').classList.remove('stop-scrolling')
    },
    stopScrolling() {
      document.getElementById('main-container').classList.add('stop-scrolling')
    },

    openPaperModal(action, paperToEdit = {}) {
      console.log("Open Paper Modal: action = ", action, " to edit = ", paperToEdit)
      this.paperAction = action
      this.paperToEdit = paperToEdit
      this.stopScrolling()
    },

    // Any modal (paper or category)
    closeModal() {
      console.log("Close modal")
      this.paperAction = ""
      this.paperToEdit = {}
      this.addNewCategory = false
      this.startScrolling()
    },

    closeSelectCategory() {
      this.modalCategories = false
      this.modalCategories ? document.getElementById('dark-arrow').style.transform = 'rotate(180deg)' : document.getElementById('dark-arrow').style.transform = 'rotate(0deg)'
    },
    openAllCategories() {
      this.modalCategories = !this.modalCategories
      this.modalCategories ? document.getElementById('dark-arrow').style.transform = 'rotate(180deg)' : document.getElementById('dark-arrow').style.transform = 'rotate(0deg)'
    },
    async deleteCategory(id) {
      await this.$confirm('Вы уверены?', 'Подтвердите действие', {
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отменить',
        type: 'warning'
      })

      try {
        await deletePaperCategory(id)
      } catch (error) {
        console.log("Failed to delete Category: ", error)
        return
      }

      await this.fetchData()
      this.$message({
        type: 'success',
        message: 'Удаление завершено'
      })
    },
    addNewPaperCategory() {
      this.addNewCategory = true
    },

    async fetchData() {
      try {
        const categories = (await getPaperCategories()).data
        this.setCategories(categories)
        this.category = categories[0]
      } catch (error) {
        console.log("Failed to fetch Categories: ", error)
      }
    },

    selectCategory(id) {
      this.category = this.categories.find(category => category.id === id)
      this.$router.replace({name: 'Science Articles', query: {category: id.toString()}})
      this.modalCategories = false
      this.modalCategories ? document.getElementById('dark-arrow').style.transform = 'rotate(180deg)' : document.getElementById('dark-arrow').style.transform = 'rotate(0deg)'
    },
  }
}
</script>

<style scoped lang="scss">
@import "style";
</style>
