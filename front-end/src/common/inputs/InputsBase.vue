<template>
  <div
    :class="{
      [wrapperClassName]: wrapperClassName,
      [$style.wrapper]: true,
      [$style.wrapperLeft]: leftLabel,
    }"
  >
    <div
      :class="{ [$style.left]: leftLabel }"
      :style="{
        width: labelWidth,
      }"
    >
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
    </div>

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
  @Prop({ type: Boolean }) leftLabel
  @Prop({ default: "auto" }) labelWidth
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

.wrapper {
  &Left {
    display: flex;
    align-items: center;
  }
}

.left {
  margin-right: 15px;
  flex: none;
}

</style>
