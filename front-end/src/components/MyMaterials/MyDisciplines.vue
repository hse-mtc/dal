<template>
  <el-col :span="24">
    <div
      v-if="mySubjects === null"
      v-loading="loading"
      class="requests__loader"
    />
    <el-row
      v-if="mySubjects && mySubjects.length > 0"
      class="subjects"
      :gutter="20"
    >
      <el-col
        v-for="(item, index) in mySubjects"
        :key="index"
        :span="12"
        class="subjects-wrapper mt-5"
      >
        <el-col>
          <SubjectCard
            :id="item.id"
            :annotation="item.annotation"
            :title="item.title"
            :is-my-subject="true"
            :owner="`${item.user.email}`"
          />
        </el-col>
      </el-col>
    </el-row>
    <div v-if="mySubjects && mySubjects.length === 0">
      У вас пока нет добавленных дисциплин
    </div>
  </el-col>
</template>

<script>
import { Component } from "vue-property-decorator";
import { getSubjects } from "@/api/subjects";
import CustomText from "@/common/CustomText";
import ModalWindow from "@/components/ModalWindow/ModalWindow";
import SubjectCard from "@/components/@Subjects/SubjectsPage/SubjectCard/index.vue";
import { UserModule } from "@/store";

@Component({
  name: "MyDisciplines",
  components: {
    CustomText,
    ModalWindow,
    SubjectCard,
  },
  computed: {
    userId() { return UserModule.userId; },
  },
})
class MyDisciplines {
  mySubjects = null
  loading = false

  created() {
    this.fetchData();
  }

  fetchData() {
    this.loading = true;
    getSubjects({ user: this.userId }).then(res => {
      this.mySubjects = res.data;
      this.loading = false;
    });
  }
}

export default MyDisciplines;
</script>

<style scoped lang="scss"></style>
