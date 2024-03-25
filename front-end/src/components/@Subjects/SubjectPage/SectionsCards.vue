<template>
  <div>
    <Draggable
      :list="sections"
      v-bind="dragOptions"
      :disabled="disableDrag"
      handle=".dragIcon"
      @change="({ moved }) => updateOrder(moved.element.id, moved.newIndex)"
    >
      <transition-group type="transition" name="flip-list">
        <SectionCard
          v-for="section in sections"
          :id="`section-${section.id}`"
          :key="section.id"
          ref="childSection"
          v-model="openedCards[section.id]"
          :section-info="section"
          @update="updateInSubcomponents"
        />
      </transition-group>
    </Draggable>
  </div>
</template>

<script>
import { Component, Vue, Watch } from "vue-property-decorator";

import Draggable from "vuedraggable";

import { SubjectsModule, UserModule } from "@/store";
import { hasPermission } from "@/utils/permissions";

import SectionCard from "./SectionCard.vue";

@Component({
  name: "SectionsCards",
  components: {
    SectionCard,
    Draggable,
  },
})
class SectionsCards extends Vue {
  openedCards = {}

  created() {
    SubjectsModule.setCurrentSubjectId(this.$route.params.subjectId);
    SubjectsModule.fetchSections();
  }

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

  @Watch("sections")
  watchSections() {
    this.$nextTick(this.updateInSubcomponents);
  }

  updateOrder(id, order) {
    SubjectsModule.changeSectionsOrder({ id, order }).then(this.updateInSubcomponents);
  }

  updateInSubcomponents() {
    this.$refs.childSection?.forEach(section => section.updateInSubcomponents());
  }

  @Watch("$route", { immediate: true })
  onRouteChange(next) {
    if (next.query.section) {
      this.openedCards[next.query.section] = true;
    }
  }
}

export default SectionsCards;
</script>
