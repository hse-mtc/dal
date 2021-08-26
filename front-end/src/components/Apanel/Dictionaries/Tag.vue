<template>
  <el-tag
    :class="$style.root"
    closable
    @close="$emit('delete')"
  >
    {{ title }}
    <button
      :class="$style.button"
      @click="$emit('edit')"
    >
      <i class="el-icon-edit" />
    </button>
  </el-tag>
</template>

<script>
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  name: "Dictionaries",
})
class Dictionaries extends Vue {
  @Prop({ required: true, type: Number }) id
  @Prop({ required: true, type: String }) title
}

export default Dictionaries;
</script>

<style lang="scss" module>
@import "@/styles/variables.scss";

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  font-size: 10px;
  color: #409eff;
  border: none;
  border-radius: 50%;
  background: transparent;

  &:hover {
    color: #fff;
    background-color: #409eff;
  }
}
</style>
