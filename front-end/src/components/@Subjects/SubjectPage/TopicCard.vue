<template>
  <div :class="$style.root">
    <div :class="$style.header">
      <div :class="$style.topline">
        <svg-icon icon-class="drag" />

        <div>Тема №{{ topic.order + 1 }}</div>

        <div :class="$style.buttons">
          <img
            v-if="isEditing"
            :class="$style.button"
            src="../../../assets/subject/accept.svg"
            alt=""
            @click="acceptNewTopic(topic.id)"
          >

          <template v-else>
            <AZGuard
              :permissions="['topics.patch.all', {
                codename: 'topics.patch.self',
                validator: () => userId === subjectOwnerId,
              }]"
            >
              <img
                :class="$style.button"
                src="../../../assets/subject/edit.svg"
                alt=""
                @click="isEditing = true"
              >
            </AZGuard>
            <AZGuard
              :permissions="['topics.delete.all', {
                codename: 'topics.delete.self',
                validator: () => userId === subjectOwnerId,
              }]"
            >
              <img
                :class="$style.button"
                src="../../../assets/subject/close.svg"
                alt=""
                @click="deleteTopic(topic.id)"
              >
            </AZGuard>
          </template>
        </div>
      </div>

      <span v-if="!isEditing" :class="$style.title">
        {{ topic.title }}
      </span>
      <div v-else :class="$style.titleWrapper">
        <el-input
          v-model="topic.title"
          :class="[$style.title, $style.titleInput]"
          size="small"
        />
      </div>

      <span v-if="!isEditing" :class="$style.annotation">
        {{ topic.annotation }}
      </span>
      <div v-else :class="$style.annotationWrapper">
        <el-input
          v-model="topic.annotation"
          :class="[$style.annotation, $style.annotationInput]"
          size="mini"
          type="textarea"
          autosize
        />
      </div>
    </div>

    <div class="topic-files">
      <ClassMaterials
        v-for="(title, type) in titles"
        :key="type"
        v-model="openedMaterials[type]"
        :title="title"
        :code="codes[type]"
        :materials="materials[type]"
        :topic-id="topic.id"
        @delete="$emit('deleteMaterial', $event)"
      />
      <!-- <ClassMaterials
        v-for="(variant, key) in (topic.class_materials || {})"
        :key="`${topic.id}-${key}`"
        :ref="key"
        :opened="openedMaterials[key]"
        :subject-owner-id="subjectOwnerId"
        :title="key"
        :highlight="key === highlight"
        :topic="topic.id"
        :materials="variant || []"
        @click="openedMaterials[key] = !openedMaterials[key]"
      /> -->
    </div>
  </div>
</template>

<script>
import { Component, Prop } from "vue-property-decorator";

import { SubjectsModule, UserModule } from "@/store";

import { getDeleteRequest } from "@/utils/mutators";
import ClassMaterials from "./ClassMaterials.vue";

@Component({
  name: "TopicCard",
  components: { ClassMaterials },
})
class TopicCard {
  @Prop({ required: true }) topic

  isEditing = false

  openedMaterials = {
    lectures: false,
    seminars: false,
    groups: false,
    practices: false,
  }

  titles = {
    lectures: "Лекции",
    seminars: "Семинары",
    groups: "Групповые занятия",
    practices: "Практические занятия",
  }

  codes = {
    lectures: "LE",
    seminars: "SE",
    groups: "GR",
    practices: "PR",
  }

  get materials() { return this.topic.class_materials; }
  get subjectOwnerId() { return SubjectsModule.currentSubject.user.id; }
  get userId() { return UserModule.userId; }

  acceptNewTopic() {
    if (!this.topic.title) {
      this.$message.warning("Пожалуйста, заполните название темы");
      return;
    }

    if (!this.topic.annotation) {
      this.$message.warning("Пожалуйста, заполните аннотацию для темы");
      return;
    }

    this.isEditing = false;

    this.$emit("change", {
      id: this.topic.id,
      title: this.topic.title,
      annotation: this.topic.annotation,
    });
  }

  deleteTopic() {
    this.$emit("delete", this.topic.id);
  }

  async deleteMaterial(id) {
    await this.$confirm(
      "Вы уверены, что хотите удалить материал? Это действие не обратимо.",
      "Подтверждение",
      {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      },
    );
  }
}

export default TopicCard;
</script>

<style lang="scss" module>
.root {
  margin-top: 20px;
  padding: 20px 16px 20px;
  border: 1px solid #e5e5eb;
  border-radius: 12px;
}

.header {
  .topline {
    display: flex;
    align-items: center;

    .buttons {
      margin-left: auto;

      .button {
        cursor: pointer;
        transition: all 0.2s ease-in-out;

        &:nth-child(2) {
          margin-left: 10px;
        }

        &:hover {
          transform: scale(1.2);
        }
      }
    }
  }

  .title,
  .annotation {
    display: block;

    :global(.el-textarea__inner),
    :global(.el-input__inner) {
      padding: 0;
    }
  }

  .title {
    font-size: 22px;
    font-weight: bold;

    :global(.el-input__inner) {
      font-weight: bold;
    }
  }

  .annotation {
    font-size: 18px;
  }
}
</style>
