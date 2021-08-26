<template>
  <div :class="$style.root">
    <div :class="$style.header">
      <router-link
        :to="{ name: 'Subjects' }"
        :class="$style.arrow"
      >
        <i class="el-icon-arrow-left" />
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

      <SectionsCards :class="$style.sections" />
    </div>
  </div>
</template>

<script>
import { SubjectsModule } from "@/store";
import { Component } from "vue-property-decorator";

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
class SubjectPage {
  get subjectInfo() { return SubjectsModule.currentSubject; }
  get sections() { return SubjectsModule.currentSections; }

  mounted() {
    SubjectsModule.setCurrentSubjectId(this.$route.params.subjectId);
  }

  addSection() {
    SubjectsModule.addSection({
      title: "Новый раздел",
      subject: SubjectsModule.subjectId,
    });
  }
}

export default SubjectPage;
</script>

<style lang="scss" module>
.root {
  padding: 50px;
}

.header {
  display: flex;
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
    }
  }

  .title {
    margin: 0;
  }

  .addButton {
    margin-left: auto;
    font-size: 18px;
    color: #0c4b9a;
  }
}

.content {
  display: flex;

  .menu {
    position: sticky;
    top: 10px;

    &Wrapper {
      margin-right: 20px;
    }
  }

  .sections {
    width: 100%;
  }
}

</style>
