<template>
  <div class="root" @click="selectSubject">
    <div>
      <div class="header">
        <CustomText
          variant="header"
          @click="selectSubject"
        >
          {{ title }}
        </CustomText>
      </div>
      <CustomText
        class="annotation"
        variant="paragraph"
        color="#333"
      >
        {{ annotation }}
      </CustomText>
    </div>
    <div class="owner">
      <svg-icon
        icon-class="owner"
        class="icon"
      />

      {{ owner }}
    </div>
  </div>
</template>

<script>
import CustomText from "@/common/CustomText";

export default {
  name: "SubjectCard",
  components: {
    CustomText,
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    annotation: {
      type: String,
      required: true,
    },
    owner: {
      type: String,
      required: true,
    },
    isMySubject: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {};
  },
  methods: {
    selectSubject(e) {
      if (e.target.nodeName === "IMG") return;
      this.$router.push({ path: `/discipline-control/subjects/${this.id}/` });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
