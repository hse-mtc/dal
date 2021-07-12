<template>
  <ExpandBox title="Основное" non-expandable>
    <div class="general-info">
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
        label-position="right"
        label-width="200px"
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
              <el-button type="warning" plain @click="reset">
                Отмена
              </el-button>
            </div>
            <template v-else>
              <AZGuard
                :permissions="[
                  'students.patch.all',
                  {
                    codename: 'students.patch.milfaculty',
                    validator: () => milgroup.milfaculty === userMilfaculty,
                  },
                  {
                    codename: 'students.patch.milgroup',
                    validator: () =>
                      userMilgroups.some((x) => x === milgroup.milgroup),
                  },
                  {
                    codename: 'students.patch.self',
                    validator: () => +id === userId,
                  },
                ]"
              >
                <el-button
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
            <span v-else class="field-value"> {{ displayInfo.fullname }} </span>
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
        <el-form-item label="Статус:" prop="status">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.status"
              value-key="status"
              style="display: block"
            >
              <el-option
                v-for="(value, key) in STUDENT_STATUSES"
                :key="key"
                :label="value"
                :value="key"
              />
            </el-select>
            <span v-else class="field-value">
              {{ STUDENT_STATUSES[displayInfo.status] || "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Должность:">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.student_post"
              value-key="id"
              clearable
              style="display: block"
            >
              <el-option
                v-for="(value, key) in STUDENT_POSTS"
                :key="key"
                :label="value"
                :value="key"
              />
            </el-select>
            <span v-else class="field-value">
              {{ STUDENT_POSTS[displayInfo.student_post] || "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Взвод:" prop="milgroup">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.milgroup.id"
              value-key="milgroup"
              style="display: block"
            >
              <el-option
                v-for="item in milgroups"
                :key="item.id"
                :label="item.title"
                :value="item"
              >
                <span style="float: left">{{ item.title }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{
                  item.milfaculty.abbreviation
                }}</span>
              </el-option>
            </el-select>
            <span v-else class="field-value">
              {{ displayInfo.milgroup ? displayInfo.milgroup.title : "---" }}
              <sub>
                {{
                  displayInfo.milgroup
                    ? displayInfo.milgroup.milfaculty.title
                    : "---"
                }}
              </sub>
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Телефон:">
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
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import { findStudentBasic, patchStudent } from "@/api/students";
import { getError, patchError } from "@/utils/message";
import moment from "moment";
import { ReferenceModule, UserModule } from "@/store";
import { STUDENT_POSTS, STUDENT_STATUSES } from "@/utils/enums";

export default {
  name: "StudentGeneral",
  components: { ExpandBox },
  props: {
    milgroup: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      STUDENT_POSTS,
      STUDENT_STATUSES,
      modify: false,
      displayInfo: {},
      modifyInfo: {},
      loading: false,
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
        milgroup: [
          {
            required: true,
            message: "Пожалуйста, выберите взвод",
            trigger: "change",
          },
        ],
        status: [
          {
            required: true,
            message: "Пожалуйста, выберите взвод",
            trigger: "change",
          },
        ],
      },
    };
  },
  computed: {
    id() {
      return this.$route.params.studentId;
    },
    milgroups() {
      return ReferenceModule.milgroups;
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
  },
  async created() {
    await this.fetchInfo();
  },
  methods: {
    formatDate: date => moment(date).format("DD.MM.YYYY"),
    async fetchInfo() {
      try {
        this.loading = true;
        this.displayInfo = (await findStudentBasic(this.id)).data;
      } catch (err) {
        getError("информации о студенте", err.response.status);
      } finally {
        this.loading = false;
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
            const [
              surname,
              name,
              ...patronymicArray
            ] = this.modifyInfo.fullname.split(" ");
            const patronymic = patronymicArray.join(" ");
            const requestBody = {
              ...this.modifyInfo,
              milgroup: this.modifyInfo.milgroup.id,
              student_post: this.modifyInfo.student_post.id,
              surname,
              name,
              patronymic,
              photo: undefined,
            };
            await patchStudent(requestBody);
            this.displayInfo = this.modifyInfo;
            this.modify = false;
          } catch (err) {
            patchError("информации о студенте", err.response.status);
          } finally {
            this.loading = false;
          }
        }
      });
    },
    reset() {
      this.modify = false;
      this.$refs.form.clearValidate();
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
          await patchStudent({ id: this.id, image: base64 });
          await this.fetchInfo();
        } catch (err) {
          patchError("фотографии студента", err.response.status);
        } finally {
          this.loading = false;
        }
      };
      reader.readAsDataURL(file);

      return true;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
