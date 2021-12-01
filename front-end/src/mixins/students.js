import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

export const StudentStatusesMixin = {
  data() {
    return {
      studentStatuses: {},
      studentStatusesAreLoading: true,
    };
  },

  async beforeCreate() {
    this.studentStatuses = await ChoicesModule.studentStatuses;
    this.studentStatusesAreLoading = false;
  },

  methods: {
    studentStatusLabelFromValue(value) {
      return defaultChoiceLabelFromValue(this.studentStatuses, value);
    },
  },
};

export const StudentPostsMixin = {
  data() {
    return {
      studentPosts: {},
      studentPostsAreLoading: true,
    };
  },

  async beforeCreate() {
    this.studentPosts = await ChoicesModule.studentPosts;
    this.studentPostsAreLoading = false;
  },

  methods: {
    studentPostLabelFromValueOrDefault(value, defaultLabel) {
      return defaultChoiceLabelFromValue(this.studentPosts, value, defaultLabel);
    },
  },
};
