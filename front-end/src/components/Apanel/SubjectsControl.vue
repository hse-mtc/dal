<template>
  <div>
    <el-row class="pageTitle">
      <el-col :span="24">
        <div class="d-flex align-items-center justify-content-end">
          <AZGuard :permissions="['subjects.post.all', 'subjects.post.self']">
            <el-button
              type="text"
              :class="$style.addButton"
              @click="windowModal = true"
            >
              + Добавить дисциплину
            </el-button>
          </AZGuard>
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
        field="milspecialty"
        header="ВУС"
        column-key="milspecialty"
      >
        <template #body="{ data }">
          <div>{{ milspecaltyCode(data.milspecialty) }}</div>
        </template>
      </PrimeColumn>
      <PrimeColumn
        v-if="hasPerm"
        header="Управление"
        width="120"
        column-key="buttons"
      >
        <template #body="{ data }">
          <div :class="$style.buttons">
            <AZGuard
              :permissions="['subjects.patch.all', {
                codename: 'subjects.patch.self',
                validator: () => data.user.id === userId,
              }]"
            >
              <svg-icon
                :class="$style.button"
                icon-class="edit"
                @click="editSubject(data.id)"
              />
            </AZGuard>
            <AZGuard
              :permissions="['subjects.delete.all', {
                codename: 'subjects.delete.self',
                validator: () => data.user.id === userId,
              }]"
            >
              <svg-icon
                :class="$style.button"
                icon-class="close"
                @click="deleteSubjectHandler(data.id)"
              />
            </AZGuard>
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
        <ElFormItem label="Название" prop="title">
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
        <ElFormItem label="ВУС" prop="milspecialty">
          <ElSelect
            v-model="subjectForm.milspecialty"
            filterable
            placeholder="ВУС"
          >
            <ElOption
              v-for="item in milspecialties"
              :key="item.id"
              :label="item.code"
              :value="item.id"
            />
          </ElSelect>
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
import { Component, Vue } from "vue-property-decorator";
import { Message } from "element-ui";

import ModalWindow from "@/components/ModalWindow/ModalWindow";
import CustomText from "@/common/CustomText";
import { SIZES } from "@/utils/appConsts";
import { SubjectsModule, UserModule } from "@/store";
import { hasPermission } from "@/utils/permissions";
import { getMilSpecialties } from "@/api/reference-book";

@Component({
  name: "SubjectsControl",
  components: {
    CustomText,
    ModalWindow,
  },
  data() {
    return {
      milspecialties: [],
    };
  },
  computed: {
    userId() { return UserModule.userId; },
  },
})
class SubjectsControl extends Vue {
  SIZES = SIZES
  windowModal = false
  subjectForm = {
    id: null,
    title: "",
    annotation: "",
    milspecialty: null,
  }

  rules = {
    title: [{ required: true, message: "Обязательное поле" }],
    annotation: [{ required: true, message: "Обязательное поле" }],
    milspecialty: [{ required: true, message: "Обязательное поле" }],
  }

  get subjects() { return SubjectsModule.subjects; }

  async mounted() {
    this.milspecialties = (await getMilSpecialties()).data;
    this.subjectForm.milspecialty = this.milspecialties[0].id;
  }

  submitForm(name) {
    this.$refs[name].validate(async valid => {
      if (valid) {
        if (await SubjectsModule.upsertSubject(this.subjectForm)) {
          this.closeModal();
          Message({
            message: "Дисциплина успешно создана!",
            type: "success",
          });
        } else {
          Message({
            message: "Ошибка создания дисциплины",
            type: "error",
          });
        }
      }
    });
  }

  milspecaltyCode(milspecialtyId) {
    if (milspecialtyId) {
      return this.milspecialties.filter(milspecialty => milspecialty.id === milspecialtyId)[0].code;
    }
    return "-";
  }

  editSubject(id) {
    const { title, annotation, milspecialty } = this.subjects.find(
      subject => subject.id === id,
    );
    this.subjectForm = {
      id, title, annotation, milspecialty,
    };
    this.windowModal = true;
  }

  closeModal() {
    this.subjectForm = {
      id: null,
      title: "",
      annotation: "",
      milspecialty: null,
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

  hasPerm = false;

  created() {
    if (hasPermission(["subjects.patch.all"]) && hasPermission(["subjects.delete.all"])) {
      this.hasPerm = true;
    } else { this.hasPerm = false; }
  }
}

export default SubjectsControl;
</script>

<style lang="scss" module>
@import "@/styles/variables.scss";

.addButton {
  display: block;
  margin: 0 0 0 auto;
  font-size: 18px;
  color: #0c4b9a;
}

.buttons {
  .button {
    font-size: 24px;
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
</style>
