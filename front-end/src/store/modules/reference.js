import {
  VuexModule,
  Module,
  Mutation,
  Action,
} from "vuex-module-decorators";

import store, { ReferenceModule } from "@/store";

import {
  getMilFaculties,
  getMilGroups,
  getAchievementTypes,
  getPrograms,
  getRooms,
  getSkills,
  addMilGroup,
  deleteMilGroup,
  editMilGroup,
  addAchievementType,
  editAchievementType,
  addMilFaculty,
  editMilFaculty,
  getMilSpecialties,
  addMilSpecialty,
  editMilSpecialty,
  deleteMilSpecialty,
  addProgram,
  editProgram,
  deleteProgram,
  deleteRoom,
  editRoom,
  addRoom,
  deleteSkill,
  editSkill,
  addSkill,
} from "@/api/reference-book";
import {
  getAddRequest,
  getDeleteRequest,
  getEditRequest,
  getFetchRequest,
} from "@/utils/mutators";
import { getError } from "@/utils/message";

@Module({ store, name: "reference", namespaced: true })
class Reference extends VuexModule {
  _milgroups = [];
  _milgroupsLoaded = false;

  _milfaculties = [];
  _milfacultiesLoaded = false;

  _milspecialties = [];
  _milspecialtiesLoaded = false;

  _achievementTypes = [];
  _achievementTypesLoaded = false;

  _programs = [];
  _programsLoaded = false;

  _rooms = [];
  _roomsLoaded = false;

  _skills = [];
  _skillsLoaded = false;

  @Mutation
  SET_IS_LOADED({ field, value }) {
    this[field] = value;
  }

  // MILGROUPS
  @Mutation
  SET_MILGROUPS(payload) {
    this._milgroups = payload;
  }

  @Action
  async fetchMilgroups() {
    return await getFetchRequest(
      getMilGroups,
      data => {
        this.SET_MILGROUPS(data);
        this.SET_IS_LOADED({ field: "_milgroupsLoaded", value: true });
      },
      "взвода",
    ).call(this);
  }

  @Action
  async addMilgroup(newItem) {
    return await getAddRequest(
      addMilGroup,
      this.SET_MILGROUPS,
      "_milgroups",
      "взвод",
    ).call(this, newItem);
  }

  @Action
  async editMilgroup({ id, ...newData }) {
    return await getEditRequest(
      editMilGroup,
      this.SET_MILGROUPS,
      "_milgroups",
      "взвод",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteMilgroup(id) {
    return await getDeleteRequest(
      deleteMilGroup,
      this.SET_MILGROUPS,
      "_milgroups",
      "взвод",
    ).call(this, id);
  }

  get milgroups() {
    if (!this._milgroupsLoaded) {
      ReferenceModule.fetchMilgroups();
    }

    return this._milgroups;
  }

  // MILFACULTIES
  @Mutation
  SET_MILFACULTIES(payload) {
    this._milfaculties = payload;
  }

  @Action
  async fetchMilfaculties() {
    return await getFetchRequest(
      getMilFaculties,
      data => {
        this.SET_MILFACULTIES(data);
        this.SET_IS_LOADED({ field: "_milfacultiesLoaded", value: true });
      },
      "циклов",
    ).call(this);
  }

  @Action
  async addMilfaculty(newItem) {
    return await getAddRequest(
      addMilFaculty,
      this.SET_MILFACULTIES,
      "_milfaculties",
      "цикла",
    ).call(this, newItem);
  }

  @Action
  async editMilfaculty({ id, ...newData }) {
    return await getEditRequest(
      editMilFaculty,
      this.SET_MILFACULTIES,
      "_milfaculties",
      "цикла",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteMilfaculty(id) {
    return await getDeleteRequest(
      deleteMilGroup,
      this.SET_MILFACULTIES,
      "_milfaculties",
      "цикла",
    ).call(this, id);
  }

  get milfaculties() {
    if (!this._milfacultiesLoaded) {
      ReferenceModule.fetchMilfaculties();
    }

    return this._milfaculties;
  }

  // milspecialties
  @Mutation
  SET_MILSPECIALTIES(payload) {
    this._milspecialties = payload;
  }

  @Action
  async fetchMilSpecialties() {
    return await getFetchRequest(
      getMilSpecialties,
      data => {
        this.SET_MILSPECIALTIES(data);
        this.SET_IS_LOADED({ field: "_milspecialtiesLoaded", value: true });
      },
      "воинских специальностей",
    ).call(this);
  }

  @Action
  async addMilSpecialty(newItem) {
    return await getAddRequest(
      addMilSpecialty,
      this.SET_MILSPECIALTIES,
      "_milspecialties",
      "воинскую специальность",
    ).call(this, newItem);
  }

  @Action
  async editMilSpecialty({ id, ...newData }) {
    return await getEditRequest(
      editMilSpecialty,
      this.SET_MILSPECIALTIES,
      "_milspecialties",
      "воинскую специальность",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteMilSpecialty(id) {
    return await getDeleteRequest(
      deleteMilSpecialty,
      this.SET_MILSPECIALTIES,
      "_milspecialties",
      "воинскую специальность",
    ).call(this, id);
  }

  get milspecialties() {
    if (!this._milspecialtiesLoaded) {
      ReferenceModule.fetchMilSpecialties();
    }

    return this._milspecialties;
  }

  // ACHIEVEMENT TYPES
  @Mutation
  SET_ACHIEVEMENT_TYPES(payload) {
    this._achievementTypes = payload;
  }

  @Action
  async fetchAchievementTypes() {
    return await getFetchRequest(
      getAchievementTypes,
      data => {
        this.SET_ACHIEVEMENT_TYPES(data);
        this.SET_IS_LOADED({ field: "_achievementTypesLoaded", value: true });
      },
      "типов достижений",
    ).call(this);
  }

  @Action
  async addAchievementType(newItem) {
    return await getAddRequest(
      addAchievementType,
      this.SET_ACHIEVEMENT_TYPES,
      "_achievementTypes",
      "тип достижения",
    ).call(this, newItem);
  }

  @Action
  async editAchievementType({ id, ...newData }) {
    return await getEditRequest(
      editAchievementType,
      this.SET_ACHIEVEMENT_TYPES,
      "_achievementTypes",
      "тип достижения",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteAchievementType(id) {
    return await getDeleteRequest(
      deleteMilGroup,
      this.SET_ACHIEVEMENT_TYPES,
      "_achievementTypes",
      "тип достижения",
    ).call(this, id);
  }

  get achievementTypes() {
    if (!this._achievementTypesLoaded) {
      ReferenceModule.fetchAchievementTypes();
    }

    return this._achievementTypes;
  }

  // PROGRAMS
  @Mutation
  SET_PROGRAMS(payload) {
    this._programs = payload;
  }

  @Action
  async fetchPrograms() {
    return await getFetchRequest(
      getPrograms,
      data => {
        this.SET_PROGRAMS(data);
        this.SET_IS_LOADED({ field: "_programsLoaded", value: true });
      },
      "образовательных программ",
    ).call(this);
  }

  @Action
  async addProgram(newItem) {
    return await getAddRequest(
      addProgram,
      this.SET_PROGRAMS,
      "_programs",
      "образовательную программу",
    ).call(this, newItem);
  }

  @Action
  async editProgram({ id, ...newData }) {
    return await getEditRequest(
      editProgram,
      this.SET_PROGRAMS,
      "_programs",
      "образовательную программу",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteProgram(id) {
    return await getDeleteRequest(
      deleteProgram,
      this.SET_PROGRAMS,
      "_programs",
      "образовательную программу",
    ).call(this, id);
  }

  get programs() {
    if (!this._programsLoaded) {
      ReferenceModule.fetchPrograms();
    }

    return this._programs;
  }

  // ROOMS
  @Mutation
  SET_ROOMS(payload) {
    this._rooms = payload;
  }

  @Action
  async fetchRooms() {
    return await getFetchRequest(
      getRooms,
      data => {
        data.sort((a, b) => {
          const titleA = a.title;
          const titleB = b.title;

          const numA = Number(titleA);
          const numB = Number(titleB);

          const isNumA = !Number.isNaN(numA);
          const isNumB = !Number.isNaN(numB);

          if (isNumA && isNumB) {
            return numA - numB;
          }

          if (isNumA) {
            return -1;
          }

          if (isNumB) {
            return 1;
          }

          return titleA.localeCompare(titleB);
        });
        this.SET_ROOMS(data);
        this.SET_IS_LOADED({ field: "_roomsLoaded", value: true });
      },
      "аудиторий",
    ).call(this);
  }

  @Action
  async addRoom(newItem) {
    return await getAddRequest(
      addRoom,
      this.SET_ROOMS,
      "_rooms",
      "аудиторию",
    ).call(this, newItem);
  }

  @Action
  async editRoom({ id, ...newData }) {
    return await getEditRequest(
      editRoom,
      this.SET_ROOMS,
      "_rooms",
      "аудиторию",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteRoom(id) {
    return await getDeleteRequest(
      deleteRoom,
      this.SET_ROOMS,
      "_rooms",
      "аудиторию",
    ).call(this, id);
  }

  get rooms() {
    if (!this._roomsLoaded) {
      ReferenceModule.fetchRooms();
    }

    return this._rooms;
  }

  // SKILLS
  @Mutation
  SET_SKILLS(payload) {
    this._skills = payload;
  }

  @Action
  async fetchSkills() {
    return await getFetchRequest(
      getSkills,
      data => {
        this.SET_SKILLS(data);
        this.SET_IS_LOADED({ field: "_skillsLoaded", value: true });
      },
      "умений",
    ).call(this);
  }

  @Action
  async addSkill(newItem) {
    return await getAddRequest(
      addSkill,
      this.SET_SKILLS,
      "_skills",
      "умение",
    ).call(this, newItem);
  }

  @Action
  async editSkill({ id, ...newData }) {
    return await getEditRequest(
      editSkill,
      this.SET_SKILLS,
      "_skills",
      "умение",
    ).call(this, { id, ...newData });
  }

  @Action
  async deleteSkill(id) {
    return await getDeleteRequest(
      deleteSkill,
      this.SET_SKILLS,
      "_skills",
      "умение",
    ).call(this, id);
  }

  get skills() {
    if (!this._skillsLoaded) {
      ReferenceModule.fetchSkills();
    }

    return this._skills;
  }
}

export default Reference;
