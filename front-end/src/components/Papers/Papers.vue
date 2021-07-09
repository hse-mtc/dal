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
          <el-col :offset="1" :span="22" class="categories-title">
            <el-row style="width: 100%">
              <el-col
                v-for="{ id, title } in categories"
                :key="id"
                :span="12"
                class="category-title"
              >
                <div>
                  <span
                    v-if="id !== 'bin'"
                    :id="id"
                    style="cursor: pointer"
                    @click="selectCategory({ id, title })"
                  >
                    {{ title }}
                  </span>
                  <img
                    v-if="id !== 'bin'"
                    class="category-delete ml-2"
                    height="10px"
                    src="../../assets/scienceWorks/close.svg"
                    alt="Удалить категорию"
                    @click="deleteCategory(id)"
                  >
                  <span
                    v-if="id === 'bin'"
                    style="cursor: pointer; color: #858587"
                    @click="selectCategory('bin')"
                  >
                    Корзина
                  </span>
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
        <el-col :span="16" :offset="2">
          <Search placeholder="Введите ключевые слова" />
          <AdvancedSearch class="advanced-search" />
          <Serp class="documents" @openPaperModal="openPaperModal" />
        </el-col>
      </el-row>
    </el-col>

    <AddCategoryModal
      v-if="addNewCategory"
      @closeModal="closeModal"
    />
    <UpsertModal
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
import { Component, Watch } from "vue-property-decorator";

import Serp from "@/components/Papers/Serp";
import UpsertModal from "@/components/Papers/UpsertModal";

import Search from "@/components/Search/Papers";
import AdvancedSearch from "@/components/Search/PapersAdvanced.vue";
import AddCategoryModal from "@/components/Categories/AddModal.vue";

import { PapersModule } from "@/store";

@Component({
  name: "Papers",
  components: {
    AddCategoryModal,
    AdvancedSearch,
    Serp,
    Search,
    UpsertModal,
  },
})
class Papers {
  calendarData = null

  documents = []
  count = null

  paperAction = ""
  paperToEdit = {}

  category = {}
  modalCategories = false
  addNewCategory = false

  get categories() { return [...PapersModule.categories, { title: "Корзина", id: "bin" }]; }

  created() {
    this.selectCategory(this.categories[0]);
  }

  startScrolling() {
    document
      .getElementById("main-container")
      .classList.remove("stop-scrolling");
  }

  stopScrolling() {
    document.getElementById("main-container").classList.add("stop-scrolling");
  }

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
  }

  closeModal() {
    this.paperAction = "";
    this.paperToEdit = {};
    this.addNewCategory = false;
    this.startScrolling();
  }

  rotateArrow() {
    const arrow = document.getElementById("dark-arrow");
    if (arrow) {
      arrow.style.transform = this.modalCategories
        ? "rotate(180deg)"
        : "rotate(0deg)";
    }
  }

  closeCategorySelector() {
    this.modalCategories = false;
    this.rotateArrow();
  }

  toggleCategorySelector() {
    this.modalCategories = !this.modalCategories;
    this.rotateArrow();
  }

  async deleteCategory(id) {
    await this.$confirm("Вы уверены?", "Подтвердите действие", {
      confirmButtonText: "Удалить",
      cancelButtonText: "Отменить",
      type: "warning",
    });

    if (await PapersModule.deleteCategory(id) && id === this.category.id) {
      this.selectCategory(this.categories[0]);
    }
  }

  addNewPaperCategory() {
    this.addNewCategory = true;
  }

  selectCategory(category) {
    if (!category) return;

    this.category = category;

    if (category.id) {
      this.$router.replace({
        name: "Papers",
        query: { category: category.id.toString() },
      });
    }
    this.closeCategorySelector();
  }

  @Watch("categories")
  onCategoriesChange(next) {
    if (!this.category.id) {
      ([this.category] = next);
    }
  }
}

export default Papers;
</script>

<style scoped lang="scss">
@import "papers";
</style>
