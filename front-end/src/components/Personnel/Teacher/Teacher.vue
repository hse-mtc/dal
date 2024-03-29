<template>
  <el-col
    v-loading="loading || teacherPostsAreLoading || teacherRanksAreLoading"
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
        {{ isProfile ? "Мой профиль" : fullname }}
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
            v-loading="loading || teacherPostsAreLoading || teacherRanksAreLoading"
            class="avatar-uploader"
            action="/api/lms/students/"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :disabled="disableUpload"
          >
            <img
              v-if="displayInfo.photo"
              :src="`/media/` + displayInfo.photo.image"
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
            :disabled="loading || teacherPostsAreLoading || teacherRanksAreLoading"
            hide-required-asterisk
          >
            <el-form-item class="actions">
              <transition name="el-fade-in" mode="out-in">
                <div v-if="modify">
                  <el-button type="primary" plain @click="save">
                    Сохранить
                  </el-button>
                  <el-button type="warning" plain @click="reset">
                    Отмена
                  </el-button>
                </div>
                <template v-else>
                  <AZGuard
                    :permissions="[
                      'teachers.patch.all',
                      {
                        codename: 'teachers.patch.milfaculty',
                        validator: () => milgroup.milfaculty === userMilfaculty,
                      },
                      {
                        codename: 'teachers.patch.milgroup',
                        validator: () =>
                          userMilgroups.some((x) => x === milgroup.milgroup),
                      },
                      {
                        codename: 'teachers.patch.self',
                        validator: () => +id === userId && userType === 'teacher',
                      },
                    ]"
                  >
                    <el-button
                      v-if="isSuperuser"
                      type="info"
                      plain
                      icon="el-icon-edit"
                      @click="startModify"
                    >
                      Редактировать
                    </el-button>
                  </AZGuard>
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
                    firstDayOfWeek: 1,
                  }"
                  format="dd.MM.yyyy"
                  value-format="yyyy-MM-dd"
                  :clearable="false"
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
                    v-for="rank in teacherRanks"
                    :key="rank.value"
                    :label="rank.label"
                    :value="rank.value"
                  />
                </el-select>
                <span v-else class="field-value">
                  {{ teacherRankLabelFromValue(displayInfo.rank) }}
                </span>
              </transition>
            </el-form-item>

            <el-form-item label="Должность" prop="post">
              <transition name="el-fade-in" mode="out-in">
                <el-select
                  v-if="modify"
                  v-model="modifyInfo.post"
                  value-key="post"
                  style="display: block"
                >
                  <el-option
                    v-for="post in teacherPosts"
                    :key="post.value"
                    :label="post.label"
                    :value="post.value"
                  />
                </el-select>
                <span v-else class="field-value">
                  {{ teacherPostLabelFromValue(displayInfo.post) }}
                </span>
              </transition>
            </el-form-item>

            <el-form-item label="Цикл" prop="milfaculty">
              <transition name="el-fade-in" mode="out-in">
                <el-select
                  v-if="modify"
                  v-model="modifyInfo.milfaculty.id"
                  value-key="milfaculty"
                  style="display: block"
                >
                  <el-option
                    v-for="item in milfaculties"
                    :key="item.id"
                    :label="item.title"
                    :value="item.id"
                  />
                </el-select>
                <span v-else class="field-value">
                  {{ milfacultyTitle }}
                </span>
              </transition>
            </el-form-item>

            <el-form-item label="Прикрепленные взвода:" prop="milgroups">
              <transition name="el-fade-in" mode="out-in">
                <el-select
                  v-if="modify"
                  v-model="modifyInfo.milgroups"
                  value-key="id"
                  multiple
                  style="display: block"
                >
                  <el-option
                    v-for="item in milgroups"
                    :key="item.id"
                    :label="item.title"
                    :value="item"
                  >
                    <span style="float: left">{{ item.title }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px; margin-right: 15px;">
                      {{ item.milfaculty.abbreviation }}
                    </span>
                  </el-option>
                </el-select>
                <span v-else-if="displayInfo.milgroups" class="field-value">
                  <div
                    v-for="mg in displayInfo.milgroups"
                    :key="mg.id"
                  >
                    {{ mg.title }}
                    <sub>
                      {{ mg.milfaculty.abbreviation }}
                    </sub>
                  </div>
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
                  {{ personalPhoneNumber }}
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
import { maska } from "maska";

import { patchTeacher, findTeacher } from "@/api/teachers";
import { patchError, getError } from "@/utils/message";
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import moment from "moment";
import { UserModule, ReferenceModule } from "@/store";
import ChangePasswordForm from "@/components/ChangePasswordForm/ChangePasswordForm.vue";
import { TeacherPostsMixin, TeacherRanksMixin } from "@/mixins/teachers";
import { hasPermission } from "@/utils/permissions";

export default {
  name: "Teacher",
  directives: { maska },
  components: { ExpandBox, ChangePasswordForm },
  mixins: [TeacherPostsMixin, TeacherRanksMixin],
  data() {
    return {
      disableUpload: false,
      dialog: false,
      loading: false,
      modify: false,
      phoneBackup: "",
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
            message: "Пожалуйста, выберите звание",
            trigger: "change",
          },
        ],
        post: [
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
    id() {
      return this.$route.params.teacherId;
    },
    isProfile() {
      return this.personType === "teacher" && this.personId === +this.id;
    },
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    userMilgroups() {
      return UserModule.personMilgroups;
    },
    userId() {
      return UserModule.personId;
    },
    userType() {
      return UserModule.personType;
    },
    milgroup() {
      return this.displayInfo.milgroup || {};
    },
    fullname() {
      return this.displayInfo.fullname;
    },
    personalPhoneNumber() {
      return this.displayInfo.contact_info
                      && this.displayInfo.contact_info.personal_phone_number
        ? this.displayInfo.contact_info.personal_phone_number
        : "---";
    },
    milfacultyTitle() {
      return this.displayInfo.milfaculty
        ? this.displayInfo.milfaculty.title
        : "---";
    },
    isSuperuser() {
      return UserModule.isSuperuser;
    },
  },
  async created() {
    await this.fetchInfo();
    if ((parseInt(this.$route.params.teacherId, 16) !== this.userId || this.personType === "student") && !this.isSuperuser) {
      this.disableUpload = true;
    } else {
      this.disableUpload = false;
    }
    // eslint-disable-next-line max-len
    this.displayInfo.contact_info.personal_phone_number = this.maskPhone(this.displayInfo.contact_info.personal_phone_number);
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
      this.phoneBackup = this.displayInfo.contact_info.personal_phone_number;
    },
    maskPhone(phoneBefore) {
      if (phoneBefore.length === 11) {
        return `+ ${phoneBefore[0]} (${phoneBefore[1]}${phoneBefore[2]}${phoneBefore[3]}) ${phoneBefore[4]}${phoneBefore[5]}${phoneBefore[6]}-${phoneBefore[7]}${phoneBefore[8]}-${phoneBefore[9]}${phoneBefore[10]}`;
      }
      return `+ ${phoneBefore}`;
    },
    reset() {
      this.modifyInfo.contact_info.personal_phone_number = this.phoneBackup;
      this.modify = false;
      this.$refs.form.clearValidate();
    },
    async save() {
      const valid = await this.$refs.form.validate();
      if (!valid) {
        return;
      }

      const [surname, name, ...patronymicArray] = this.modifyInfo.fullname
        .replace(/\s+/g, " ")
        .trim()
        .split(" ");
      const patronymic = patronymicArray.join(" ");

      const requestBody = {
        ...this.modifyInfo,
        contact_info: {
          corporate_email: null,
          personal_email: null,
          personal_phone_number: this.parsePhone(this.modifyInfo.contact_info.personal_phone_number),
        },
        milgroups: this.modifyInfo.milgroups.map(x => x.id),
        milfaculty: this.modifyInfo.milfaculty.id,
        surname,
        name,
        patronymic,
        photo: undefined,
        name_genitive: undefined,
        surname_genitive: undefined,
      };

      // eslint-disable-next-line max-len
      this.modifyInfo.contact_info.personal_phone_number = this.maskPhone(this.modifyInfo.contact_info.personal_phone_number);

      this.loading = true;

      try {
        await patchTeacher(requestBody);
      } catch (err) {
        patchError("информации о преподавателе", err.response.status);
        return;
      } finally {
        this.loading = false;
      }

      this.displayInfo = this.modifyInfo;
      this.modify = false;
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

    parsePhone(masked) {
      if (!masked) {
        return null;
      }

      return masked
        .replaceAll("(", "")
        .replaceAll(")", "")
        .replaceAll("-", "")
        .replaceAll(" ", "");
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
