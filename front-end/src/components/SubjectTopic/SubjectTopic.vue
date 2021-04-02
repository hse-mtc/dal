<template>
  <div class="topic">
    <div class="topic-title">
      <div class="d-flex align-items-center">
        <img
          height="12"
          class="mr-2"
          src="../../assets/icons/drag.svg"
          alt=""
        />
        <div>Тема №{{ index }}</div>
      </div>
      <div class="buttons" v-if="isOwner">
        <img
          v-if="isEditing"
          @click="acceptNewTopic(topic.id)"
          class="grow"
          src="../../assets/subject/accept.svg"
          alt=""
        />

        <template v-else>
          <img
            @click="isEditing = true"
            class="grow"
            src="../../assets/subject/edit.svg"
            alt=""
          />
          <img
            @click="deleteTopic(topic.id)"
            class="grow"
            src="../../assets/subject/close.svg"
            alt=""
          />
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
      <el-input class="title-input" v-model="topic.title" clearable />
    </div>

    <div v-if="!isEditing">
      <CustomText variant="paragraph">
        {{ topic.annotation }}
      </CustomText>
    </div>
    <div v-else style="width: 90%; margin-top: 10px">
      <el-input
        type="textarea"
        :autosize="{ minRows: 2, maxRows: 4 }"
        class="title-input"
        v-model="topic.annotation"
        clearable
      />
    </div>

    <div class="topic-files">
      <ClassMaterials
        v-for="(variant, key) in topic.class_materials || {}"
        :key="`${topic.id}-${key}`"
        :opened="openedMaterials.includes(key)"
        :isOwner="isOwner"
        :title="key"
        :highlight="key === highlight"
        :topic="topic.id"
        :materials="variant || []"
        :ref="key"
        @click="toggleMaterialsOpen(key)"
      />
    </div>
  </div>
</template>

<script>
import ClassMaterials from "./ClassMaterials";
import CustomText from "@/common/CustomText";

export default {
  name: "SubjectTopic",
  components: { CustomText, ClassMaterials },
  props: ["isOwner", "topic", "index"],
  data() {
    return {
      isEditing: null,
      openedMaterials: [],
      highlight: "",
    };
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

      setTimeout(() => (this.highlight = ""), 2000);
    }
  },
  methods: {
    acceptNewTopic() {
      let title;
      let annotation;

      if (this.topic.title) {
        this.$message.warning("Пожалуйста, заполните название темы");
        return;
      }

      if (this.topic.annotation) {
        this.$message.warning("Пожалуйста, заполните аннотацию для темы");
        return;
      }

      const dataToSend = {
        title: title,
        annotation: annotation,
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
          (item) => item !== key
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
