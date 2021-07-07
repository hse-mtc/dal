import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";
import { Message } from "element-ui";

import store, { PapersModule } from "@/store";
import {
  addPaperCategories,
  deletePaperCategory,
  editPaperCategories,
  getPaperCategories,
} from "@/api/paper_categories";
import {
  addAuthor,
  deleteAuthor,
  editAuthors,
  getAuthors,
} from "@/api/authors";
import {
  addPublisher,
  deletePublisher,
  editPublisher,
  getPublishers,
} from "@/api/publishers";

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
      Message({
        type: "error",
        message: "Не удалось загрузить издателей",
      });
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
      Message({
        type: "error",
        message: "Не удалось удалить издателя",
      });

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
      Message({
        type: "error",
        message: "Не удалось добавить издателя",
      });

      return false;
    }
  }

  @Action
  async editPublisher({ id, ...newData }) {
    try {
      const { data } = await editPublisher(id, newData);

      const index = this._publishersList.findIndex(item => item.id === id);
      const newArray = [...this._publishersList];
      newArray[index] = data;

      this.setPublishers(newArray);

      return true;
    } catch (e) {
      console.error("Не удалось изменить издателя:", e);
      Message({
        type: "error",
        message: "Не удалось изменить издателя",
      });

      return false;
    }
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
      Message({
        type: "error",
        message: "Не удалось загрузить авторов",
      });
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
      Message({
        type: "error",
        message: "Не удалось удалить автора",
      });

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
      Message({
        type: "error",
        message: "Не удалось добавить автора",
      });

      return false;
    }
  }

  @Action
  async editAuthors({ id, ...newData }) {
    try {
      const { data } = await editAuthors(id, newData);

      const index = this._authorsList.findIndex(item => item.id === id);
      const newArray = [...this._authorsList];
      newArray[index] = data;
      this.setAuthors(newArray);

      return true;
    } catch (e) {
      console.error("Не удалось изменить автора:", e);
      Message({
        type: "error",
        message: "Не удалось изменить автора",
      });

      return false;
    }
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
      Message({
        type: "error",
        message: "Не удалось загрузить категорию",
      });
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
      Message({
        type: "error",
        message: "Не удалось удалить категорию",
      });

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
      Message({
        type: "error",
        message: "Не удалось добавить категорию",
      });

      return false;
    }
  }

  @Action
  async editCategories({ id, ...newData }) {
    try {
      const { data } = await editPaperCategories(id, newData);
      const index = this._categoriesList.findIndex(item => item.id === id);
      const newArray = [...this._categoriesList];
      newArray[index] = data;
      this.setCategories(newArray);

      return true;
    } catch (e) {
      console.error("Не удалось изменить категорию:", e);
      Message({
        type: "error",
        message: "Не удалось изменить категорию",
      });

      return false;
    }
  }

  get categories() {
    if (!this._categoriesLoaded) {
      PapersModule.fetchCategories();
    }

    return this._categoriesList;
  }
}

export default Papers;
