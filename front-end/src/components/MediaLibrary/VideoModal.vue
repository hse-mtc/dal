<template>
  <ModalWindow :opened="true" v-on="$listeners">
    <el-form ref="form" :model="formValues" :rules="rules">
      <el-form-item prop="title">
        <TextInput
          v-model="formValues.title"
          title="Название"
          is-text-area
        />
      </el-form-item>

      <el-form-item prop="annotation">
        <TextInput
          v-model="formValues.annotation"
          title="Описание"
          is-text-area
        />
      </el-form-item>

      <el-form-item prop="video">
        <FileInput
          v-model="formValues.video"
          title="Загрузите видео"
          :limit="1"
          :files-types="['.mp4', '.mov', '.avi', '.mkv', '.webm']"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">
          Сохранить
        </el-button>
        <el-button type="info" @click="close">
          Закрыть
        </el-button>
      </el-form-item>
    </el-form>
  </ModalWindow>
</template>

<script>
import {
  FileInput,
  TextInput,
} from "@/common/inputs";

import ModalWindow from "@/components/ModalWindow/ModalWindow.vue";

export default {
  name: "VideoModal",
  components: {
    ModalWindow,
    TextInput,
    FileInput,
  },
  props: {
    initData: { type: Object, required: true },
    isChanging: { type: Boolean, default: false },
  },
  data() {
    const required = [{ required: true, message: "Обязательное поле" }];
    return {
      rules: {
        title: required,
      },
      formValues: this.lodash.cloneDeep(this.initData),
    };
  },
  watch: {
    initData(nextValue, prevValue) {
      if (!this.lodash.isEqual(nextValue, prevValue)) {
        this.formValues = this.lodash.cloneDeep(nextValue);
      }
    },
  },
  methods: {
    onSubmit() {
      this.$refs.form.validate(valid => {
        if (!valid || (!this.isChanging && !this.formValues.video.length)) {
          return false;
        }

        this.$emit("save", this.formValues);
        this.$emit("close-modal", true);
        return true;
      });
    },
    close() {
      this.$emit("close-modal", true);
    },
  },
};
</script>
