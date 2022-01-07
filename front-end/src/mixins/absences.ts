import { Component, Vue } from "vue-property-decorator";

import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

import { Choices } from "@/types/choices";

@Component
export class AbsenceExcusesMixin extends Vue {
  absenceExcuses: Choices = {};
  absenceExcusesAreLoading = true;

  async beforeCreate(): Promise<void> {
    this.absenceExcuses = await ChoicesModule.absenceExcuses;
    this.absenceExcusesAreLoading = false;
  }

  absenceExcuseLabelFromValue(value: string): string {
    return defaultChoiceLabelFromValue(this.absenceExcuses, value);
  }
}

@Component
export class AbsenceStatusesMixin extends Vue {
  absenceStatuses: Choices = {};
  absenceStatusesAreLoading = true;

  async beforeCreate(): Promise<void> {
    this.absenceStatuses = await ChoicesModule.absenceStatuses;
    this.absenceStatusesAreLoading = false;
  }

  absenceStatusLabelFromValue(value: string): string {
    return defaultChoiceLabelFromValue(this.absenceStatuses, value);
  }
}
