<template>
  <el-col :offset="2" :span="20" class="scienceWork">
    <el-row class="pageTitle">
      <el-col>
        <div class="d-flex align-items-center justify-content-between">
          <div class="d-flex align-items-center">
            <img
              src="../../assets/scienceWorks/previous.svg"
              @click="backToSubjects"
              style="position: absolute; left: -40px; cursor: pointer"
              height="22px"
              alt="назад"
            />
            {{ subject }}
          </div>
          <CustomText
            v-if="userId === subjectOwnerId"
            @click="addTopic"
            variant="paragraph"
            color="#0C4B9A"
            :custom-style="{ cursor: 'pointer' }"
          >
            <div @click="addTopic">+ Добавить раздел</div>
          </CustomText>
        </div>
      </el-col>
    </el-row>
    <div class="subjectsWrapper">
      <div class="subjectsMenu">
        <div class="parts">
          <div class="parts-all">Все разделы</div>
          <div
            v-for="(part, index) in subjectInfo"
            :key="part.id"
            class="part"
            @click="selectPart(part.id, index)"
            :id="part.id"
          >
            {{ part.title }}
          </div>
        </div>
      </div>
      <div class="subjects">
        <SearchForMaterials placeholder="Введите название темы или документа" />
        <div class="main-parts">
          <draggable
            :list="subjectInfo"
            v-bind="dragOptions"
            @start="dragging = true"
            @end="dragging = false"
            :disabled="userId !== subjectOwnerId"
            @change="
              ({ moved }) => updateOrder(moved.element.id, moved.newIndex)
            "
          >
            <transition-group type="transition" name="flip-list">
              <div
                v-for="mainPart in subjectInfo"
                :key="mainPart.id"
                class="main-part"
                ref="cards"
              >
                <div class="main-part-title" style="width: 100%">
                  <img
                    height="12"
                    class="mr-2"
                    src="../../assets/icons/drag.svg"
                    alt=""
                  />

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
                      class="title-input"
                      style="height: 30px !important"
                      v-model="mainPart.title"
                      clearable
                    />
                  </div>

                  <div class="buttons" v-if="userId === subjectOwnerId">
                    <img
                      v-if="editTitleIndex === mainPart.id"
                      @click="acceptNewTitle(mainPart.id)"
                      class="grow"
                      src="../../assets/subject/accept.svg"
                      alt=""
                    />
                    <template v-else>
                      <img
                        @click="editTitle(mainPart.id)"
                        class="grow"
                        src="../../assets/subject/edit.svg"
                        alt=""
                      />
                      <img
                        @click="deleteSection(mainPart.id)"
                        class="grow"
                        src="../../assets/subject/close.svg"
                        alt=""
                      />
                    </template>
                  </div>
                </div>

                <SubjectTopics
                  v-show="openedCards.includes(mainPart.id)"
                  :sectionId="mainPart.id"
                  :isOwner="userId === subjectOwnerId"
                />
              </div>
            </transition-group>
          </draggable>
        </div>
      </div>
    </div>
  </el-col>
</template>

<script>
import SearchForMaterials from "@/components/Search/SearchForMaterials";
import SubjectTopics from "@/components/SubjectTopic/SubjectTopics.vue";
import draggable from "vuedraggable";
import {
  addSection,
  deleteSection,
  editSectionTitle,
  changeSectionOrder,
  getSubject,
} from "@/api/subjects";
import { mapActions, mapState } from "vuex";
import CustomText from "@/common/CustomText";

export default {
  name: "Subject",
  async mounted() {
    await this.fetchData(this.$route.params.subjectId);
    console.log("this.$route", this.$route);
    this.openedCards = [...this.openedCards, +this.$route.query.section];
  },
  data() {
    return {
      subject: null,
      subjectId: null,
      subjectInfo: null,
      editTitleIndex: null,
      subjectOwnerId: null,
      openedCards: [],
    };
  },
  components: {
    draggable,
    CustomText,
    SearchForMaterials,
    SubjectTopics,
  },
  computed: {
    ...mapState({
      subjects: (state) => state.subjects.subjects,
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
  watch: {
    elemData: {
      deep: false,
      handler() {
        console.log("!!!");
      },
    },
  },
  methods: {
    ...mapActions({
      setSubjects: "subjects/setSubjects",
    }),
    deleteSection(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить раздел? Это действие не обратимо.",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        }
      ).then(() => {
        deleteSection(id).then(() => {
          this.subjectInfo = this.subjectInfo.filter((item) => item.id !== id);
        });
      });
    },
    acceptNewTitle(id) {
      let title = this.subjectInfo.find((item) => item.id === id).title;

      if (!title) {
        this.$message.warning("Пожалуйста, заполните название раздела");
        return;
      }

      const sendData = {
        title: title,
        subject: this.subjectId,
      };
      editSectionTitle(id, sendData);
      this.editTitleIndex = null;
    },
    editTitle(id) {
      this.editTitleIndex = id;
    },
    addTopic() {
      const dataToSend = {
        title: `Новый раздел`,
        subject: this.subjectId,
      };
      addSection(dataToSend).then((res) => {
        this.subjectInfo.push(res.data);
      });
    },
    togglePart(id) {
      const index = this.openedCards.indexOf(id);

      if (index !== -1) {
        this.openedCards = this.openedCards.filter((item) => item !== id);
      } else {
        this.openedCards = [...this.openedCards, id];
      }
    },
    selectPart(id, index) {
      if (this.openedCards.indexOf(id)) {
        this.openedCards = [...this.openedCards, id];
      }

      this.$nextTick(() =>
        this.$refs.cards[index].scrollIntoView({
          block: "start",
          inline: "nearest",
          behavior: "smooth",
        })
      );
    },
    async fetchData(subjectId) {
      this.subjectId = subjectId;
      await getSubject({ id: subjectId })
        .then((response) => {
          this.subject = response.data.title;
          this.subjectInfo = response.data.sections;
          this.subjectOwnerId = response.data.user.id;
        })
        .catch(() => {
          // eslint-disable-next-line no-console
          console.log("Данные по предмету не указаны");
        });
    },
    backToSubjects() {
      this.$router.push({ path: `/subjects/` });
    },
    updateOrder(sectionId, newOrder) {
      changeSectionOrder(sectionId, newOrder);
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
