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

    <PrimeTable
      :value="subjects"
      auto-layout
      class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
    >
      <PrimeColumn
        field="title"
        header="Название"
        width="250"
        column-key="title"
      />
      <PrimeColumn
        field="annotation"
        header="Аннотация"
        column-key="annotation"
      />
      <PrimeColumn
        header="Управление"
        width="120"
        column-key="buttons"
      >
        <template #body="{ data }">
          <div class="buttons">
            <img
              class="grow"
              src="../../assets/subject/edit.svg"
              alt=""
              @click="editSubject(data.id)"
            >
            <img
              class="grow"
              src="../../assets/subject/close.svg"
              alt=""
              @click="deleteSubjectHandler(data.id)"
            >
          </div>
        </template>
      </PrimeColumn>
    </PrimeTable>

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
import { Component } from "vue-property-decorator";
import { Message } from "element-ui";

import ModalWindow from "@/components/ModalWindow/ModalWindow";
import CustomText from "@/common/CustomText";
import { SIZES } from "@/utils/appConsts";
import { AppModule, SubjectsModule } from "@/store";

@Component({
  name: "SubjectsControl",
  components: {
    CustomText,
    ModalWindow,
  },
})
class SubjectsControl {
  SIZES = SIZES
  windowModal = false
  subjectForm = {
    id: null,
    title: "",
    annotation: "",
  }

  rules = {
    title: [{ required: true, message: "Обязательное поле" }],
    annotation: [{ required: true, message: "Обязательное поле" }],
  }

  get subjects() { return SubjectsModule.subjects; }
  get userId() { return AppModule.userId; }

  submitForm(name) {
    this.$refs[name].validate(async valid => {
      if (valid) {
        if (await SubjectsModule.upsertSubject(this.subjectForm)) {
          this.closeModal();
        } else {
          Message({
            message: "Ошибка отправки формы",
            type: "error",
          });
        }
      }
    });
  }

  editSubject(id) {
    const { title, annotation } = this.subjects.find(
      subject => subject.id === id,
    );
    this.subjectForm = { id, title, annotation };
    this.windowModal = true;
  }

  closeModal() {
    this.subjectForm = {
      id: null,
      title: "",
      annotation: "",
    };
    this.windowModal = false;
  }

  async deleteSubjectHandler(id) {
    await this.$confirm(
      "Вы уверены, что хотите удалить дисциплину? Это действие не обратимо. Это повлечет за собой удаление всех данных об оценках и расписании, связанных с этой дисциплиной.",
      "Подтверждение",
      {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      },
    );

    if (await SubjectsModule.deleteSubject(id)) {
      Message({
        message: "Предмет удален",
        type: "success",
      });
    } else {
      Message({
        message: "Удаление не удалось",
        type: "error",
      });
    }
  }
}

export default SubjectsControl;
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
