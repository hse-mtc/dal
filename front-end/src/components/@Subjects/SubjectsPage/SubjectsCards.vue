<template>
  <div :class="$style.root">
    <div
      v-for="card in cards"
      :key="card.id"
      :class="$style.cardWrapper"
    >
      <SubjectCard
        :id="card.id"
        :annotation="card.annotation"
        :title="card.title"
        :is-my-subject="userId === card.user.id"
        :owner="card.user.email"
      />
    </div>
  </div>
</template>

<script>
import { UserModule } from "@/store";
import { Component, Prop } from "vue-property-decorator";

import SubjectCard from "./SubjectCard/index.vue";

@Component({
  name: "Subjects",
  components: { SubjectCard },
})
class Subjects {
  @Prop({ default: () => [] }) cards

  get userId() { return UserModule.userId; }
}

export default Subjects;
</script>

<style lang="scss" module>
.root {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  margin: -20px -20px 0 0;
}

.cardWrapper {
  width: calc(50% - 20px);
  margin: 20px 20px 0 0;
}

@media screen and (max-width: 768px) {
  .root {
    flex-direction: column;
    margin: 0;
  }

  .cardWrapper {
    width: 100%;
    margin: 20px 0 0;

    &:first-child {
      margin-top: 0;
    }
  }
}
</style>
