<template>
  <div>
    <el-col :span="24" class="scienceWork">
      <el-row class="pageTitle">
        <el-col :offset="2" :span="22">
          Военно-научные работы
        </el-col>
      </el-row>

      <div v-if="categories.length" class="categories-block">
        <el-row class="select-work">
          <el-col :span="10" :offset="2">
            <span class="category-selected" @click="toggleCategorySelector">
              {{ category.title }}
            </span>
            <img
              id="dark-arrow"
              src="../../assets/scienceWorks/dropdownBlack.svg"
              alt="Открыть список категорий"
              class="ml-2"
              style="cursor: pointer"
              @click="toggleCategorySelector"
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
                v-for="{ id, title } in categories"
                :key="id"
                :span="12"
                class="category-title"
              >
                <div>
                  <span
                    :id="id"
                    style="cursor: pointer"
                    @click="selectCategory(id)"
                  >
                    {{ title }}
                  </span>
                  <img
                    class="category-delete ml-2"
                    height="10px"
                    src="../../assets/scienceWorks/close.svg"
                    alt="Удалить категорию"
                    @click="deleteCategory(id)"
                  >
                </div>
              </el-col>

              <el-col :span="12" class="category-title" style="color: #0050b2">
                <span
                  style="cursor: pointer"
                  @click="addNewPaperCategory"
                >Добавить новую категорию</span>
              </el-col>
            </el-row>
          </el-col>

          <el-col :span="1" class="cross-col">
            <img
              src="../../assets/scienceWorks/cross.svg"
              alt=""
              @click="closeCategorySelector"
            >
          </el-col>
        </el-row>
      </div>

      <el-row class="search">
        <el-col :span="12" :offset="2">
          <Search placeholder="Введите ключевые слова" />
          <AdvancedSearch class="advanced-search" />
          <Documents class="documents" @openPaperModal="openPaperModal" />
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
      @closeModal="closeModal"
    />
    <UpsertPaperModal
      v-if="paperAction"
      :action="paperAction"
      :paper="paperToEdit"
      @closeModal="closeModal"
    />

    <div
      v-if="paperAction || addNewCategory"
      class="background"
      @click="closeModal"
    />
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import { FunctionalCalendar } from "vue-functional-calendar";

import Documents from "@/components/Documents/Documents";
import UpsertPaperModal from "@/components/Documents/UpsertPaperModal";

import Search from "@/components/Search/Search";
import AdvancedSearch from "@/components/AdvancedSearch/AdvancedSearch";
import AddCategoryModalWindow from "@/components/AddCategoryModalWindow/AddCategoryModalWindow";

import {
  getPaperCategories,
  deletePaperCategory,
} from "@/api/paper_categories";
import EventBus from "@/components/EventBus";

export default {
  name: "",
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
    };
  },

  computed: {
    ...mapState({
      categories: state => state.documents.categories,
    }),
  },

  created() {
    this.fetchData();
  },
  mounted() {
    const self = this;
    EventBus.$on("UPDATE_CATEGORY", () => {
      self.fetchData();
    });
  },

  methods: {
    ...mapActions({
      setCategories: "documents/setCategories",
    }),

    startScrolling() {
      document
        .getElementById("main-container")
        .classList.remove("stop-scrolling");
    },
    stopScrolling() {
      document.getElementById("main-container").classList.add("stop-scrolling");
    },

    openPaperModal(action, paperToEdit = {}) {
      console.log(
        "Open Paper Modal: action = ",
        action,
        " to edit = ",
        paperToEdit,
      );
      this.paperAction = action;
      this.paperToEdit = paperToEdit;
      this.stopScrolling();
    },

    // Any modal (paper or category)
    closeModal() {
      console.log("Close modal");
      this.paperAction = "";
      this.paperToEdit = {};
      this.addNewCategory = false;
      this.startScrolling();
    },

    rotateArrow() {
      const arrow = document.getElementById("dark-arrow");
      if (arrow) {
        arrow.style.transform = this.modalCategories
          ? "rotate(180deg)"
          : "rotate(0deg)";
      }
    },
    closeCategorySelector() {
      this.modalCategories = false;
      this.rotateArrow();
    },
    toggleCategorySelector() {
      this.modalCategories = !this.modalCategories;
      this.rotateArrow();
    },
    async deleteCategory(id) {
      await this.$confirm("Вы уверены?", "Подтвердите действие", {
        confirmButtonText: "Удалить",
        cancelButtonText: "Отменить",
        type: "warning",
      });

      try {
        await deletePaperCategory(id);
      } catch (error) {
        console.log("Failed to delete Category: ", error);
        return;
      }

      await this.fetchData();
      this.$message({
        type: "success",
        message: "Удаление завершено",
      });
    },
    addNewPaperCategory() {
      this.addNewCategory = true;
    },

    async fetchData() {
      let categories;
      try {
        categories = (await getPaperCategories()).data;
      } catch (error) {
        console.log("Failed to fetch Categories: ", error);
      }

      this.setCategories(categories);
      this.selectCategory(categories[0].id);
    },

    selectCategory(id) {
      this.category = this.categories.find(category => category.id === id);
      this.$router.replace({
        name: "Science Articles",
        query: { category: id.toString() },
      });
      this.closeCategorySelector();
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
