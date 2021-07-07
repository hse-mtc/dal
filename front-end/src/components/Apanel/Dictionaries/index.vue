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
            <div
              v-if="!editingItemId"
              :class="$style.tagsWrapper"
            >
              <Tag
                v-for="({ id, title }) in tagsItems"
                :id="id"
                :key="id"
                :title="title"
                :class="$style.tag"
                @delete="deleteItem(id)"
                @edit="startEdit(id)"
              >
                {{ title }}
              </Tag>
            </div>

            <Forms
              :is-edit="!!editingItemId"
              :init-state="modalData"
              :type="currentTab"
              :class="$style.form"
              @submit="addItem($event)"
              @change="editItem"
              @cancel="stopEdit"
            />
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { Component, Watch } from "vue-property-decorator";
import _omit from "lodash/omit";

import { PapersModule } from "@/store";

import ModalWindow from "@/components/ModalWindow/ModalWindow.vue";
import Forms from "./Forms.vue";
import Tag from "./Tag.vue";

@Component({
  name: "Dictionaries",
  components: {
    Forms,
    ModalWindow,
    Tag,
  },
})
class Dictionaries {
  newItem = ""
  searchQuery = ""
  editingItemId = null
  modalData = {}

  tabs = {
    publishers:
    {
      label: "Издатели",
      mapFunc: item => ({ title: item.name, id: item.id }),
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
      add: PapersModule.addAuthor,
      delete: PapersModule.deleteAuthor,
      edit: PapersModule.editAuthors,
    },
    categories: {
      label: "Категории",
      add: PapersModule.addCategory,
      delete: PapersModule.deleteCategory,
      edit: PapersModule.editCategories,
    },
  }

  currentTab = "publishers"

  get tagsItems() {
    const { mapFunc } = this.tabs[this.currentTab];
    const data = (mapFunc
      ? this[this.currentTab].map(mapFunc)
      : this[this.currentTab])
      .sort((left, right) => (left.title > right.title ? 1 : -1));

    if (this.searchQuery) {
      const query = this.searchQuery.toLowerCase();
      return data
        .filter(item => item.title.toLowerCase().includes(query));
    }

    return data;
  }

  get publishers() { return PapersModule.publishers; }

  get authors() { return PapersModule.authors; }

  get categories() { return PapersModule.categories; }

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

  startEdit(id) {
    this.editingItemId = id;
    this.modalData = _omit(
      this[this.currentTab].find(item => item.id === id),
      ["id"],
    );
  }

  stopEdit() {
    this.editingItemId = null;
    this.modalData = {};
  }

  async editItem(data) {
    const { edit } = this.tabs[this.currentTab];

    const res = await edit({
      id: this.editingItemId,
      ...data,
    });

    if (res) {
      this.stopEdit();
    }
  }

  addItem(data) {
    this.tabs[this.currentTab].add(data);
  }

  @Watch("currentTab")
  onCurrentTabChange() {
    this.editingItemId = null;
    this.modalData = {};
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
