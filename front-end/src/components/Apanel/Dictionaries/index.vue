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
          <template v-if="currentTab === field">
            <TabsEditor
              v-if="editorsTypes[currentTab] === 'tags'"
              :type="currentTab"
              :tags="tagsItems"
              :editing-item="editingData"
              @addItem="onAddItem"
              @startEdit="onStartEdit"
              @abortEdit="onAbortEdit"
              @submitEdit="onSubmitEdit"
              @delete="onDelete"
            />

            <TableEditor
              v-else
              :type="currentTab"
              :data="tagsItems"
              @addItem="onAddItem"
              @startEdit="onStartEdit"
              @abortEdit="onAbortEdit"
              @submitEdit="onSubmitEdit"
              @delete="onDelete"
            />
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { Component, Watch } from "vue-property-decorator";
import _omit from "lodash/omit";

import { PapersModule, ReferenceModule } from "@/store";

import TabsEditor from "./TagsEditor.vue";
import TableEditor from "./TableEditor.vue";

const weekdays = {
  0: "Понедельник",
  1: "Вторник",
  2: "Среда",
  3: "Четверг",
  4: "Пятница",
  5: "Суббота",
  6: "Воскресенье",
};

@Component({
  name: "Dictionaries",
  components: {
    TabsEditor,
    TableEditor,
  },
})
class Dictionaries {
  newItem = ""
  searchQuery = ""
  editingItemId = null
  editingData = null

  editorsTypes = {
    publishers: "tags",
    authors: "tags",
    categories: "tags",
  }

  tabs = {
    publishers:
    {
      label: "Издатели",
      mapFunc: item => ({ title: item.name, id: item.id }),
      sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
      filterFunc: (item, query) => item.title.toLowerCase().includes(query),
      add: PapersModule.addPublisher,
      delete: PapersModule.deletePublisher,
      edit: PapersModule.editPublisher,
    },
    authors: {
      label: "Авторы",
      mapFunc: item => ({
        id: item.id,
        title: [item.surname, item.name, item.patronymic].filter(Boolean).join(" "),
      }),
      sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
      filterFunc: (item, query) => item.title.toLowerCase().includes(query),
      add: PapersModule.addAuthor,
      delete: PapersModule.deleteAuthor,
      edit: PapersModule.editAuthors,
    },
    categories: {
      label: "Категории",
      sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
      filterFunc: (item, query) => item.title.toLowerCase().includes(query),
      add: PapersModule.addCategory,
      delete: PapersModule.deleteCategory,
      edit: PapersModule.editCategories,
    },
    milgroups: {
      label: "Взвода",
      sortFunc: (left, right) => (left.milgroup > right.milgroup ? 1 : -1),
      filterFunc: (item, query) => {
        const stringItem = `${item.milgroup} ${item.milfaculty} ${weekdays[item.weekday]}`
          .toLowerCase();
        return query.split(" ")
          .reduce((memo, word) => memo && (word && stringItem.includes(word)), true);
      },
      add: ReferenceModule.addMilgroup,
      delete: ReferenceModule.deleteMilgroup,
      edit: ReferenceModule.editMilgroup,
    },
  }

  currentTab = "publishers"

  get tagsItems() {
    const { mapFunc, sortFunc, filterFunc } = this.tabs[this.currentTab];
    const data = (mapFunc
      ? this[this.currentTab].map(mapFunc)
      : this[this.currentTab])
      .sort(sortFunc);

    if (this.searchQuery) {
      const query = this.searchQuery.toLowerCase();
      return data.filter(item => filterFunc(item, query));
    }

    return data;
  }

  get publishers() { return PapersModule.publishers; }
  get authors() { return PapersModule.authors; }
  get categories() { return PapersModule.categories; }
  get milgroups() { return ReferenceModule.milgroups; }

  async onDelete(id) {
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

  onStartEdit(id) {
    this.editingItemId = id;
    this.editingData = _omit(
      this[this.currentTab].find(item => item.id === id),
      ["id"],
    );
  }

  onAbortEdit() {
    this.editingItemId = null;
    this.editingData = null;
  }

  async onSubmitEdit(data) {
    const { edit } = this.tabs[this.currentTab];

    const res = await edit({
      id: this.editingItemId,
      ...data,
    });

    if (res) {
      this.onAbortEdit();
    }
  }

  onAddItem(data) {
    this.tabs[this.currentTab].add(data);
  }

  @Watch("currentTab")
  onCurrentTabChange() {
    this.editingItemId = null;
    this.editingData = null;
  }
}

export default Dictionaries;
</script>

<style lang="scss" module>
.root {}

.search {
  margin-bottom: 20px;
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
