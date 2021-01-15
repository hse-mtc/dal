<template>
  <div class="topics" style="display: none">
    <el-button v-if="isOwner" @click="addTopic" class="add-theme">
      <CustomText
        variant="paragraph"
        color="#FFF"
        :custom-style="{ fontWeight: 600 }"
        >Добавить тему
      </CustomText>
    </el-button>
    <div v-if="topics.length === 0" class="pt-2 pl-2">
      <CustomText v-if="!isOwner" variant="paragraph"
        >Этот раздел пока пуст
      </CustomText>
    </div>
    <draggable
      :list="topics"
      v-bind="dragOptions"
      @change="({moved}) => updateOrder(moved.element.id, moved.newIndex)"
    >
      <transition-group type="transition" name="flip-list">
        <div v-for="(item, index) in topics" :key="index" class="topic">
          <div class="topic-title">
            <div class="d-flex align-items-center">
              <img
                height="12"
                class="mr-2"
                src="../../assets/icons/drag.svg"
                alt=""
              />
              <div>Тема №{{ index + 1 }}</div>
            </div>
            <div class="buttons" v-if="isOwner">
              <img
                v-if="editTopicId === item.id"
                @click="acceptNewTopic(item.id)"
                class="grow"
                src="../../assets/subject/accept.svg"
                alt=""
              />
              <img
                v-if="editTopicId === null"
                @click="editTopic(item.id)"
                class="grow"
                src="../../assets/subject/edit.svg"
                alt=""
              />
              <img
                v-if="editTopicId === null"
                @click="deleteTopic(item.id)"
                class="grow"
                src="../../assets/subject/close.svg"
                alt=""
              />
              <img
                v-if="editTopicId === null"
                @click="downloadTopic(item.id)"
                class="grow"
                src="../../assets/subject/download.svg"
                alt=""
              />
            </div>
          </div>

          <div v-if="editTopicId !== item.id">
            <CustomText variant="header" class="topic-content">
              {{ item.title }}
            </CustomText>
          </div>
          <div v-if="editTopicId === item.id" style="width: 90%">
            <el-input class="title-input" v-model="item.title" clearable />
          </div>

          <div v-if="editTopicId !== item.id">
            <CustomText variant="paragraph">
              {{ item.annotation }}
            </CustomText>
          </div>
          <div
            v-if="editTopicId === item.id"
            style="width: 90%; margin-top: 10px"
          >
            <el-input
              type="textarea"
              :autosize="{ minRows: 2, maxRows: 4 }"
              class="title-input"
              v-model="item.annotation"
              clearable
            />
          </div>

          <div class="topic-files">
            <ClassMaterials
              :isOwner="isOwner"
              title="LE"
              :topic="item.id"
              :materials="
                (item.class_materials && item.class_materials.lectures) || []
              "
            />
            <ClassMaterials
              :isOwner="isOwner"
              title="SE"
              :topic="item.id"
              :materials="
                (item.class_materials && item.class_materials.seminars) || []
              "
            />
            <ClassMaterials
              :isOwner="isOwner"
              title="GR"
              :topic="item.id"
              :materials="
                (item.class_materials && item.class_materials.groups) || []
              "
            />
            <ClassMaterials
              :isOwner="isOwner"
              title="PR"
              :topic="item.id"
              :materials="
                (item.class_materials && item.class_materials.practices) || []
              "
            />
          </div>
        </div>
      </transition-group>
    </draggable>
  </div>
</template>

<script>
import ClassMaterials from "./ClassMaterials";
import CustomText from "@/common/CustomText";
import {
  addTopics,
  deleteTopics,
  editTopics,
  getTopics,
  changeTopicOrder,
} from "@/api/topic";
import { mapState } from "vuex";
import draggable from "vuedraggable";

export default {
  name: "",
  components: { CustomText, ClassMaterials, draggable },
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
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      getTopics(this.sectionId).then((res) => {
        this.topics = res.data.topics;
      });
    },
    editTopic(id) {
      this.editTopicId = id;
    },
    acceptNewTopic(id) {
      let title;
      let annotation;

      if (this.topics.find((item) => item.id === id).title) {
        title = this.topics.find((item) => item.id === id).title;
      } else {
        this.$message.warning("Пожалуйста, заполните название темы");
        return;
      }

      if (this.topics.find((item) => item.id === id).annotation) {
        annotation = this.topics.find((item) => item.id === id).annotation;
      } else {
        this.$message.warning("Пожалуйста, заполните аннотацию для темы");
        return;
      }

      const dataToSend = {
        title: title,
        annotation: annotation,
        section: this.sectionId,
      };
      editTopics(id, dataToSend);
      this.editTopicId = null;
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
      changeTopicOrder(topicId, newOrder)
    }
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
