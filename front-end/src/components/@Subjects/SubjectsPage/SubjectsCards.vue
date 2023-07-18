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
        :milspecialty="milspecaltyCode(card.milspecialty)"
        :is-my-subject="userId === card.user.id"
        :owner="card.user.email"
      />
    </div>
  </div>
</template>

<script>
import { UserModule } from "@/store";
import { Component, Prop, Vue } from "vue-property-decorator";

import SubjectCard from "./SubjectCard/index.vue";
import { getMilSpecialties } from "@/api/reference-book";

@Component({
  name: "Subjects",
  components: { SubjectCard },
})
class Subjects extends Vue {
  @Prop({ default: () => [] }) cards
  @Prop({ default: () => [] }) milspecialties

  get userId() { return UserModule.userId; }

  milspecaltyCode(milspecialtyId) {
    if (milspecialtyId) {
      return `ВУС: ${this.milspecialties.filter(milspecialty => milspecialty.id === milspecialtyId)[0].code}`;
    }
    return "";
  }
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
