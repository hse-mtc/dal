<template>
  <div :class="variant" :style="{ color: color, ...customStyle }">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "CustomText",
  props: {
    variant: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      default: "black",
    },
    customStyle: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },
};
</script>

<style scoped lang="scss">
.page-header {
  font-family: ProximaNovaRegular;
  font-style: normal;
  font-weight: normal;
  font-size: 44px;
  line-height: 54px;
}

.header {
  font-family: ProximaNovaRegular;
  font-style: normal;
  font-weight: 600;
  font-size: 22px;
  line-height: 27px;
}

.sub-header {
  font-family: ProximaNovaRegular;
  font-style: normal;
  font-weight: normal;
  font-size: 19px;
  line-height: 23px;
}

.paragraph {
  font-family: ProximaNovaRegular;
  font-style: normal;
  font-weight: normal;
  font-size: 18px;
  line-height: 24px;
}
</style>
