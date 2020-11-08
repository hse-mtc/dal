<template>
  <el-col :offset="2" :span="20" class="scienceWork">
    <el-row class="pageTitle">
      <el-col :span="23">
        <div class="d-flex align-items-center justify-content-between">
          Учебно-методические материалы
          <CustomText variant="paragraph" :custom-style="{color: '#0C4B9A', cursor: 'pointer'}">
            <div @click="windowModal = true">+Добавить дисциплину</div>
          </CustomText>
        </div>
      </el-col>
    </el-row>
    <el-row class="search">
      <el-col :span="23">
        <SearchForSubjects placeholder="Введите название предмета"/>
        <el-row v-if="filteredSubjects.length !== 0" class="subjects" :gutter="20">
          <el-col
              :span="12"
              v-for="(item, index) in filteredSubjects"
              :key="index"
              class="subjects-wrapper mt-5"
          >
            <el-col>
              <SubjectCard
                  :id="item.id"
                  :annotation="item.annotation"
                  :title="item.title"
                  :isMySubject="userId === item.user.id"
                  owner="Тест Тестов Тестович"
                  @deleted="deletedSubject"
                  @edit="editSubject"
              />
            </el-col>
          </el-col>
        </el-row>
        <div v-else>Предметов с таким названием не найдено.</div>
      </el-col>
    </el-row>

    <ModalWindow :opened="windowModal" @closeModal="closeModal">
      <CustomText :customStyle="{'font-weight': 'normal'}" variant="header">Добавление дисциплины</CustomText>
      <ElForm
          class="subject-form"
          ref="subjectForm"
          :rules="rules"
          :model="subjectForm"
          label-width="180px"
      >
        <ElFormItem label="Название дисциплины" prop="title">
          <ElInput placeholder="Введите название" v-model="subjectForm.title"/>
        </ElFormItem>

        <ElFormItem label="Аннотация" prop="annotation">
          <ElInput
              placeholder="Введите текст аннотации"
              v-model="subjectForm.annotation"
              type="textarea"
              :autosize="{ minRows: 2 }"
          />
        </ElFormItem>
        <ElFormItem>
          <ElButton type="primary" @click="submitForm('subjectForm')">Отправить</ElButton>
          <ElButton @click="closeModal">Отменить</ElButton>
        </ElFormItem>
      </ElForm>
    </ModalWindow>
  </el-col>
</template>

<script>
import {getSubjects} from "@/api/subjects";
import SubjectCard from "@/components/SubjectCard/SubjectCard";
import {mapState, mapActions} from "vuex";
import SearchForSubjects from "@/components/Search/SearchForSubjects";
import ModalWindow from "@/components/ModalWindow/ModalWindow";
import CustomText from "@/common/CustomText";
import {upsertSubject} from "@/api/subject";

export default {
  name: "",
  components: {
    CustomText,
    ModalWindow,
    SubjectCard,
    SearchForSubjects,
  },
  data() {
    return {
      windowModal: false,
      subjectForm: {
        id: null,
        title: "",
        annotation: "",
      },
      rules: {
        title: [{required: true, message: "Обязательное поле"}],
        annotation: [{required: true, message: "Обязательное поле"}],
      },
    };
  },
  computed: {
    ...mapState({
      userId: (state) => state.app.userId,
      subjects: (state) => state.subjects.subjects,
    }),
    filteredSubjects() {
      if (this.$route.query.subjectsSearch) {
        const subjectsSearch = this.$route.query.subjectsSearch;
        if (subjectsSearch.trim()) {
          return this.subjects.filter((item) =>
              item.title.toUpperCase().includes(subjectsSearch.toUpperCase())
          );
        } else {
          return this.subjects;
        }
      } else {
        return this.subjects;
      }
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    ...mapActions({
      setSubjects: "subjects/setSubjects",
      deleteSubject: "subjects/deleteSubject",
      upsertSubject: "subjects/upsertSubject"
    }),
    submitForm(name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          upsertSubject(this.subjectForm).then((res) => {
            this.upsertSubject(res.data)
            this.closeModal()
          }).catch(() => {
            console.log("Ошибка отправки формы")
          })
        }
      });
    },
    editSubject(id) {
      const { title, annotation } = this.subjects.find(subject => subject.id === id);
      this.subjectForm = { id, title, annotation };
      this.windowModal = true;
    },
    closeModal() {
      this.subjectForm = {
        id: null,
        title: "",
        annotation: "",
      }
      this.windowModal = false
    },
    fetchData() {
      if (this.subjects.length === 0) {
        getSubjects()
            .then((response) => {
              this.setSubjects(response.data)
            })
            .catch(() => {
              console.log("Данные по предметам не указаны");
            });
      }
    },
    deletedSubject(id) {
      this.deleteSubject(id)
    }
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
