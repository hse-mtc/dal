import { Component, Vue } from "vue-property-decorator";

import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

import type { Choice } from "@/types/choices";

@Component
export class EncouragementTypesMixin extends Vue {
  encouragementTypes: Choice[] = [];
  encouragementTypesAreLoading = true;

  async beforeCreate(): Promise<void> {
    this.encouragementTypes = await ChoicesModule.encouragementTypes;
    this.encouragementTypesAreLoading = false;
  }

  encouragementTypeLabelFromValue(value: string): string {
    return defaultChoiceLabelFromValue(this.encouragementTypes, value);
  }
}
