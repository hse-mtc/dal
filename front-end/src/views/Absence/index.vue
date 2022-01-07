<template>
  <div class="app-container">
    <Absence />
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";

import Absence from "@/components/Absence/Absence.vue";

@Component({
  name: "AbsenceView",
  components: { Absence },
})
class AbsenceView extends Vue {}

export default AbsenceView;
</script>
