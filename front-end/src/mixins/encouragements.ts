import { Component, Vue } from "vue-property-decorator";

import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

import type { Choices } from "@/types/choices";

@Component
export class EncouragementTypesMixin extends Vue {
  encouragementTypes: Choices = {};
  encouragementTypesAreLoading = true;

  async beforeCreate(): Promise<void> {
    this.encouragementTypes = await ChoicesModule.encouragementTypes;
    this.encouragementTypesAreLoading = false;
  }

  encouragementTypeLabelFromValue(value: string): string {
    return defaultChoiceLabelFromValue(this.encouragementTypes, value);
  }
}
