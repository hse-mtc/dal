import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store, { PapersModule } from "@/store";
import {
  addPaperCategory,
  deletePaperCategory,
  editPaperCategory,
  getPaperCategories,
} from "@/api/paper_categories";
import {
  addAuthor,
  deleteAuthor,
  editAuthor,
  getAuthors,
} from "@/api/authors";
import {
  addPublisher,
  deletePublisher,
  editPublisher,
  getPublishers,
} from "@/api/publishers";
import {
  getAddRequest, getDeleteRequest, getEditRequest, getFetchRequest,
} from "@/utils/mutators";

@Module({ store, name: "papers", namespaced: true })
class Papers extends VuexModule {
  _publishersList = []
  _publishersLoaded = false
  _authorsList = []
  _authorsLoaded = false
  _categoriesList = []
  _categoriesLoaded = false

  @Mutation
  SET_IS_LOADED({ field, value }) {
    this[field] = value;
  }

  @Mutation
  SET_PUBLISHERS(publishers) {
    this._publishersList = publishers;
  }

  @Action
  async fetchPublishers() {
    return await getFetchRequest(
      getPublishers,
      data => {
        this.SET_PUBLISHERS(data);
        this.SET_IS_LOADED({ field: "_publishersLoaded", value: true });
      },
      "издателей",
    ).call(this);
  }

  @Action
  async addPublisher(newItem) {
    return await getAddRequest(
      addPublisher,
      this.SET_PUBLISHERS,
      "_publishersList",
      "издателя",
    ).call(this, newItem);
  }

  @Action
  async editPublisher({ id, ...newData }) {
    return await getEditRequest(
      editPublisher,
      this.SET_PUBLISHERS,
      "_publishersList",
      "издателя",
    ).call(this, { id, ...newData });
  }

  @Action
  async deletePublisher(id) {
    return await getDeleteRequest(
      deletePublisher,
      this.SET_PUBLISHERS,
      "_publishersList",
      "издателя",
    ).call(this, id);
  }

  get publishers() {
    if (!this._publishersLoaded) {
      PapersModule.fetchPublishers();
    }

    return this._publishersList;
  }

  @Mutation
  SET_AUTHORS(authors) {
    this._authorsList = authors;
  }

  @Action
  async fetchAuthors() {
    return await getFetchRequest(
      getAuthors,
      data => {
        this.SET_AUTHORS(data);
        this.SET_IS_LOADED({ field: "_authorsLoaded", value: true });
      },
      "авторов",
    ).call(this);
  }

  @Action
  async addAuthor(newItem) {
    return await getAddRequest(
      addAuthor,
      this.SET_AUTHORS,
      "_authorsList",
      "автора",
    ).call(this, newItem);
  }

  @Action
  async editAuthors({ id, ...newData }) {
    return await getEditRequest(
      editAuthor,
      this.SET_AUTHORS,
      "_authorsList",
      "автора",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteAuthor(id) {
    return await getDeleteRequest(
      deleteAuthor,
      this.SET_AUTHORS,
      "_authorsList",
      "автора",
    ).call(this, id);
  }

  get authors() {
    if (!this._authorsLoaded) {
      PapersModule.fetchAuthors();
    }

    return this._authorsList;
  }

  @Mutation
  SET_CATEGORIES(payload) {
    this._categoriesList = payload;
  }

  @Action
  async fetchCategories() {
    return await getFetchRequest(
      getPaperCategories,
      data => {
        const mapped = data.map(cat => ({
          ...cat,
          filters: Object.prototype.hasOwnProperty.call(cat, "filters")
            ? cat.filters
            : cat.additional_schema,
        }));
        this.SET_CATEGORIES([...mapped, { title: "Корзина", id: "bin" }]);
        this.SET_IS_LOADED({ field: "_categoriesLoaded", value: true });
      },
      "категории",
    ).call(this);
  }

  @Action
  async reloadCategories() {
    try {
      const { data } = await getPaperCategories();
      const mapped = data.map(cat => ({
        ...cat,
        filters: Object.prototype.hasOwnProperty.call(cat, "filters")
          ? cat.filters
          : cat.additional_schema,
      }));
      this.SET_CATEGORIES([...mapped, { title: "Корзина", id: "bin" }]);
      this.SET_IS_LOADED({ field: "_categoriesLoaded", value: true });
      return true;
    } catch (e) {
      console.error("Не удалось перезагрузить категории:", e);
      return false;
    }
  }

  @Action
  async addCategory(newItem) {
    const payload = { ...newItem };

    if (payload.filters) {
      payload.additional_schema = payload.filters;
      delete payload.filters;
    }

    return await getAddRequest(
      addPaperCategory,
      this.SET_CATEGORIES,
      "_categoriesList",
      "категорию",
    ).call(this, payload);
  }

@Action
  async editCategories({ id, ...newData }) {
    const payload = { id, ...newData };

    if (payload.filters) {
      payload.additional_schema = payload.filters;
      delete payload.filters;
    }

    return await getEditRequest(
      editPaperCategory,
      this.SET_CATEGORIES,
      "_categoriesList",
      "категорию",
    ).call(this, payload);
  }

  @Action
async deleteCategory(id) {
  return await getDeleteRequest(
    deletePaperCategory,
    this.SET_CATEGORIES,
    "_categoriesList",
    "категорию",
  ).call(this, id);
}

  get categories() {
    if (!this._categoriesLoaded) {
      PapersModule.fetchCategories();
    }

    return this._categoriesList;
  }
}

export default Papers;
