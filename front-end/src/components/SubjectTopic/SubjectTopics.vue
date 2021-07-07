<template>
  <div class="topics">
    <div v-if="isOwner" class="add-theme">
      <CustomText
        variant="paragraph"
        color="#0C4B9A"
        :custom-style="{ cursor: 'pointer' }"
      >
        <div @click="addTopic">
          + Добавить тему
        </div>
      </CustomText>
    </div>
    <div v-if="topics.length === 0" class="pt-2 pl-2">
      <CustomText v-if="!isOwner" variant="paragraph">
        Этот раздел пока пуст
      </CustomText>
    </div>
    <Draggable
      :list="topics"
      v-bind="dragOptions"
      :disabled="!isOwner"
      @change="({ moved }) => updateOrder(moved.element.id, moved.newIndex)"
    >
      <transition-group type="transition" name="flip-list">
        <SubjectTopic
          v-for="(item, index) in topics"
          :key="item.id"
          :topic="item"
          :is-owner="isOwner"
          class="topic"
          :index="index + 1"
          @update="onTopicUpdate(index, $event)"
          @delete="deleteTopic"
          @change="acceptNewTopic"
        />
      </transition-group>
    </Draggable>
  </div>
</template>

<script>
import CustomText from "@/common/CustomText";
import {
  addTopics,
  deleteTopics,
  editTopics,
  getTopics,
  changeTopicOrder,
} from "@/api/topic";
import Draggable from "vuedraggable";
import { UserModule } from "@/store";
import SubjectTopic from "./SubjectTopic.vue";

export default {
  name: "SubjectTopics",
  components: {
    CustomText,
    SubjectTopic,
    Draggable,
  },
  // todo
  // eslint-disable-next-line vue/require-prop-types
  props: ["sectionId", "isOwner"],
  data() {
    return {
      topics: [],
      editTopicId: null,
    };
  },
  computed: {
    userId() { return UserModule.userId; },
    dragOptions() {
      return {
        animation: 200,
        group: "description",
        disabled: false,
        ghostClass: "ghost",
        easing: "cubic-bezier(1, 0.5, 0.8, 1)",
      };
    },
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      await getTopics(this.sectionId).then(res => {
        this.topics = res.data.topics;
      });
    },
    acceptNewTopic(data) {
      editTopics(data.id, data.newData);
    },
    deleteTopic(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить раздел? Это действие не обратимо.",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(() => {
        deleteTopics(id).then(() => {
          this.topics = this.topics.filter(item => item.id !== id);
        });
      });
    },
    addTopic() {
      const dataToSend = {
        title: "Новая тема",
        section: this.sectionId,
        annotation: "Введите аннотацию",
      };
      addTopics(dataToSend).then(res => {
        this.topics.unshift(res.data);
      });
    },
    updateOrder(topicId, newOrder) {
      changeTopicOrder(topicId, newOrder);
    },
    onTopicUpdate(index, newData) {
      this.topics = [
        ...this.topics.slice(0, index),
        newData,
        ...this.topics.slice(index + 1),
      ];
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
