import { Component, ModelSync, Prop } from "vue-property-decorator";

import InputsBase from "./InputsBase.vue";

@Component({
  inheritAttrs: false,
  components: { InputsBase },
})
class InputsMixin {
  @ModelSync("modelValue", "change", { required: true }) value
  @Prop({ required: true }) modelValue
  @Prop({ default: null }) title
  @Prop({ default: null }) annotation
  @Prop({ type: String, default: "" }) wrapperClassName
  @Prop({ type: String, default: "" }) titleClassName
  @Prop({ type: String, default: "" }) annotationClassName
}

export default InputsMixin;
