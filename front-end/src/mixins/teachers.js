import { ReferenceModule } from "@/store";

export const teacherPostMixin = {
  computed: {
    teacherPosts() {
      return ReferenceModule.teacherPosts;
    },
  },

  methods: {
    displayTeacherPost(value) {
      const filtered = Object
        .values(this.teacherPosts)
        .filter(post => post.value === value);

      if (filtered.length === 1) {
        return filtered[0].label;
      }
      return value;
    },
  },
};

export const teacherRankMixin = {
  computed: {
    teacherRanks() {
      return ReferenceModule.teacherRanks;
    },
  },

  methods: {
    displayTeacherRank(value) {
      const filtered = Object
        .values(this.teacherRanks)
        .filter(rank => rank.value === value);

      if (filtered.length === 1) {
        return filtered[0].label;
      }
      return value;
    },
  },
};
