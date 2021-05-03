<template>
  <div :class="{ [wrapperClassName]: wrapperClassName }">
    <span
      v-if="title"
      :class="[$style.title, { [titleClassName]: titleClassName }]"
    >
      {{ title }}
    </span>
    <span
      v-if="annotation"
      :class="[
        $style.annotation,
        { [annotationClassName]: annotationClassName },
      ]"
    >
      {{ annotation }}
    </span>
    <slot />
  </div>
</template>

<script>
export default {
  name: "InputsBase",
  props: {
    title: { type: String, default: null },
    annotation: { type: String, default: null },
    wrapperClassName: { type: String, default: "" },
    titleClassName: { type: String, default: "" },
    annotationClassName: { type: String, default: "" },
  },
};
</script>

<style lang="scss" module>
@import "@/styles/variables.scss";

.title {
  display: block;
  margin-bottom: 8px;
  font-size: 19px;
  line-height: 23px;
  font-family: $nova;
}

.annotation {
  display: block;
  margin-bottom: 14px;
  font-family: $nova;
  font-size: 17px;
  line-height: 21px;
  color: #76767a;
}
</style>
