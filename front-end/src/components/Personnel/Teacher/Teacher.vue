<template>
  <el-col
    v-loading="loading"
    :offset="2"
    :span="20"
    class="teacher-page"
  >
    <div class="page-title">
      <div v-if="$route.params.teacherId" class="d-flex align-items-center">
        <img
          src="@/assets/scienceWorks/previous.svg"
          style="position: absolute; left: -40px; cursor: pointer"
          height="22px"
          alt="назад"
          @click="backToPersonnel"
        >
        {{ isProfile ? "Мой профиль" : "Преподаватель" }}
      </div>
      <div v-if="isProfile">
        <el-button type="primary" @click="dialog = true">
          Сменить пароль
        </el-button>
      </div>
    </div>
    <div class="row">
      <ExpandBox title="Основное" non-expandable>
        <div class="teacher-info">
          <el-upload
            v-loading="loading"
            class="avatar-uploader"
            action="/api/lms/students/"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
          >
            <img
              v-if="displayInfo.photo"
              :src="displayInfo.photo.image"
              class="avatar"
            >
            <i v-else class="el-icon-user avatar-uploader-icon" />
          </el-upload>
          <el-form
            ref="form"
            class="form"
            :model="modifyInfo"
            :rules="rules"
            label-width="200px"
            label-position="right"
            size="mini"
            :disabled="loading"
            hide-required-asterisk
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
            <el-form-item label="ФИО:" prop="fullname">
              <transition name="el-fade-in" mode="out-in">
                <el-input v-if="modify" v-model="modifyInfo.fullname" />
                <span v-else class="field-value">
                  {{ displayInfo.fullname }}
                </span>
              </transition>
            </el-form-item>
            <el-form-item label="Дата рождения:" prop="birth_info">
              <transition name="el-fade-in" mode="out-in">
                <el-date-picker
                  v-if="modify"
                  v-model="modifyInfo.birth_info.date"
                  type="date"
                  style="width: 100%;"
                  :picker-options="{
                    disabledDate(time) {
                      return time.getTime() > Date.now();
                    },
                  }"
                  format="dd.MM.yyyy"
                  value-format="yyyy-MM-dd"
                />
                <span v-else class="field-value">
                  {{
                    displayInfo.birth_info
                      ? formatDate(displayInfo.birth_info.date)
                      : "---"
                  }}
                </span>
              </transition>
            </el-form-item>
            <el-form-item label="Звание" prop="rank">
              <transition name="el-fade-in" mode="out-in">
                <el-select
                  v-if="modify"
                  v-model="modifyInfo.rank"
                  value-key="rank"
                  style="display: block"
                >
                  <el-option
                    v-for="item in ranks"
                    :key="item.rank"
                    :label="item.rank"
                    :value="item.rank"
                  />
                </el-select>
                <span v-else class="field-value">
                  {{ displayInfo.rank }}
                </span>
              </transition>
            </el-form-item>

            <el-form-item label="Должность" prop="teacher_post">
              <transition name="el-fade-in" mode="out-in">
                <el-select
                  v-if="modify"
                  v-model="modifyInfo.teacher_post"
                  value-key="teacher_post"
                  style="display: block"
                >
                  <el-option
                    v-for="item in teacherPosts"
                    :key="item.teacher_post"
                    :label="item.teacher_post"
                    :value="item.teacher_post"
                  />
                </el-select>
                <span v-else class="field-value">
                  {{ displayInfo.teacher_post }}
                </span>
              </transition>
            </el-form-item>

            <el-form-item label="Цикл" prop="milfaculty">
              <transition name="el-fade-in" mode="out-in">
                <el-select
                  v-if="modify"
                  v-model="modifyInfo.milfaculty"
                  value-key="milfaculty"
                  style="display: block"
                >
                  <el-option
                    v-for="item in milfaculties"
                    :key="item.milfaculty"
                    :label="item.milfaculty"
                    :value="item.milfaculty"
                  />
                </el-select>
                <span v-else class="field-value">
                  {{ displayInfo.milfaculty }}
                </span>
              </transition>
            </el-form-item>

            <el-form-item label="Прикрепленный взвод:" prop="milgroup">
              <transition name="el-fade-in" mode="out-in">
                <el-select
                  v-if="modify"
                  v-model="modifyInfo.milgroup.milgroup"
                  value-key="milgroup"
                  style="display: block"
                >
                  <el-option
                    v-for="item in milgroups"
                    :key="item.milgroup"
                    :label="item.milgroup"
                    :value="item.milgroup"
                  >
                    <span style="float: left">{{ item.milgroup }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">
                      {{ item.milfaculty }}
                    </span>
                  </el-option>
                </el-select>
                <span v-else class="field-value">
                  {{
                    displayInfo.milgroup ? displayInfo.milgroup.milgroup : "---"
                  }}
                  <sub>
                    {{
                      displayInfo.milgroup
                        ? displayInfo.milgroup.milfaculty
                        : ""
                    }}
                  </sub>
                </span>
              </transition>
            </el-form-item>
            <el-form-item label="Телефон:" prop="personal_phone_number">
              <transition name="el-fade-in" mode="out-in">
                <el-input
                  v-if="modify"
                  v-model="modifyInfo.contact_info.personal_phone_number"
                  v-maska="'# (###) ###-##-##'"
                />
                <span v-else class="field-value">
                  {{
                    displayInfo.contact_info &&
                      displayInfo.contact_info.personal_phone_number
                      ? displayInfo.contact_info.personal_phone_number
                      : "---"
                  }}
                </span>
              </transition>
            </el-form-item>
          </el-form>
        </div>
      </ExpandBox>
    </div>
    <el-dialog
      width="500px"
      :visible.sync="dialog"
      destroy-on-close
      :close-on-click-modal="false"
      :before-close="beforeClose"
    >
      <ChangePasswordForm in-dialog @submited="dialog = false" />
    </el-dialog>
  </el-col>
</template>

<script>
import { patchTeacher, findTeacher } from "@/api/teachers";
import { patchError, getError } from "@/utils/message";
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import moment from "moment";
import { UserModule, ReferenceModule } from "@/store";
import ChangePasswordForm from "@/components/ChangePasswordForm/ChangePasswordForm.vue";

export default {
  name: "Teacher",
  components: { ExpandBox, ChangePasswordForm },
  data() {
    return {
      dialog: false,
      loading: false,
      modify: false,
      displayInfo: {},
      modifyInfo: {},
      rules: {
        fullname: [
          {
            validator: (rule, value, callback) => {
              if (!value) {
                callback(new Error("Пожалуйста, введите ФИО"));
              } else if (
                value
                  .replace(/\s+/g, " ")
                  .trim()
                  .split(" ").length < 2
              ) {
                callback(new Error("Фамилия и имя обязательны"));
              } else {
                callback();
              }
            },
            trigger: "change",
          },
        ],
        birth_info: [
          {
            validator: (rule, value, callback) => {
              if (!value.date) {
                callback(new Error("Пожалуйста, введите дату рождения"));
              } else {
                callback();
              }
            },
            trigger: "change",
          },
        ],
        rank: [
          {
            required: true,
            message: "Пожалуйста, выберите дату рождения",
            trigger: "change",
          },
        ],
        teacher_post: [
          {
            required: true,
            message: "Пожалуйста, выберите должность",
            trigger: "change",
          },
        ],
        milfaculty: [
          {
            required: true,
            message: "Пожалуйста, выберите цикл",
            trigger: "change",
          },
        ],
      },
    };
  },
  computed: {
    personType() {
      return UserModule.personType;
    },
    personId() {
      return UserModule.personId;
    },
    milgroups() {
      return ReferenceModule.milgroups;
    },
    milfaculties() {
      return ReferenceModule.milfaculties;
    },
    ranks() {
      return ReferenceModule.ranks;
    },
    teacherPosts() {
      return ReferenceModule.teacherPosts;
    },
    id() {
      return this.$route.params.teacherId;
    },
    isProfile() {
      return (
        this.personType === "teacher" && this.personId === +this.id
      );
    },
  },
  async created() {
    await this.fetchInfo();
  },
  methods: {
    formatDate: date => (moment(date).isValid() ? moment(date).format("DD.MM.YYYY") : "---"),
    async fetchInfo() {
      const id = this.$route.params.teacherId;
      if (id) {
        try {
          this.loading = true;
          this.displayInfo = (await findTeacher(id)).data;
        } catch (err) {
          getError("преподавателя", err.response.status);
        } finally {
          this.loading = false;
        }
      }
    },
    startModify() {
      this.modify = true;
      this.modifyInfo = { ...this.displayInfo };
      if (!this.modifyInfo.birth_info) {
        this.$set(this.modifyInfo, "birth_info", { date: "" });
      }
      if (!this.modifyInfo.milgroup) {
        this.$set(this.modifyInfo, "milgroup", {});
      }
      if (!this.modifyInfo.contact_info) {
        this.$set(this.modifyInfo, "contact_info", {});
      }
    },
    async save() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          try {
            this.loading = true;
            const [surname, name, ...patronymicArray] = this.modifyInfo.fullname
              .replace(/\s+/g, " ")
              .trim()
              .split(" ");
            const patronymic = patronymicArray.join(" ");
            const requestBody = {
              ...this.modifyInfo,
              milgroup: this.modifyInfo.milgroup.milgroup,
              surname,
              name,
              patronymic,
              photo: undefined,
              // contact_info: undefined,
            };
            await patchTeacher(requestBody);
            this.displayInfo = this.modifyInfo;
            this.modify = false;
          } catch (err) {
            patchError("информации о преподавателе", err.response.status);
          } finally {
            this.loading = false;
          }
        }
      });
    },
    beforeAvatarUpload(file) {
      const isValidType = file.type === "image/jpeg" || file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isValidType) {
        this.$message.error("Изображение должно иметь формат jpeg или png.");
        return false;
      }
      if (!isLt2M) {
        this.$message.error("Размер изображения не должен превышать 2 МБ.");
        return false;
      }

      const reader = new FileReader();
      reader.onloadend = async() => {
        try {
          const base64 = reader.result;
          this.loading = true;
          await patchTeacher({ id: this.id, image: base64 });
          await this.fetchInfo();
        } catch (err) {
          patchError("фотографии преподавателя", err.response.status);
        } finally {
          this.loading = false;
        }
      };
      reader.readAsDataURL(file);

      return true;
    },
    backToPersonnel() {
      this.$router.push({ name: "Personnel" });
    },
    async beforeClose() {
      try {
        await this.$confirm(
          "Вы уверены, что хотите закрыть окно смены пароля?",
          "Подтверждение",
          {
            confirmButtonText: "Да",
            cancelButtonText: "Отмена",
            type: "warning",
          },
        );
        this.dialog = false;
      } catch {}
    },
  },
};
</script>

<style scoped lang="scss">
@import "style.scss";
</style>
