import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

export const PunishmentTypesMixin = {
  data() {
    return {
      punishmentTypes: {},
      punishmentTypesAreLoading: true,
    };
  },

  async beforeCreate() {
    this.punishmentTypes = await ChoicesModule.punishmentTypes;
    this.punishmentTypesAreLoading = false;
  },

  methods: {
    punishmentTypeLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.punishmentTypes, value);
    },
  },
};
