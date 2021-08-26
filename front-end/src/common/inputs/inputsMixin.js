import {
  Component,
  ModelSync,
  Prop,
  Vue,
} from "vue-property-decorator";

import InputsBase from "./InputsBase.vue";

@Component({
  inheritAttrs: false,
  components: { InputsBase },
})
class InputsMixin extends Vue {
  @ModelSync("modelValue", "change", { required: true }) value
  @Prop({ required: true }) modelValue
  @Prop({ default: null }) title
  @Prop({ default: null }) annotation
  @Prop({ type: String, default: "" }) wrapperClassName
  @Prop({ type: String, default: "" }) titleClassName
  @Prop({ type: String, default: "" }) annotationClassName
  @Prop({ type: Boolean }) leftLabel
  @Prop({ default: "auto " }) labelWidth
}

export default InputsMixin;
