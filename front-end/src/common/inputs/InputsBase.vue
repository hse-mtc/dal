<template>
  <div :class="{ [wrapperClassName]: wrapperClassName }">
    <span
      v-if="title"
      :class="[
        $style.title,
        { [titleClassName]: titleClassName },
      ]"
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
import { Component, Prop } from "vue-property-decorator";

@Component({
  name: "InputBase",
})
class InputBase {
  @Prop({ type: String, default: null }) title
  @Prop({ type: String, default: null }) annotation
  @Prop({ type: String, default: "" }) wrapperClassName
  @Prop({ type: String, default: "" }) titleClassName
  @Prop({ type: String, default: "" }) annotationClassName
}

export default InputBase;
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
