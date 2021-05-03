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
            @deleted="deletedSubject"
            @edit="editSubject"
          />
        </el-col>
      </el-col>
    </el-row>
    <div v-if="mySubjects && mySubjects.length === 0">
      У вас пока нет добавленных дисциплин
    </div>

    <ModalWindow :opened="windowModal" @closeModal="closeModal">
      <CustomText :custom-style="{'font-weight': 'normal'}" variant="header">
        Добавление дисциплины
      </CustomText>
      <ElForm
        ref="subjectForm"
        class="subject-form"
        :rules="rules"
        :model="subjectForm"
        label-width="180px"
      >
        <ElFormItem label="Название дисциплины" prop="title">
          <ElInput v-model="subjectForm.title" placeholder="Введите название" />
        </ElFormItem>

        <ElFormItem label="Аннотация" prop="annotation">
          <ElInput
            v-model="subjectForm.annotation"
            placeholder="Введите текст аннотации"
            type="textarea"
            :autosize="{minRows: 2}"
          />
        </ElFormItem>
        <ElFormItem>
          <ElButton type="primary" @click="submitForm('subjectForm')">
            Отправить
          </ElButton>
          <ElButton @click="closeModal">
            Отменить
          </ElButton>
        </ElFormItem>
      </ElForm>
    </ModalWindow>
  </el-col>
</template>

<script>
import { mapActions, mapState } from "vuex";
import { getSubjects, upsertSubject } from "@/api/subjects";
import CustomText from "@/common/CustomText";
import ModalWindow from "@/components/ModalWindow/ModalWindow";
import SubjectCard from "@/components/SubjectCard/SubjectCard";

export default {
  name: "MyDisciplines",
  components: {
    CustomText,
    ModalWindow,
    SubjectCard,
  },
  data() {
    return {
      mySubjects: null,
      windowModal: false,
      loading: false,
      subjectForm: {
        id: null,
        title: "",
        annotation: "",
      },
      rules: {
        title: [{ required: true, message: "Обязательное поле" }],
        annotation: [{ required: true, message: "Обязательное поле" }],
      },
    };
  },
  computed: {
    ...mapState({
      userId: state => state.app.userId,
    }),
  },
  created() {
    this.fetchData();
  },
  methods: {
    ...mapActions({
      setSubjects: "subjects/setSubjects",
      deleteSubject: "subjects/deleteSubject",
      upsertSubject: "subjects/upsertSubject",
    }),
    submitForm(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          upsertSubject(this.subjectForm)
            .then(res => {
              this.upsertSubject(res.data);
              this.closeModal();
              this.fetchData();
            })
            .catch(() => {
              console.log("Ошибка отправки формы");
            });
        }
      });
    },
    fetchData() {
      this.loading = true;
      getSubjects({ user: this.userId }).then(res => {
        this.mySubjects = res.data;
        this.loading = false;
      });
    },
    deletedSubject(id) {
      this.deleteSubject(id);
    },
    closeModal() {
      this.subjectForm = {
        id: null,
        title: "",
        annotation: "",
      };
      this.windowModal = false;
    },
    editSubject(id) {
      const { title, annotation } = this.mySubjects.find(
        subject => subject.id === id,
      );
      this.subjectForm = { id, title, annotation };
      this.windowModal = true;
    },
  },
};
</script>

<style scoped lang="scss"></style>
