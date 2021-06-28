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
        <img
          v-if="displayInfo.photo"
          :src="displayInfo.photo.image"
          class="avatar"
        >
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
            <el-input
              v-if="modify"
              v-model="modifyInfo.birth_info.date"
              v-maska="'##.##.####'"
            />
            <span v-else class="field-value">
              {{ displayInfo.birth_info ? displayInfo.birth_info.date : "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Статус:">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.status"
              value-key="status"
              style="display: block"
            >
              <el-option
                v-for="item in studentStatuses"
                :key="item"
                :label="item | statusFilter"
                :value="item"
              />
            </el-select>
            <span v-else class="field-value">
              {{ displayInfo.status | statusFilter }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Должность:">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.student_post"
              value-key="student_post"
              style="display: block"
            >
              <el-option
                v-for="item in studentPosts"
                :key="item.id"
                :label="item.title"
                :value="item.id"
              />
            </el-select>
            <span v-else class="field-value">
              {{
                studentPosts.some((x) => x.id === displayInfo.student_post)
                  ? studentPosts.find((x) => x.id === displayInfo.student_post)
                    .title
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Взвод:">
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
                <span style="float: right; color: #8492a6; font-size: 13px">{{
                  item.milfaculty
                }}</span>
              </el-option>
            </el-select>
            <span v-else class="field-value">
              {{ displayInfo.milgroup.milgroup }}
              <sub> {{ displayInfo.milgroup.milfaculty }} </sub>
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
import { mapActions, mapState } from "vuex";
import { findStudent, patchStudent } from "@/api/students";
import { getError, patchError } from "@/utils/message";

export default {
  name: "StudentGeneral",
  components: { ExpandBox },
  filters: {
    statusFilter(value) {
      switch (value) {
        case "AP":
          return "Абитуриент";
        case "ST":
          return "Обучающийся";
        case "EX":
          return "Отчислен";
        case "GR":
          return "Выпустился";
        default:
          return "Ошибка";
      }
    },
  },
  data() {
    return {
      modify: false,
      displayInfo: {},
      modifyInfo: {},
      loading: false,
      id: this.$route.params.studentId,
    };
  },
  computed: {
    ...mapState("reference", ["milgroups", "studentPosts", "studentStatuses"]),
  },
  async created() {
    await this.fetchInfo();
    await this.fetchMilgroups();
    await this.fetchStudentPosts();
    await this.fetchStudentStatuses();
  },
  methods: {
    ...mapActions("reference", [
      "fetchMilgroups",
      "fetchStudentPosts",
      "fetchStudentStatuses",
    ]),
    async fetchInfo() {
      try {
        this.loading = true;
        this.displayInfo = (await findStudent(this.id)).data;
      } catch (err) {
        getError("информации о студенте", err);
      } finally {
        this.loading = false;
      }
    },
    startModify() {
      this.modify = true;
      this.modifyInfo = { ...this.displayInfo };
    },
    async save() {
      try {
        this.loading = true;
        await patchStudent(this.modifyInfo);
        this.displayInfo = this.modifyInfo;
        this.modify = false;
      } catch {
        patchError("информации о студенте");
      } finally {
        this.loading = false;
      }
    },
    handleAvatarSuccess(res, file) {
      this.modifyInfo.photo.image = URL.createObjectURL(file.raw);
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
