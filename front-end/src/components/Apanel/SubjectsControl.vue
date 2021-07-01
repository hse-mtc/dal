<template>
  <div>
    <el-row class="pageTitle">
      <el-col :span="24">
        <div class="d-flex align-items-center justify-content-end">
          <CustomText
            variant="paragraph"
            :custom-style="{ color: '#409EFF', cursor: 'pointer' }"
          >
            <div @click="windowModal = true">
              + Добавить дисциплину
            </div>
          </CustomText>
        </div>
      </el-col>
    </el-row>

    <el-table
      :data="localSubjects"
      style="width: 100%"
    >
      <el-table-column
        fixed
        prop="title"
        label="Название"
        width="250"
        style="word-break: break-word;"
      />
      <el-table-column
        prop="annotation"
        label="Аннотация"
      />
      <el-table-column
        fixed="right"
        label="Управление"
        width="120"
      >
        <template slot-scope="scope">
          <div class="buttons">
            <img
              class="grow"
              src="../../assets/subject/edit.svg"
              alt=""
              @click="editSubject(scope.row.id)"
            >
            <img
              class="grow"
              src="../../assets/subject/close.svg"
              alt=""
              @click="deleteSubjectHandler(scope.row.id)"
            >
          </div>
        </template>
      </el-table-column>
    </el-table>

    <ModalWindow :opened="windowModal" @closeModal="closeModal">
      <CustomText :mb="SIZES.m" :custom-style="{ 'font-weight': 'normal' }" variant="header">
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
            :autosize="{ minRows: 2 }"
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
  </div>
</template>

<script>
import { deleteSubject, getSubjects, upsertSubject } from "@/api/subjects";
import { mapActions, mapState } from "vuex";
import ModalWindow from "@/components/ModalWindow/ModalWindow";
import CustomText from "@/common/CustomText";
import { SIZES } from "@/utils/appConsts";
import { sortBy, isEqual } from "lodash";
import { Message } from "element-ui";

export default {
  name: "SubjectsControl",
  components: {
    CustomText,
    ModalWindow,
  },
  data() {
    return {
      SIZES,
      localSubjects: [],
      windowModal: false,
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
      subjects: state => state.subjects.subjects,
    }),
  },
  watch: {
    subjects: {
      deep: true,
      handler() {
        if (!isEqual(sortBy(this.subjects), sortBy(this.localSubjects))) {
          this.localSubjects = [...this.subjects];
        }
      },
    },
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
    fetchData() {
      if (this.subjects.length === 0) {
        getSubjects()
          .then(response => {
            this.setSubjects(response.data);
            this.localSubjects = [...this.subjects];
          })
          .catch(() => {
            Message({
              message: "Данные по предметам не указаны",
              type: "error",
            });
          });
      } else {
        this.localSubjects = [...this.subjects];
      }
    },
    submitForm(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          upsertSubject(this.subjectForm)
            .then(res => {
              console.log(1);
              this.upsertSubject(res.data);
              this.closeModal();
            })
            .catch(() => {
              Message({
                message: "Ошибка отправки формы",
                type: "error",
              });
            });
        }
      });
    },
    editSubject(id) {
      const { title, annotation } = this.subjects.find(
        subject => subject.id === id,
      );
      this.subjectForm = { id, title, annotation };
      this.windowModal = true;
    },
    closeModal() {
      this.subjectForm = {
        id: null,
        title: "",
        annotation: "",
      };
      this.windowModal = false;
    },
    deleteSubjectHandler(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить дисциплину? Это действие не обратимо. Это повлечет за собой удаление всех данных об оценках и расписании, связанных с этой дисциплиной.",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      ).then(() => {
        deleteSubject(id)
          .then(() => {
            this.deleteSubject(id);
          })
          .catch(err => {
            Message({
              message: "Удаление не удалось",
              type: "error",
            });
            console.log(
              `delete of subject with id: ${this.id} FAILED. Error: ${err}`,
            );
          });
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.buttons {
  z-index: 4;
  align-items: center;
  justify-content: center;
  img {
    cursor: pointer;
    margin-left: $s;

    &.grow {
      transition: all 0.2s ease-in-out;

      &:hover {
        transform: scale(1.2);
      }
    }
  }
}
</style>
