import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store, { DocumentsModule } from "@/store";
import { addPaperCategories, deletePaperCategory, getPaperCategories } from "@/api/paper_categories";
import { addAuthor, deleteAuthor, getAuthors } from "@/api/authors";
import { addPublisher, deletePublisher, getPublishers } from "@/api/publishers";

@Module({ store, name: "documents", namespaced: true })
class Documents extends VuexModule {
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

  @Action({ commit: "SET_IS_LOADED" })
  setIsLoaded({ field, value }) {
    return { field, value };
  }

  @Mutation
  SET_PUBLISHERS(publishers) {
    this._publishersList = publishers;
  }

  @Action({ commit: "SET_PUBLISHERS" })
  setPublishers(publishers) {
    return publishers;
  }

  @Action
  async fetchPublishers() {
    try {
      const { data } = await getPublishers();
      this.setPublishers(data);
      this.SET_IS_LOADED({ field: "_publishersLoaded", value: true });
    } catch (e) {
      console.error("Не удалось загрузить издателей", e);
    }
  }

  @Action
  async deletePublisher(id) {
    try {
      await deletePublisher(id);

      this.setPublishers(this._publishersList.filter(item => item.id !== id));

      return true;
    } catch (e) {
      console.error("Не удалось удалить издателя:", e);

      return false;
    }
  }

  @Action
  async addPublisher({ name }) {
    try {
      const { data } = await addPublisher(name);

      this.setPublishers([...this._publishersList, data]);

      return true;
    } catch (e) {
      console.error("Не удалось добавить издателя:", e);

      return false;
    }
  }

  get publishers() {
    if (!this._publishersLoaded) {
      DocumentsModule.fetchPublishers();
    }

    return this._publishersList;
  }

  @Mutation
  SET_AUTHORS(authors) {
    this._authorsList = authors;
  }

  @Action({ commit: "SET_AUTHORS" })
  setAuthors(authors) {
    return authors;
  }

  @Action
  async fetchAuthors() {
    try {
      const { data } = await getAuthors();
      this.setAuthors(data);
      this.SET_IS_LOADED({ field: "_authorsLoaded", value: true });
    } catch (e) {
      console.error("Не удалось загрузить авторов", e);
    }
  }

  @Action
  async deleteAuthor(id) {
    try {
      await deleteAuthor(id);

      this.setAuthors(this._authorsList.filter(item => item.id !== id));

      return true;
    } catch (e) {
      console.error("Не удалось удалить автора:", e);

      return false;
    }
  }

  @Action
  async addAuthor(info) {
    try {
      const { data } = await addAuthor(info);

      this.setAuthors([...this._authorsList, data]);

      return true;
    } catch (e) {
      console.error("Не удалось добавить автора:", e);

      return false;
    }
  }

  get authors() {
    if (!this._authorsLoaded) {
      DocumentsModule.fetchAuthors();
    }

    return this._authorsList;
  }

  @Mutation
  SET_CATEGORIES(payload) {
    this._categoriesList = payload;
  }

  @Action({ commit: "SET_CATEGORIES" })
  setCategories(categories) {
    return categories;
  }

  @Action
  async fetchCategories() {
    try {
      const { data } = await getPaperCategories();
      this.setCategories(data);
      this.SET_IS_LOADED({ field: "_categoriesLoaded", value: true });
    } catch (e) {
      console.error("Не удалось загрузить категорию", e);
    }
  }

  @Action
  async deleteCategory(id) {
    try {
      await deletePaperCategory(id);

      this.setCategories(this._categoriesList.filter(item => item.id !== id));

      return true;
    } catch (e) {
      console.error("Не удалось удалить категорию:", e);

      return false;
    }
  }

  @Action
  async addCategory(info) {
    try {
      const { data } = await addPaperCategories(info);

      this.setCategories([...this._categoriesList, data]);

      return true;
    } catch (e) {
      console.error("Не удалось добавить категорию:", e);

      return false;
    }
  }

  get categories() {
    if (!this._categoriesLoaded) {
      DocumentsModule.fetchCategories();
    }

    return this._categoriesList;
  }
}

export default Documents;
