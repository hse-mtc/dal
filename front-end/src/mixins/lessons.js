import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

export const LessonTypesMixin = {
  data() {
    return {
      lessonTypes: {},
      lessonTypesLoading: true,
    };
  },

  async beforeCreate() {
    this.lessonTypes = await ChoicesModule.lessonTypes;
    this.lessonTypesAreLoading = false;
  },

  methods: {
    lessonTypeLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.lessonTypes, value);
    },
  },
};
