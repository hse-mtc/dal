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
      @change="({ moved }) => updateOrder(moved.element.id, moved.newIndex, moved.element.section)"
    >
      <transition-group type="transition" name="flip-list">
        <TopicCard
          v-for="topic in topics"
          :id="`section-${sectionId}-topic-${topic.id}`"
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
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

import Draggable from "vuedraggable";

import {
  addTopics,
  changeTopicOrder,
  deleteTopics,
  editTopics,
  getTopics,
} from "@/api/topic";

import {
  getAddRequest,
  getDeleteRequest,
  getEditRequest,
  getFetchRequest,
  getOrderChangeRequest,
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
class TopicsCards extends Vue {
  @Prop({ required: true }) sectionId
  @Prop({ required: true }) shown
  @Prop({ required: true }) sections

  topicsList = []
  topicsListLoaded = false
  editMutated = false

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

  async addTopic() {
    const res = await getAddRequest(
      addTopics,
      data => { this.topicsList = data; },
      "topicsList",
      "тему",
    ).call(this, {
      title: "Новая тема",
      section: this.sectionId,
      annotation: "Введите аннотацию",
    });

    if (res) {
      this.$nextTick(() => {
        const elem = document.getElementById(`section-${
          this.sectionId
        }-topic-${
          this.topics[this.topics.length - 1].id
        }`);

        if (elem) {
          elem.scrollIntoView({
            block: "start",
            inline: "nearest",
            behavior: "smooth",
          });
        }
      });
    }
    this.getTopics();
  }

  async editTopic({ id, ...newData }) {
    this.editMutated = await getEditRequest(
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
    await getDeleteRequest(
      deleteTopics,
      data => { this.topicsList = data; },
      "topicsList",
      "тему",
    ).call(this, id);
    this.getTopics();
  }

  async updateOrder(id, order, sectionId) {
    let newOrder = null;
    const sectionOrder = this.sections.filter(section => section.id === sectionId)[0].order;
    if (sectionOrder !== 0) {
      const previousSectionId = this.sections.filter(section => section.order === sectionOrder - 1)[0].id;
      let topicsArray = [];
      await getFetchRequest(
        () => getTopics(previousSectionId),
        data => {
          topicsArray = data;
          this.topicsListLoaded = true;
        },
        "темы",
      ).call(this);
      newOrder = topicsArray[topicsArray.length - 1].order + 1 + order;
    } else {
      newOrder = order;
    }
    await getOrderChangeRequest(
      changeTopicOrder,
      data => { this.topicsList = data; },
      "topicsList",
      "тему",
    ).call(this, id, newOrder);
    this.getTopics();
  }

  @Watch("editMutated")
  onEditMutatedChange() {
    if (this.editMutated) {
      this.getTopics();
      this.editMutated = false;
    }
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
