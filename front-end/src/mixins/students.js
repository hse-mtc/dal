import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

export const studentStatusesMixin = {
  data() {
    return {
      studentStatuses: {},
    };
  },

  async beforeCreate() {
    this.studentStatuses = await ChoicesModule.studentStatuses;
  },

  methods: {
    studentStatusLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.studentStatuses, value);
    },
  },
};
