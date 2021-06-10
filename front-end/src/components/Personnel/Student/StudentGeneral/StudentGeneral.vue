<template>
  <ExpandBox title="О студенте" no-expand>
    <div class="general-info">
      <el-upload
        class="avatar-uploader"
        action="https://jsonplaceholder.typicode.com/posts/"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
      >
        <img v-if="displayInfo.photo.image" :src="displayInfo.photo.image" class="avatar">
        <i v-else class="el-icon-picture-outline avatar-uploader-icon" />
      </el-upload>
      <el-form
        ref="form"
        class="form"
        :model="modifyInfo"
        label-position="right"
        label-width="150px"
        size="mini"
        :disabled="loading"
      >
        <el-form-item class="actions">
          <transition name="el-fade-in" mode="out-in">
            <div v-if="modify">
              <el-button type="primary" plain @click="save">
                Сохранить
              </el-button>
              <el-button type="warning" plain @click="modify = false">
                Отмена
              </el-button>
            </div>
            <template v-else>
              <el-button
                type="info"
                plain
                icon="el-icon-edit"
                @click="startModify"
              >
                Редактировать
              </el-button>
            </template>
          </transition>
        </el-form-item>
        <el-form-item label="ФИО:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.fullname" />
            <span v-else class="field-value"> {{ displayInfo.fullname }} </span>
          </transition>
        </el-form-item>
        <el-form-item label="Дата рождения:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.birth_info.date" v-maska="'##.##.####'" />
            <span v-else class="field-value">
              {{ displayInfo.birth_info.date }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Статус:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.status" />
            <span v-else class="field-value"> {{ displayInfo.status }} </span>
          </transition>
        </el-form-item>
        <el-form-item label="Пост:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.student_post" />
            <span v-else class="field-value">
              {{ displayInfo.student_post }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Взвод:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.milgroup.milgroup" />
            <span v-else class="field-value">
              {{ displayInfo.milgroup.milgroup }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Телефон:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.contact_info.phone"
              v-maska="'# (###) ###-##-##'"
            />
            <span v-else class="field-value">
              {{ displayInfo.contact_info.phone }}
            </span>
          </transition>
        </el-form-item>
      </el-form>
    </div>
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";

export default {
  name: "StudentGeneral",
  components: { ExpandBox },
  data() {
    return {
      modify: false,
      displayInfo: {},
      modifyInfo: {},
      loading: false,
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.displayInfo = {
        photo: {
          image: null,
        },
        fullname: "Кацевалов Артем Сергеевич",
        birth_info: {
          date: "23.02.2000",
        },
        status: "AP",
        student_post: "",
        milgroup: {
          milgroup: 1809,
          milfaculty: "ВКС",
        },
        contact_info: {
          phone: "8 (915) 472-16-20",
        },
      };
    },
    startModify() {
      this.modify = true;
      this.modifyInfo = { ...this.displayInfo };
    },
    save() {
      this.displayInfo = this.modifyInfo;
      this.modify = false;
    },
    handleAvatarSuccess(res, file) {
      this.form.foto = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isValidType = file.type === "image/jpeg" || file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isValidType) {
        this.$message.error("Изображение должно иметь формат jpeg или png.");
      }
      if (!isLt2M) {
        this.$message.error("Размер изображения не должен превышать 2 МБ.");
      }
      return isValidType && isLt2M;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
