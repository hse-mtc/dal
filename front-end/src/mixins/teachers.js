import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

export const teacherPostMixin = {
  data() {
    return {
      teacherPosts: {},
    };
  },

  async beforeCreate() {
    this.teacherPosts = await ChoicesModule.teacherPosts;
  },

  methods: {
    teacherPostLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.teacherPosts, value);
    },
  },
};

export const teacherRankMixin = {
  data() {
    return {
      teacherRanks: {},
    };
  },

  async beforeCreate() {
    this.teacherRanks = await ChoicesModule.teacherRanks;
  },

  methods: {
    teacherRankLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.teacherRanks, value);
    },
  },
};
