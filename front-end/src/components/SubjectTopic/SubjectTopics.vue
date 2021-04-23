<template>
  <div class="topics">
    <el-button v-if="isOwner" @click="addTopic" class="add-theme">
      <CustomText
        variant="paragraph"
        color="#FFF"
        :custom-style="{ fontWeight: 600 }"
      >
        Добавить тему
      </CustomText>
    </el-button>
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
          :isOwner="isOwner"
          class="topic"
          :index="index + 1"
          @delete="deleteTopic"
        />
      </transition-group>
    </Draggable>
  </div>
</template>

<script>
import SubjectTopic from "./SubjectTopic.vue";
import CustomText from "@/common/CustomText";
import {
  addTopics,
  deleteTopics,
  editTopics,
  getTopics,
  changeTopicOrder,
} from "@/api/topic";
import { mapState } from "vuex";
import Draggable from "vuedraggable";

export default {
  name: "SubjectTopics",
  components: {
    CustomText,
    SubjectTopic,
    Draggable,
  },
  props: ["sectionId", "isOwner"],
  data() {
    return {
      topics: [],
      editTopicId: null,
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.app.userId,
    }),
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
      await getTopics(this.sectionId).then((res) => {
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
        }
      ).then(() => {
        deleteTopics(id).then(() => {
          this.topics = this.topics.filter((item) => item.id !== id);
        });
      });
    },
    addTopic() {
      const dataToSend = {
        title: "Новая тема",
        section: this.sectionId,
        annotation: "Введите аннотацию",
      };
      addTopics(dataToSend).then((res) => {
        this.topics.push(res.data);
      });
    },
    updateOrder(topicId, newOrder) {
      changeTopicOrder(topicId, newOrder);
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
