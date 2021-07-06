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
        <el-button type="primary">
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
            label-width="150px"
            label-position="right"
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
                <span v-else class="field-value">
                  {{ displayInfo.fullname }}
                </span>
              </transition>
            </el-form-item>
            <el-form-item label="Дата рождения:">
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
                    :value="item"
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
                  <!-- eslint-disable vue/camelcase -->
                  <el-option
                    v-for="item in teacherPosts"
                    :key="item.teacher_post"
                    :label="item.teacher_post"
                    :value="item"
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
                    :value="item"
                  />
                </el-select>
                <span v-else class="field-value">
                  {{ displayInfo.milfaculty }}
                </span>
              </transition>
            </el-form-item>

            <el-form-item label="Прикрепленный взвод" prop="milgroup">
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
          </el-form>
        </div>
      </ExpandBox>
    </div>
  </el-col>
</template>

<script>
import { patchTeacher, findTeacher } from "@/api/teachers";
import { patchError, getError } from "@/utils/message";
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import moment from "moment";
import { UserModule, ReferenceModule } from "@/store";

export default {
  name: "Teacher",
  components: { ExpandBox },
  data() {
    return {
      loading: false,
      modify: false,
      displayInfo: {},
      modifyInfo: {},
      rules: {
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
        this.personType === "teacher" && this.personId === parseInt(this.id, 10)
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
            const [
              surname,
              name,
              ...patronymicArray
            ] = this.modifyInfo.fullname.split(" ");
            const patronymic = patronymicArray.join(" ");
            const requestBody = {
              ...this.modifyInfo,
              milgroup: this.modifyInfo.milgroup.milgroup,
              teacher_post: this.modifyInfo.teacher_post.id,
              rank: this.modifyInfo.rank.id,
              surname,
              name,
              patronymic,
              photo: undefined,
              contact_info: undefined,
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
  },
};
</script>

<style scoped lang="scss">
@import "style.scss";
</style>
