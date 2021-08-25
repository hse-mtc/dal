<template>
  <div v-if="shown" :class="$style.root">
    <AZGuard
      :permissions="['topics.post.all', {
        codename: 'topics.post.self',
        validator: () => userId === subjectOwnerId,
      }]"
    >
      <el-button
        type="text"
        :class="$style.addButton"
        @click="addTopic"
      >
        + Добавить тему
      </el-button>
    </AZGuard>

    <Draggable
      :list="topics"
      v-bind="dragOptions"
      :disabled="disableDrag"
      @change="({ moved }) => updateOrder(moved.element.id, moved.newIndex)"
    >
      <transition-group type="transition" name="flip-list">
        <TopicCard
          v-for="topic in topics"
          :key="topic.id"
          :topic="topic"
          @change="editTopic"
          @delete="deleteTopic"
        />
      </transition-group>
    </Draggable>
  </div>
</template>

<script>
import { Component, Prop } from "vue-property-decorator";

import Draggable from "vuedraggable";

import {
  addTopics,
  changeTopicOrder, deleteTopics, editTopics, getTopics,
} from "@/api/topic";
import {
  getAddRequest,
  getDeleteRequest, getEditRequest, getFetchRequest, getOrderChangeRequest,
} from "@/utils/mutators";
import { hasPermission } from "@/utils/permissions";

import TopicCard from "./TopicCard.vue";

@Component({
  name: "TopicsCards",
  components: {
    TopicCard,
    Draggable,
  },
})
class TopicsCards {
  @Prop({ required: true }) sectionId
  @Prop({ required: true }) shown

  topicsList = []
  topicsListLoaded = false

  get topics() {
    if (!this.topicsListLoaded) {
      this.getTopics();
    }

    return this.topicsList;
  }

  get dragOptions() {
    return {
      animation: 200,
      group: "description",
      disabled: false,
      ghostClass: "ghost",
      easing: "cubic-bezier(1, 0.5, 0.8, 1)",
    };
  }

  get disableDrag() {
    return !hasPermission([{
      codename: "sections-order.patch.all", // TODO: add sections-order.patch.self to BE and use validator with it on FE
      validator: () => this.userId === this.subjectOwnerId,
    }]);
  }

  getTopics() {
    getFetchRequest(
      () => getTopics(this.sectionId),
      data => {
        this.topicsList = data;
        this.topicsListLoaded = true;
      },
      "темы",
    ).call(this);
  }

  addTopic() {
    getAddRequest(
      addTopics,
      data => { this.topicsList = data; },
      "topicsList",
      "тему",
    ).call(this, {
      title: "Новая тема",
      section: this.sectionId,
      annotation: "Введите аннотацию",
    });
  }

  editTopic({ id, ...newData }) {
    getEditRequest(
      editTopics,
      data => { this.topicsList = data; },
      "topicsList",
      "тему",
    ).call(this, { id, ...newData });
  }

  async deleteTopic(id) {
    await this.$confirm(
      "Вы уверены, что хотите удалить тему? Это действие не обратимо.",
      "Подтверждение",
      {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      },
    );

    getDeleteRequest(
      deleteTopics,
      data => { this.topicsList = data; },
      "topicsList",
      "тему",
    ).call(this, id);
  }

  updateOrder(id, order) {
    getOrderChangeRequest(
      changeTopicOrder,
      data => { this.topicsList = data; },
      "topicsList",
      "тему",
    ).call(this, id, order);
  }
}

export default TopicsCards;
</script>

<style lang="scss" module>
.addButton {
  display: block;
  margin: 20px 0 0 auto;
  font-size: 18px;
  color: #0c4b9a;
}
</style>
