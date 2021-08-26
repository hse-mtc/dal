<template>
  <div ref="root" :class="$style.root">
    <div :class="$style.header">
      <div :class="$style.topline">
        <svg-icon icon-class="drag" />

        <div>Тема №{{ topic.order + 1 }}</div>

        <div :class="$style.buttons">
          <svg-icon
            v-if="isEditing"
            :class="$style.button"
            icon-class="accept"
            @click="acceptNewTopic(topic.id)"
          />

          <template v-else>
            <AZGuard
              :permissions="['topics.patch.all', {
                codename: 'topics.patch.self',
                validator: () => userId === subjectOwnerId,
              }]"
            >
              <svg-icon
                :class="$style.button"
                icon-class="edit"
                @click="isEditing = true"
              />
            </AZGuard>
            <AZGuard
              :permissions="['topics.delete.all', {
                codename: 'topics.delete.self',
                validator: () => userId === subjectOwnerId,
              }]"
            >
              <svg-icon
                :class="$style.button"
                icon-class="close"
                @click="deleteTopic(topic.id)"
              />
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
    </div>
  </div>
</template>

<script>
import {
  Component,
  Prop,
  Ref,
  Vue,
} from "vue-property-decorator";

import { SubjectsModule, UserModule } from "@/store";

import ClassMaterials from "./ClassMaterials.vue";

@Component({
  name: "TopicCard",
  components: { ClassMaterials },
})
class TopicCard extends Vue {
  @Prop({ required: true }) topic

  @Ref() root

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

  // mounted() { this.onRouteChange(); }

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

  // @Watch("$route")
  // onRouteChange({ query: { topic, materialsType } }) {
  //   if (+topic === this.topic.id && materialsType) {
  //     this.openedMaterials[materialsType] = true;
  //     this.root.scrollIntoView({
  //       block: "start",
  //       inline: "nearest",
  //       behavior: "smooth",
  //     });
  //   }
  // }
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
        font-size: 24px;
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
