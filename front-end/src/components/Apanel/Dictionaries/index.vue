<template>
  <div :class="$style.root">
    <el-input
      v-model="searchQuery"
      placeholder="Поиск"
      prefix-icon="el-icon-search"
      clearable
      :class="$style.search"
    />

    <div>
      <el-tabs v-model="currentTab" tab-position="left">
        <el-tab-pane
          v-for="({ label }, field) in tabs"
          :key="field"
          :name="field"
          :label="label"
        >
          <div
            v-if="currentTab === field"
            :class="$style.editor"
          >
            <div :class="$style.tagsWrapper">
              <el-tag
                v-for="({ id, title }) in tagsItems"
                :key="id"
                closable
                :class="$style.tag"
                @close="deleteItem(id)"
              >
                {{ title }}
              </el-tag>
            </div>

            <Forms
              :type="currentTab"
              :class="$style.form"
              @submit="addItem($event)"
            />
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { Component } from "vue-property-decorator";

import { DocumentsModule } from "@/store";
import { mutateData } from "@/utils/mutateData";

import Forms from "./Forms.vue";

@Component({
  name: "Dictionaries",
  components: {
    Forms,
  },
})
class Dictionaries {
  newItem = ""
  searchQuery = ""

  tabs = {
    publishers:
    {
      label: "Издатели",
      add: DocumentsModule.addPublisher,
      delete: DocumentsModule.deletePublisher,
    },
    authors: {
      label: "Авторы",
      add: DocumentsModule.addAuthor,
      delete: DocumentsModule.deleteAuthor,
    },
    categories: {
      label: "Категории",
      add: DocumentsModule.addCategory,
      delete: DocumentsModule.deleteCategory,
    },
  }

  currentTab = "publishers"

  get tagsItems() {
    if (this.searchQuery) {
      return this[this.currentTab]
        .filter(item => item.title.includes(this.searchQuery));
    }

    return this[this.currentTab];
  }

  get publishers() {
    return DocumentsModule.publishers.map(item => ({
      title: item.name,
      id: item.id,
    }));
  }

  get authors() {
    return DocumentsModule.authors.map(item => ({
      id: item.id,
      title: [item.surname, item.name, item.patronymic].join(" "),
    }));
  }

  get categories() { return DocumentsModule.categories; }

  async deleteItem(id) {
    await this.$confirm(
      "Вы уверены, что хотите удалить?",
      "Подтверждение",
      {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      },
    );

    this.tabs[this.currentTab].delete(id);
  }

  addItem(data) {
    this.tabs[this.currentTab].add(data);
  }
}

export default Dictionaries;
</script>

<style lang="scss" module>
.root {}

.search {
  margin-bottom: 20px;
}

.tagsWrapper {
  margin: -10px -10px 0 0;

  .tag {
    margin: 10px 10px 0 0;
  }
}

.addNew {
  width: 400px;
  display: flex;
  margin-bottom: 20px;
}

.editor {
  display: flex;
  justify-content: space-between;

  .form {
    width: 400px;
    margin-left: 20px;
    flex: none;
  }
}

</style>
