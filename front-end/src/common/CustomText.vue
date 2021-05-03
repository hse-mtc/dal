<template>
  <div
    :class="variant"
    :style="{
      color: color,
      'margin-top': mt + 'px',
      'margin-bottom': mb + 'px',
      'margin-left': ml + 'px',
      'margin-right': mr + 'px',
      ...customStyle,
    }"
  >
    <slot />
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
      default: () => ({}),
    },
    mt: {
      type: Number,
      default: 0,
    },
    mb: {
      type: Number,
      default: 0,
    },
    mr: {
      type: Number,
      default: 0,
    },
    ml: {
      type: Number,
      default: 0,
    },
  },
};
</script>

<style scoped lang="scss">
.page-header {
  font-family: ProximaNovaRegular;
  font-style: normal;
  font-weight: 400;
  font-size: 44px;
  margin-top: 30px;
}

.page-header-1 {
  font-family: ProximaNovaRegular;
  font-style: normal;
  font-weight: normal;
  font-size: 36px;
  line-height: 44px;
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

.label-1 {
  font-family: ProximaNovaRegular;
  font-style: normal;
  font-weight: 600;
  font-size: 16px;
  line-height: 20px;
}
</style>
