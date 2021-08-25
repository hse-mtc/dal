<template>
  <div :class="$style.root">
    <draggable
      :list="sections"
      v-bind="dragOptions"
      :disabled="disableDrag"
      @change="({ moved }) => updateOrder(moved.element.id, moved.newIndex)"
    >
      <transition-group type="transition" name="flip-list">
        <SectionCard
          v-for="section in sections"
          :key="section.id"
          :section-info="section"
        />
      </transition-group>
    </draggable>
  </div>
</template>

<script>
import { Component } from "vue-property-decorator";

import draggable from "vuedraggable";

import { SubjectsModule, UserModule } from "@/store";
import { hasPermission } from "@/utils/permissions";

import SectionCard from "./SectionCard.vue";

@Component({
  name: "SectionsCards",
  components: {
    SectionCard,
    draggable,
  },
})
class SectionsCards {
  get userId() { return UserModule.userId; }
  get sections() { return SubjectsModule.currentSections; }
  get dragOptions() {
    return {
      animation: 200,
      group: "description",
      disabled: false,
      ghostClass: "ghost",
      easing: "cubic-bezier(1, 0.5, 0.8, 1)",
    };
  }

  get disableDrag() {
    return !hasPermission([{
      codename: "sections-order.patch.all", // TODO: add sections-order.patch.self to BE and use validator with it on FE
      validator: () => this.userId === this.subjectOwnerId,
    }]);
  }

  updateOrder(id, order) {
    SubjectsModule.changeSectionsOrder({ id, order });
  }
}

export default SectionsCards;
</script>

<style lang="scss" module>
.root {}
</style>
