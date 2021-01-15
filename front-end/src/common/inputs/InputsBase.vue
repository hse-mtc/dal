<template>
    <div :class="{[wrapperClassName]: wrapperClassName}">
      <span
        v-if="title"
        :class="[$style.title, {[titleClassName]: titleClassName}]"
      >
        {{ title }}
      </span>
      <slot />
    </div>
</template>

<script>
export default {
  name: 'InputsBase',
  props: {
    title: {default: null},
    wrapperClassName: {type: String, default: ''},
    titleClassName: {type: String, default: ''},
  }
}
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
</style>