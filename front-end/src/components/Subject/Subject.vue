<template>
  <el-col :offset="1" :span="22" class="scienceWork">
    <el-row class="pageTitle">
      <el-col>
        <div class="d-flex align-items-center justify-content-between">
          <div class="d-flex align-items-center">
            <img
              src="../../assets/scienceWorks/previous.svg"
              style="position: absolute; left: -40px; cursor: pointer"
              height="22px"
              alt="назад"
              @click="backToSubjects"
            >
            {{ subject }}
          </div>
          <AZGuard
            :permissions="['sections.post.all', {
              codename: 'sections.post.self',
              validator: () => userId === subjectOwnerId,
            }]"
          >
            <CustomText
              variant="paragraph"
              color="#0C4B9A"
              :custom-style="{ cursor: 'pointer' }"
              @click="addTopic"
            >
              <div @click="addTopic">
                + Добавить раздел
              </div>
            </CustomText>
          </AZGuard>
        </div>
      </el-col>
    </el-row>
    <div class="subjectsWrapper">
      <div class="subjectsMenu">
        <div class="parts">
          <div class="parts-all">
            Все разделы
          </div>
          <div
            v-for="(part, index) in subjectInfo"
            :id="part.id"
            :key="part.id"
            class="part"
            @click="selectPart(part.id, index)"
          >
            {{ part.title }}
          </div>
        </div>
      </div>
      <div class="subjects">
        <!--        <SearchForMaterials placeholder="Введите название темы или документа" />-->
        <div class="main-parts">
          <draggable
            :list="subjectInfo"
            v-bind="dragOptions"
            :disabled="disableDrag"
            @start="dragging = true"
            @end="dragging = false"
            @change="
              ({ moved }) => updateOrder(moved.element.id, moved.newIndex)
            "
          >
            <transition-group type="transition" name="flip-list">
              <div
                v-for="mainPart in subjectInfo"
                :key="mainPart.id"
                ref="cards"
                class="main-part"
              >
                <div
                  class="main-part-title"
                  style="
                    width: 100%;
                    display: flex;
                    justify-content: flex-start;
                  "
                >
                  <img
                    height="12"
                    class="mr-2"
                    src="../../assets/icons/drag.svg"
                    alt=""
                  >

                  <div
                    v-if="editTitleIndex !== mainPart.id"
                    style="width: 90%"
                    @click="togglePart(mainPart.id)"
                  >
                    {{ mainPart.title }}
                  </div>
                  <div
                    v-else
                    style="width: 90%"
                    @keyup.enter="acceptNewTitle(mainPart.id)"
                  >
                    <el-input
                      v-model="mainPart.title"
                      class="title-input"
                      style="height: 30px !important"
                      clearable
                    />
                  </div>

                  <div class="buttons">
                    <img
                      v-if="editTitleIndex === mainPart.id"
                      class="grow"
                      src="../../assets/subject/accept.svg"
                      alt=""
                      @click="acceptNewTitle(mainPart.id)"
                    >
                    <template v-else>
                      <AZGuard
                        :permissions="['sections.patch.all', {
                          codename: 'sections.patch.self',
                          validator: () => userId === subjectOwnerId,
                        }]"
                      >
                        <img
                          class="grow"
                          src="../../assets/subject/edit.svg"
                          alt=""
                          @click="editTitle(mainPart.id)"
                        >
                      </AZGuard>
                      <AZGuard
                        :permissions="['sections.delete.all', {
                          codename: 'sections.delete.self',
                          validator: () => userId === subjectOwnerId,
                        }]"
                      >
                        <img
                          class="grow"
                          src="../../assets/subject/close.svg"
                          alt=""
                          @click="deleteSection(mainPart.id)"
                        >
                      </AZGuard>
                    </template>
                  </div>
                </div>
                <AZGuard
                  :permissions="['topics.get.all', {
                    codename: 'topics.get.self',
                    validator: () => userId === subjectOwnerId },
                  ]"
                >
                  <SubjectTopics
                    v-show="openedCards.includes(mainPart.id)"
                    :section-id="mainPart.id"
                    :subject-owner-id="subjectOwnerId"
                  />
                </AZGuard>
              </div>
            </transition-group>
          </draggable>
        </div>
      </div>
    </div>
  </el-col>
</template>

<script>
import { Component } from "vue-property-decorator";
import SearchForMaterials from "@/components/Search/SearchForMaterials";
import SubjectTopics from "@/components/SubjectTopic/SubjectTopics.vue";
import draggable from "vuedraggable";
import { hasPermission } from "@/utils/permissions";

import {
  addSection,
  deleteSection,
  editSectionTitle,
  changeSectionOrder,
  getSubject,
} from "@/api/subjects";
import CustomText from "@/common/CustomText";
import { SubjectsModule, UserModule } from "@/store";

@Component({
  name: "Subject",
  components: {
    draggable,
    CustomText,
    SearchForMaterials,
    SubjectTopics,
  },
  computed: {
    userId() {
      return UserModule.userId;
    },
    disableDrag() {
      return !hasPermission([{
        codename: "sections-order.patch.all", // TODO: add sections-order.patch.self to BE and use validator with it on FE
        validator: () => this.userId === this.subjectOwnerId,
      }]);
    },
  },
})
class MyDisciplines {
  subject = null
  subjectId = null
  editTitleIndex = null
  subjectOwnerId = null
  openedCards = []

  get subjects() { return SubjectsModule.subjects; }
  get subjectInfo() { return SubjectsModule.currentSections; }
  get dragOptions() {
    return {
      animation: 200,
      group: "description",
      disabled: false,
      ghostClass: "ghost",
      easing: "cubic-bezier(1, 0.5, 0.8, 1)",
    };
  }

  async mounted() {
    await this.fetchData(this.$route.params.subjectId);
    this.openedCards = [...this.openedCards, +this.$route.query.section];
  }

  deleteSection(id) {
    this.$confirm(
      "Вы уверены, что хотите удалить раздел? Это действие не обратимо.",
      "Подтверждение",
      {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      },
    ).then(() => {
      deleteSection(id).then(() => {
        this.subjectInfo = this.subjectInfo.filter(item => item.id !== id);
      });
    });
  }

  acceptNewTitle(id) {
    const { title } = this.subjectInfo.find(item => item.id === id);

    if (!title) {
      this.$message.warning("Пожалуйста, заполните название раздела");
      return;
    }

    const sendData = {
      title,
      subject: this.subjectId,
    };
    editSectionTitle(id, sendData);
    this.editTitleIndex = null;
  }

  editTitle(id) {
    this.editTitleIndex = id;
  }

  addTopic() {
    const dataToSend = {
      title: "Новый раздел",
      subject: this.subjectId,
    };
    addSection(dataToSend).then(res => {
      this.subjectInfo.push(res.data);
    });
  }

  togglePart(id) {
    const index = this.openedCards.indexOf(id);

    if (index !== -1) {
      this.openedCards = this.openedCards.filter(item => item !== id);
    } else {
      this.openedCards = [...this.openedCards, id];
    }
  }

  selectPart(id, index) {
    if (this.openedCards.indexOf(id)) {
      this.openedCards = [...this.openedCards, id];
    }

    this.$nextTick(() => this.$refs.cards[index].scrollIntoView({
      block: "start",
      inline: "nearest",
      behavior: "smooth",
    }));
  }

  async fetchData(subjectId) {
    this.subjectId = subjectId;
    await getSubject({ id: subjectId })
      .then(response => {
        this.subject = response.data.title;
        // this.subjectInfo = response.data.sections;
        this.subjectOwnerId = response.data.user.id;
      })
      .catch(() => {
        // eslint-disable-next-line no-console
        console.log("Данные по предмету не указаны");
      });
  }

  backToSubjects() {
    this.$router.push({ name: "Subjects" });
  }

  updateOrder(sectionId, newOrder) {
    changeSectionOrder(sectionId, newOrder);
  }
}

export default MyDisciplines;
</script>

<style scoped lang="scss">
@import "style";
</style>
