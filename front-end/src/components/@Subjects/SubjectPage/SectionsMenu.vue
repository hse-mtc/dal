<template>
  <div :class="$style.menu">
    <span :class="[$style.menuItem, $style.menuTitle]">
      Все разделы
    </span>
    <span
      v-for="section in sections"
      :id="section.id"
      :key="section.id"
      :class="$style.menuItem"
    >
      {{ section.title }}
    </span>
  </div>
</template>

<script>
import { Component } from "vue-property-decorator";

import { SubjectsModule } from "@/store";

@Component({
  name: "SectionsMenu",
})
class SectionsMenu {
  get sections() { return SubjectsModule.currentSections; }
}

export default SectionsMenu;
</script>

<style lang="scss" module>
.menu {
  background-color: #f5f5f7;
  padding: 15px;

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
}
</style>
