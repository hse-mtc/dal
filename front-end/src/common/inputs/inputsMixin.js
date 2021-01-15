import InputsBase from './InputsBase.vue'

export default {
  components: { InputsBase },
  model: {
    prop: 'modelValue',
    event: 'change',
  },
  props: {
    modelValue: { required: true },
    title: { default: null },
    wrapperClassName: { type: String, default: '' },
    titleClassName: { type: String, default: '' },
  },
  computed: {
    value: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('change', value)
      }
    },
  }
}