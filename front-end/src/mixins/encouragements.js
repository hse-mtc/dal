import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

export const EncouragementTypesMixin = {
  data() {
    return {
      encouragementTypes: {},
      encouragementTypesAreLoading: true,
    };
  },

  async beforeCreate() {
    this.encouragementTypes = await ChoicesModule.encouragementTypes;
    this.encouragementTypesAreLoading = false;
  },

  methods: {
    encouragementTypeLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.encouragementTypes, value);
    },
  },
};
