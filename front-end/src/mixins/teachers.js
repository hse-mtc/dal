import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

export const TeacherPostsMixin = {
  data() {
    return {
      teacherPosts: {},
      teacherPostsAreLoading: true,
    };
  },

  async beforeCreate() {
    this.teacherPosts = await ChoicesModule.teacherPosts;
    this.teacherPostsAreLoading = false;
  },

  methods: {
    teacherPostLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.teacherPosts, value);
    },
  },
};

export const TeacherRanksMixin = {
  data() {
    return {
      teacherRanks: {},
      teacherRanksAreLoading: true,
    };
  },

  async beforeCreate() {
    this.teacherRanks = await ChoicesModule.teacherRanks;
    this.teacherRanksAreLoading = false;
  },

  methods: {
    teacherRankLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.teacherRanks, value);
    },
  },
};
