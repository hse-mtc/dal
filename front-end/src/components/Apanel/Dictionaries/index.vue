<template>
  <div>
    <el-input
      v-model="searchQuery"
      placeholder="Поиск"
      prefix-icon="el-icon-search"
      clearable
      :class="$style.search"
    />

    <div>
      <el-tabs
        v-model="currentTab"
        tab-position="left"
      >
        <el-tab-pane
          v-for="({ label }, field) in tabs"
          :key="field"
          :name="field"
          :label="label"
        >
          <AZGuard :permissions="[field + '.patch.all']">
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
                v-else-if="editorsTypes[currentTab] === 'table'"
                :type="currentTab"
                :data="tagsItems"
                @addItem="onAddItem"
                @submitEdit="onTableEdit"
                @delete="onDelete"
              />
            </template>
          </AZGuard>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { Component, Vue, Watch } from "vue-property-decorator";
import _omit from "lodash/omit";

import { PapersModule, ReferenceModule } from "@/store";

import { hasPermission } from "@/utils/permissions";
import { WEEKDAYS } from "@/utils/enums";
import TabsEditor from "./TagsEditor.vue";
import TableEditor from "./TableEditor.vue";

@Component({
  name: "Dictionaries",
  components: {
    TabsEditor,
    TableEditor,
  },
})
class Dictionaries extends Vue {
  newItem = ""
  searchQuery = ""
  editingItemId = null
  editingData = null

  editorsTypes = {
    publishers: "tags",
    authors: "tags",
    categories: "tags",
    achievementTypes: "tags",
    milfaculties: "tags",
    rooms: "tags",
    skills: "tags",
    milgroups: "table",
    milspecialties: "table",
    programs: "table",
  }

  tabs = {}

  // programs: {
  //   label: "Программы",
  //   sortFunc: (left, right) => (left.code > right.code ? 1 : -1),
  //   filterFunc: (item, query) => {
  //     const stringItem = `${item.code} ${item.title} ${item.faculty}`.toLowerCase();
  //     return query.split(" ")
  //       .reduce((memo, word) => memo && (!word || stringItem.includes(word)), true);
  //   },
  //   add: ReferenceModule.addProgram,
  //   delete: ReferenceModule.deleteProgram,
  //   edit: ReferenceModule.editProgram,
  // },

  currentTab = ""

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
  get milfaculties() { return ReferenceModule.milfaculties; }
  get achievementTypes() { return ReferenceModule.achievementTypes; }
  get milspecialties() { return ReferenceModule.milspecialties; }
  get programs() { return ReferenceModule.programs; }
  get rooms() { return ReferenceModule.rooms; }
  get skills() { return ReferenceModule.skills; }

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

    if (res && this.editorsTypes[this.currentTab] === "tags") {
      this.onAbortEdit();
    }
  }

  onTableEdit(data) {
    this.onStartEdit(data.id);
    this.onSubmitEdit(data);
    this.onAbortEdit();
  }

  onAddItem(data) {
    this.tabs[this.currentTab].add(data);
  }

  @Watch("currentTab")
  onCurrentTabChange() {
    this.editingItemId = null;
    this.editingData = null;
  }

  created() {
    if (hasPermission(["publishers.patch.all"])) {
      this.tabs.publishers = {
        label: "Издатели",
        mapFunc: item => ({ title: item.name, id: item.id }),
        sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
        filterFunc: (item, query) => item.title.toLowerCase().includes(query),
        add: PapersModule.addPublisher,
        delete: PapersModule.deletePublisher,
        edit: PapersModule.editPublisher,
      };
    }
    if (hasPermission(["authors.patch.all"])) {
      this.tabs.authors = {
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
      };
    }
    if (hasPermission(["categories.patch.all"])) {
      this.tabs.categories = {
        label: "Категории",
        sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
        filterFunc: (item, query) => item.title.toLowerCase().includes(query),
        add: PapersModule.addCategory,
        delete: PapersModule.deleteCategory,
        edit: PapersModule.editCategories,
      };
    }
    if (hasPermission(["milgroups.patch.all"])) {
      this.tabs.milgroups = {
        label: "Взвода",
        mapFunc: item => ({
          ...item,
          milfaculty: item.milfaculty.id,
          milspecialty: item.milspecialty ? item.milspecialty.id : 0,
        }),
        sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
        filterFunc: (item, query) => {
          const stringItem = `${item.title} ${
            this.milfaculties.find(milfaculty => milfaculty.id === item.milfaculty).title
          } ${WEEKDAYS[item.weekday]}`
            .toLowerCase();
          return query.split(" ")
            .reduce((memo, word) => memo && (!word || stringItem.includes(word)), true);
        },
        add: ReferenceModule.addMilgroup,
        delete: ReferenceModule.deleteMilgroup,
        edit: ReferenceModule.editMilgroup,
      };
    }
    if (hasPermission(["achievementTypes.patch.all"])) {
      this.tabs.achievementTypes = {
        label: "Достижения",
        sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
        filterFunc: (item, query) => item.title.toLowerCase().includes(query),
        add: ReferenceModule.addAchievementType,
        delete: ReferenceModule.deleteAchievementType,
        edit: ReferenceModule.editAchievementType,
      };
    }
    if (hasPermission(["milfaculties.patch.all"])) {
      this.tabs.milfaculties = {
        label: "Циклы",
        mapFunc: item => ({
          id: item.id,
          title: item.title + (item.abbreviation ? ` (${item.abbreviation})` : ""),
        }),
        sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
        filterFunc: (item, query) => item.title.toLowerCase().includes(query),
        add: ReferenceModule.addMilfaculty,
        delete: ReferenceModule.deleteMilfaculty,
        edit: ReferenceModule.editMilfaculty,
      };
    }
    if (hasPermission(["milspecialties.patch.all"])) {
      this.tabs.milspecialties = {
        label: "Направления",
        sortFunc: (left, right) => (left.code > right.code ? 1 : -1),
        filterFunc: (item, query) => {
          const stringItem = `${item.code} ${item.title}`.toLowerCase();
          return query.split(" ")
            .reduce((memo, word) => memo && (!word || stringItem.includes(word)), true);
        },
        add: ReferenceModule.addMilSpecialty,
        delete: ReferenceModule.deleteMilSpecialty,
        edit: ReferenceModule.editMilSpecialty,
      };
    }
    if (hasPermission(["rooms.patch.all"])) {
      this.tabs.rooms = {
        label: "Аудитории",
        sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
        filterFunc: (item, query) => item.title.toLowerCase().includes(query),
        add: ReferenceModule.addRoom,
        delete: ReferenceModule.deleteRoom,
        edit: ReferenceModule.editRoom,
      };
    }
    if (hasPermission(["skills.patch.all"])) {
      this.tabs.skills = {
        label: "Умения",
        sortFunc: (left, right) => (left.title > right.title ? 1 : -1),
        filterFunc: (item, query) => item.title.toLowerCase().includes(query),
        add: ReferenceModule.addSkill,
        delete: ReferenceModule.deleteSkill,
        edit: ReferenceModule.editSkill,
      };
    }
    // eslint-disable-next-line prefer-destructuring
    this.currentTab = Object.keys(this.tabs)[0];
  }
}
export default Dictionaries;
</script>

<style lang="scss" module>
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

.tabs {
  width: 200px;
}

</style>
