import { Component, Vue } from "vue-property-decorator";

import { ChoicesModule } from "@/store";

import { defaultChoiceLabelFromValue } from "@/utils/choices";

import { Choice } from "@/types/choices";

@Component
class EncouragementTypesMixin extends Vue {
  encouragementTypes: Choice[] = [];
  encouragementTypesAreLoading: boolean = true;

  async beforeCreate(): Promise<void> {
    this.encouragementTypes = await ChoicesModule.encouragementTypes;
    this.encouragementTypesAreLoading = false;
  }

  encouragementTypeLabelFromValue(value: string): string {
    return defaultChoiceLabelFromValue(this.encouragementTypes, value);
  }
}
