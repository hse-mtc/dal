import { ReferenceModule } from "@/store";

export const studentStatusMixin = {
  computed: {
    studentStatuses() {
      return ReferenceModule.studentStatuses;
    },
  },

  methods: {
    displayStudentStatus(value) {
      const filtered = Object
        .values(this.studentStatuses)
        .filter(status => status.value === value);

      if (filtered.length === 1) {
        return filtered[0].label;
      }
      return value;
    },
  },
};
