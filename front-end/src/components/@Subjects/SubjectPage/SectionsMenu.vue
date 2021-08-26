<template>
  <div :class="$style.menu">
    <span :class="$style.menuTitle">
      Все разделы
    </span>
    <span
      v-for="section in sections"
      :id="section.id"
      :key="section.id"
      :class="$style.menuItem"
      @click="scrollToSection(section.id)"
    >
      {{ section.title }}
    </span>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";

import { SubjectsModule } from "@/store";

@Component({
  name: "SectionsMenu",
})
class SectionsMenu extends Vue {
  get sections() { return SubjectsModule.currentSections; }

  scrollToSection(id) {
    const section = document.getElementById(`section-${id}`);

    if (section) {
      section.scrollIntoView({
        block: "start",
        inline: "nearest",
        behavior: "smooth",
      });
    }
  }
}

export default SectionsMenu;
</script>

<style lang="scss" module>
@import "@/styles/variables.scss";

.menu {
  background-color: #f5f5f7;
  padding: 15px;
  border-radius: 15px;

  &Title,
  &Item {
    display: block;
    margin-top: 10px;

    &:first-child {
      margin-top: 0;
    }
  }

  &Title {
    font-weight: bold;
  }

  &Item {
    cursor: pointer;

    &:hover {
      color: $darkBlue;
    }
  }
}
</style>
