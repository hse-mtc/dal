<template>
  <ElForm
    ref="form"
    :key="reloadKey"
    :model="dataByTypes[type]"
    :rules="rulesByTypes[type]"
    action="#"
    @submit.native.prevent="onSubmit"
    @keypress.enter.native.prevent="onSubmit"
  >
    <ElFormItem
      v-for="({ placeholder, formatter }, field) in fieldsByTypes[type]"
      :key="field"
      :prop="field"
    >
      <el-input
        v-model="dataByTypes[type][field]"
        :placeholder="placeholder"
        @input="onChange(field, formatter, $event)"
      />
    </ElFormItem>

    <el-button
      type="primary"
      @click="onSubmit"
    >
      {{ isEdit ? 'Изменить' : 'Добавить' }}
    </el-button>

    <el-button
      v-if="isEdit"
      @click="$emit('cancel')"
    >
      Отменить
    </el-button>
  </ElForm>
</template>

<script>
import {
  Component,
  Prop,
  Vue,
  Watch,
} from "vue-property-decorator";
import _cloneDeep from "lodash/cloneDeep";

const capitalize = value => (value
  ? value[0].toUpperCase() + value.slice(1).toLowerCase()
  : "");

@Component({
  name: "DictionariesForms",
})
class DictionariesForms extends Vue {
  @Prop({ type: String }) type
  @Prop({ type: Object, default: () => ({}) }) initState
  @Prop({ type: Boolean }) isEdit

  reloadKey = 0

  dataByTypes = {
    publishers: {
      name: "",
    },
    authors: {
      surname: "",
      name: "",
      patronymic: "",
    },
    categories: {
      title: "",
    },
    achievementTypes: {
      title: "",
    },
    milfaculties: {
      title: "",
      abbreviation: "",
    },
    ranks: {
      title: "",
    },
    rooms: {
      title: "",
    },
    skills: {
      title: "",
    },
  }

  fieldsByTypes = {
    publishers: {
      name: { placeholder: "Введите нового издателя" },
    },
    authors: {
      surname: { placeholder: "Введите фамилию", formatter: capitalize },
      name: { placeholder: "Введите имя", formatter: capitalize },
      patronymic: { placeholder: "Введите отчество", formatter: capitalize },
    },
    categories: {
      title: { placeholder: "Введите название" },
    },
    achievementTypes: {
      title: { placeholder: "Введите название" },
    },
    milfaculties: {
      title: { placeholder: "Введите название" },
      abbreviation: { placeholder: "Введите сокращение" },
    },
    ranks: {
      title: { placeholder: "Введите название" },
    },
    rooms: {
      title: { placeholder: "Введите название" },
    },
    skills: {
      title: { placeholder: "Введите название" },
    },
  }

  rulesByTypes = {
    publishers: {
      name: [{ required: true, message: "Обязательное поле" }],
    },
    authors: {
      surname: [{ required: true, message: "Обязательное поле" }],
      name: [{ required: true, message: "Обязательное поле" }],
      patronymic: [],
    },
    categories: {
      title: [{ required: true, message: "Обязательное поле" }],
    },
    achievementTypes: {
      title: [{ required: true, message: "Обязательное поле" }],
    },
    milfaculties: {
      title: [{ required: true, message: "Обязательное поле" }],
    },
    ranks: {
      title: [{ required: true, message: "Обязательное поле" }],
    },
    rooms: {
      title: [{ required: true, message: "Обязательное поле" }],
    },
    skills: {
      title: [{ required: true, message: "Обязательное поле" }],
    },
  }

  onSubmit(e) {
    if (e) { e.preventDefault(); }

    const data = this.dataByTypes[this.type];
    const keys = Object.keys(data);
    keys.forEach(key => {
      data[key] = data[key].trim();
    });

    this.$refs.form.validate(valid => {
      if (valid) {
        this.$emit(
          this.isEdit ? "change" : "submit",
          data,
        );
        this.dataByTypes[this.type] = {};
        this.reloadKey += 1;
      }
    });
  }

  initEdit() {
    this.dataByTypes[this.type] = this.isEdit
      ? _cloneDeep(this.initState)
      : {};

    this.reloadKey += 1;
  }

  onChange(field, formatter, value) {
    this.dataByTypes[this.type][field] = formatter
      ? formatter(value)
      : value;
  }

  @Watch("initState", { deep: true })
  onInitStateChange() { this.initEdit(); }

  @Watch("isEdit", { deep: true })
  onIsEditChange() { this.initEdit(); }
}

export default DictionariesForms;
</script>
