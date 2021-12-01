import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

export const AbsenceExcusesMixin = {
  data() {
    return {
      absenceExcuses: {},
      absenceExcusesAreLoading: true,
    };
  },

  async beforeCreate() {
    this.absenceExcuses = await ChoicesModule.absenceExcuses;
    this.absenceExcusesAreLoading = false;
  },

  methods: {
    absenceExcuseLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.absenceExcuses, value);
    },
  },
};

export const AbsenceStatusesMixin = {
  data() {
    return {
      absenceStatuses: {},
      absenceStatusesAreLoading: true,
    };
  },

  async beforeCreate() {
    this.absenceStatuses = await ChoicesModule.absenceStatuses;
    this.absenceStatusesAreLoading = false;
  },

  methods: {
    absenceStatusLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.absenceStatuses, value);
    },
  },
};
