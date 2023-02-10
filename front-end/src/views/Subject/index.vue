<template>
  <div :class="$style.root">
    <div :class="$style.header">
      <router-link
        :to="{ name: 'Subjects' }"
        :class="$style.arrow"
      >
        <i @click="clear" class="el-icon-arrow-left" />
      </router-link>
      <h1 :class="$style.title">
        {{ subjectInfo.title }}
      </h1>
      <AZGuard
        :permissions="['sections.post.all', {
          codename: 'sections.post.self',
          validator: () => userId === subjectOwnerId,
        }]"
      >
        <el-button
          type="text"
          :class="$style.addButton"
          @click="addSection"
        >
          + Добавить раздел
        </el-button>
      </AZGuard>
    </div>

    <div :class="$style.content">
      <div :class="$style.menuWrapper">
        <Menu :class="$style.menu" />
      </div>
      <div :class="$style.sectionsWrapper">
        <AZGuard
          :permissions="['sections.post.all', {
            codename: 'sections.post.self',
            validator: () => userId === subjectOwnerId,
          }]"
        >
          <el-button
            type="primary"
            :class="$style.bigAddButton"
            @click="addSection"
          >
            + Добавить раздел
          </el-button>
        </AZGuard>

        <SectionsCards :class="$style.sections" />
      </div>
    </div>
  </div>
</template>

<script>
import { SubjectsModule } from "@/store";
import { Component, Vue } from "vue-property-decorator";

import Menu from "@/components/@Subjects/SubjectPage/SectionsMenu.vue";
import SectionCard from "@/components/@Subjects/SubjectPage/SectionCard.vue";
import SectionsCards from "@/components/@Subjects/SubjectPage/SectionsCards.vue";

@Component({
  name: "SubjectPage",
  components: {
    Menu,
    SectionCard,
    SectionsCards,
  },
})
class SubjectPage extends Vue {
  get subjectInfo() { return SubjectsModule.currentSubject; }
  get sections() { return SubjectsModule.currentSections; }

  mounted() {
    this.subjectInfo.title = "";
    SubjectsModule.setCurrentSubjectId(this.$route.params.subjectId);
  }

  clear() {
    this.sections.length = 0;
  }

  async addSection() {
    const res = await SubjectsModule.addSection({
      title: "Новый раздел",
      subject: SubjectsModule.subjectId,
    });

    if (res) {
      this.$nextTick(() => {
        const elem = document.getElementById(`section-${this.sections[this.sections.length - 1].id}`);

        if (elem) {
          elem.scrollIntoView({
            block: "start",
            inline: "nearest",
            behavior: "smooth",
          });
        }
      });
    }
  }
}

export default SubjectPage;
</script>

<style lang="scss" module>
.root {
  padding: 50px;

  @media screen and (max-width: 767px) {
    padding: 20px 10px;
  }
}

.header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 50px;

  .arrow {
    margin-right: 15px;
    color: #000;
    font-size: 40px;
    line-height: 48px;
    cursor: pointer;

    &:hover {
      opacity: 0.7;
      text-decoration: none;
    }

    @media screen and (max-width: 767px) {
      display: flex;
      align-items: center;

      &::after {
        content: "К дисциплинам";
        font-size: 18px;
      }
    }
  }

  .title {
    margin: 0 20px 0 0;
  }

  .addButton {
    margin-left: auto;
    font-size: 18px;
    color: #0c4b9a;

    @media screen and (max-width: 800px) {
      display: none;
    }
  }
}

.content {
  display: flex;

  .menu {
    position: sticky;
    top: 10px;

    &Wrapper {
      margin-right: 20px;

      @media screen and (max-width: 767px) {
        display: none;
      }
    }
  }

  .sectionsWrapper {
    width: 100%;

    .bigAddButton {
      width: 100%;
      display: none;

      @media screen and (max-width: 800px) {
        display: block;
      }
    }
  }
}

</style>
