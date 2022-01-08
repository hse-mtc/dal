<template>
  <div class="header">
    <CustomText variant="page-header">
      {{ title }}
    </CustomText>
    <AZGuard :permissions="permissions">
      <div v-if="button" class="button" @click="click">
        {{ button }}
      </div>
    </AZGuard>
  </div>
</template>

<script>
import CustomText from "@/common/CustomText";

export default {
  name: "PageHeader",
  components: {
    CustomText,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    button: {
      type: String,
      default: "",
    },
    permissions: {
      type: Array,
      default: () => [],
    },
    click: {
      type: Function,
      default: () => ({}),
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.header {
  margin-top: 30px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.button {
  color: $darkBlue;
  cursor: pointer;
}
</style>
