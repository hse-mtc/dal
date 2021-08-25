<template>
  <div
    :key="sectionInfo.id"
    ref="cards"
    class="main-part"
  >
    <div :class="$style.header">
      <img
        height="12"
        class="mr-2"
        src="../../../assets/icons/drag.svg"
        alt=""
      >

      <div v-if="!isEditing" @click="opened = !opened">
        {{ sectionInfo.title }}
      </div>
      <div
        v-else
        :class="$style.titleInputWrapper"
        @keyup.enter="acceptNewTitle"
      >
        <el-input
          v-model="sectionInfo.title"
          :class="$style.titleInput"
          clearable
          size="mini"
        />
      </div>

      <div :class="$style.buttons">
        <img
          v-if="isEditing"
          :class="$style.button"
          src="../../../assets/subject/accept.svg"
          alt=""
          @click="acceptNewTitle"
        >
        <template v-else>
          <AZGuard
            :permissions="['sections.patch.all', {
              codename: 'sections.patch.self',
              validator: () => userId === subjectOwnerId,
            }]"
          >
            <img
              :class="$style.button"
              src="../../../assets/subject/edit.svg"
              alt=""
              @click="editTitle"
            >
          </AZGuard>

          <AZGuard
            :permissions="['sections.delete.all', {
              codename: 'sections.delete.self',
              validator: () => userId === subjectOwnerId,
            }]"
          >
            <img
              :class="$style.button"
              src="../../../assets/subject/close.svg"
              alt=""
              @click="deleteSection"
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
      <TopicsCards
        :shown="opened"
        :section-id="sectionInfo.id"
      />
    </AZGuard>
  </div>
</template>

<script>
import { Component, ModelSync, Prop } from "vue-property-decorator";

import { SubjectsModule, UserModule } from "@/store";

import SubjectTopics from "@/components/SubjectTopic/SubjectTopics.vue";
import TopicsCards from "@/components/@Subjects/SubjectPage/TopicsCards.vue";

@Component({
  name: "SectionCard",
  components: { SubjectTopics, TopicsCards },
})
class SectionCard {
  @ModelSync("isOpen", "change", { required: true }) opened
  @Prop({ required: true }) sectionInfo

  isEditing = false

  get sections() { return SubjectsModule.currentSections; }
  get userId() { return UserModule.userId; }
  get subjectOwnerId() { return SubjectsModule.currentSubject.user.id; }

  editTitle() {
    this.isEditing = true;
  }

  acceptNewTitle() {
    SubjectsModule.updateSectionTitle(this.sectionInfo);

    this.isEditing = false;
  }

  async deleteSection() {
    await this.$confirm(
      "Вы уверены, что хотите удалить раздел? Это действие не обратимо.",
      "Подтверждение",
      {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      },
    );

    SubjectsModule.deleteSection(this.sectionInfo.id);
  }
}

export default SectionCard;
</script>

<style lang="scss" module>
.root {}

.header {
  display: flex;
  align-items: center;
  padding: 10px 10px 10px 0;
  border-bottom: 1px solid #0c4b9a;
  font-size: 20px;
  cursor: pointer;

  .title {
    &Input {
      flex: 1;
      font-size: 20px;

      :global(.el-input__inner) {
        padding: 0;
      }

      &Wrapper {
        display: flex;
        flex: 1;
        margin-right: 20px;
      }
    }
  }

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
</style>
