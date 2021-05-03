<template>
  <div class="topic">
    <div class="topic-title">
      <div class="d-flex align-items-center">
        <img
          height="12"
          class="mr-2"
          src="../../assets/icons/drag.svg"
          alt=""
        >
        <div>Тема №{{ index }}</div>
      </div>
      <div v-if="isOwner" class="buttons">
        <img
          v-if="isEditing"
          class="grow"
          src="../../assets/subject/accept.svg"
          alt=""
          @click="acceptNewTopic(topic.id)"
        >

        <template v-else>
          <img
            class="grow"
            src="../../assets/subject/edit.svg"
            alt=""
            @click="isEditing = true"
          >
          <img
            class="grow"
            src="../../assets/subject/close.svg"
            alt=""
            @click="deleteTopic(topic.id)"
          >
          <!-- <img
            @click="downloadTopic(topic.id)"
            class="grow"
            src="../../assets/subject/download.svg"
            alt=""
          /> -->
        </template>
      </div>
    </div>

    <div v-if="!isEditing">
      <CustomText variant="header" class="topic-content">
        {{ topic.title }}
      </CustomText>
    </div>
    <div v-else style="width: 90%">
      <el-input v-model="title" class="title-input" clearable />
    </div>

    <div v-if="!isEditing">
      <CustomText variant="paragraph">
        {{ topic.annotation }}
      </CustomText>
    </div>
    <div v-else style="width: 90%; margin-top: 10px">
      <el-input
        v-model="annotation"
        type="textarea"
        :autosize="{minRows: 2, maxRows: 4}"
        class="title-input"
        clearable
      />
    </div>

    <div class="topic-files">
      <ClassMaterials
        v-for="(variant, key) in topic.class_materials || {}"
        :key="`${topic.id}-${key}`"
        :ref="key"
        :opened="openedMaterials.includes(key)"
        :is-owner="isOwner"
        :title="key"
        :highlight="key === highlight"
        :topic="topic.id"
        :materials="variant || []"
        @click="toggleMaterialsOpen(key)"
      />
    </div>
  </div>
</template>

<script>
import CustomText from "@/common/CustomText.vue";
import ClassMaterials from "./ClassMaterials.vue";

export default {
  name: "SubjectTopic",
  components: { CustomText, ClassMaterials },
  model: {
    prop: "topic",
    event: "update",
  },
  props: {
    isOwner: { type: Boolean },
    topic: { type: Object, required: true, default: () => ({}) },
    index: { type: Number, required: true },
  },
  data() {
    return {
      isEditing: null,
      openedMaterials: [],
      highlight: "",
    };
  },
  computed: {
    title: {
      get() { return this.topic.title; },
      set(value) {
        this.$emit("update", {
          ...this.topic,
          title: value,
        });
      },
    },
    annotation: {
      get() { return this.topic.annotation; },
      set(value) {
        this.$emit("update", {
          ...this.topic,
          annotation: value,
        });
      },
    },
  },
  mounted() {
    if (+this.$route.query.topic === this.topic.id) {
      this.openedMaterials = [
        ...this.openedMaterials,
        this.$route.query.materialsType,
      ];
      this.$refs[this.$route.query.materialsType][0].$vnode.elm.scrollIntoView({
        block: "center",
        inline: "nearest",
        behavior: "smooth",
      });

      this.highlight = this.$route.query.materialsType;

      setTimeout(() => { this.highlight = ""; }, 2000);
    }
  },
  methods: {
    acceptNewTopic() {
      if (!this.topic.title) {
        this.$message.warning("Пожалуйста, заполните название темы");
        return;
      }

      if (!this.topic.annotation) {
        this.$message.warning("Пожалуйста, заполните аннотацию для темы");
        return;
      }

      const dataToSend = {
        title: this.topic.title,
        annotation: this.topic.annotation,
      };

      this.$emit("change", { id: this.topic.id, newData: dataToSend });
      this.isEditing = null;
    },
    deleteTopic() {
      this.$emit("delete", this.topic.id);
    },
    toggleMaterialsOpen(key) {
      const index = this.openedMaterials.indexOf(key);

      if (index !== -1) {
        this.openedMaterials = this.openedMaterials.filter(
          item => item !== key,
        );
      } else {
        this.openedMaterials = [...this.openedMaterials, key];
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
